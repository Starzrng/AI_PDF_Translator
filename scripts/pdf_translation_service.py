#!/usr/bin/env python3
"""Small, agent-friendly PDF translation workflow.

The tool deliberately does not call a machine-translation service.  A human or
AI agent writes the translation JSON after reviewing the extracted source text.
This keeps terminology, safety wording, and page-level quality under review.

Supported output mode: paired pages.  Every original page stays untouched and
is followed by one Russian translation page.  It is the reliable default for
manuals with diagrams, screenshots, tables, and dense technical layout.
"""

from __future__ import annotations

import argparse
import json
import re
from io import BytesIO
from pathlib import Path
from typing import Any

from pypdf import PdfReader, PdfWriter
import pymupdf
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FONT_CANDIDATES = (
    Path("/System/Library/Fonts/Supplemental/Arial Unicode.ttf"),
    Path("/Library/Fonts/Arial Unicode.ttf"),
    Path("/System/Library/Fonts/Supplemental/Times New Roman.ttf"),
)

# Diagram legend pages use narrow, independent cells.  Treating those cells as
# one continuous paragraph scrambles the callout order, so they receive exact
# cell-level replacements.
DIRECT_REPLACEMENTS = {
    3: [
        (90, 72, 411, 46, "• Обслуживание: рекомендуется регулярное обслуживание. Протирайте корпус чистой тканью, удаляйте пыль, остатки клея и мусор с направляющих. Периодически смазывайте оси X, Y и Z.", 8),
        (90, 133, 413, 61, "• Соблюдение законодательства: соблюдайте законы и нормы страны эксплуатации, профессиональную этику и требования безопасности. Запрещено использовать продукцию в незаконных целях. CreatBot не отвечает за правовые последствия нарушений.", 8),
        (90, 225, 415, 30, "ПРИМЕЧАНИЕ\nДополнительная информация и пояснения к основному тексту.", 8.5, 130),
        (90, 272, 415, 46, "СОВЕТ\nРекомендации для оптимизации работы, повышения эффективности и удобства использования.", 8.5, 130),
        (90, 334, 415, 46, "ВНИМАНИЕ\nМеры предосторожности, влияющие на качество печати или работу оборудования. Соблюдайте их, чтобы избежать проблем.", 8.5, 130),
        (90, 397, 415, 46, "ОПАСНОСТЬ\nПотенциальные риски. Несоблюдение требований может привести к повреждению оборудования или тяжёлой травме. Строго соблюдайте указания.", 8.5, 130),
    ],
    5: [
        (218, 76, 158, 24, "Описание изделия", 15),
        (90, 121, 180, 23, "Внешние компоненты", 14),
        (270, 409, 90, 19, "Вид спереди", 11),
        (93, 442, 268, 15, "① Экран                         ② Экструдер", 8.5),
        (93, 459, 334, 15, "③ Нагревательный стол     ④ Отсек филамента", 8.5),
    ],
    6: [
        (93, 89, 292, 15, "① Выход фильтра воздуха          ② Выключатель", 8),
        (93, 105, 342, 15, "③ Порт USB                       ④ Разъём антенны Wi-Fi", 8),
        (93, 121, 311, 15, "⑤ Порт LAN                       ⑥ Разъём питания", 8),
        (276, 463, 65, 19, "Экструдер", 11),
        (93, 496, 301, 15, "① Серводвигатель сопла        ② Двигатель подачи", 8),
        (93, 512, 266, 15, "③ Гайка прижима                 ④ Вентилятор радиатора", 8),
        (93, 528, 325, 15, "⑤ Кожух экструдера             ⑥ Быстросъёмный хотэнд", 8),
        (93, 544, 293, 15, "⑦ Быстросъёмный хотэнд       ⑧ Заслонка сопла", 8),
        (93, 560, 145, 15, "⑨ Вихретоковое выравнивание", 8),
    ],
    7: [
        (174, 305, 221, 19, "Щётка сопла / выравнивание камеры ИИ", 10),
        (93, 338, 322, 15, "① Щётка очистки сопла     ② Выравнивание камеры ИИ", 8.5),
    ],
    16: [
        (90, 76, 250, 24, "Расширенные настройки", 15),
        (90, 112, 390, 18, "Раздел расширенных настроек. Описание параметров приведено на следующей странице.", 8),
    ],
    21: [
        (130, 94, 355, 33, "СОВЕТ\nПо фотографиям ниже оцените печать первого слоя и проверьте, подходит ли зазор между соплом и нагревательным столом.", 8),
        (90, 151, 415, 61, "2. Нажимайте Speed+ или Speed- для изменения скорости печати. К значению 100 % можно быстро вернуться кнопкой «Reset» вверху.\n3. Нажимайте Flow+ или Flow- для точной настройки объёма экструзии. К значению 100 % можно быстро вернуться кнопкой «Reset» вверху.", 8),
    ],
    23: [
        (90, 73, 197, 15, "3. Выполните калибровку Z-смещения.", 8.5),
        (90, 246, 188, 22, "Управление смещением", 14),
        (90, 286, 385, 46, "1. Выберите координаты, требующие калибровки, затем нажмите «Start».\n2. Проверьте положение сопла. Если оно соответствует норме, нажмите «Skip Check»; иначе выполните калибровку.", 7.5),
        (90, 458, 300, 31, "3. После точной установки сопла по центру нажмите Next.\n4. Нажмите Start.", 7.5),
        (90, 614, 405, 18, "5. Ожидание калибровки координат XY.  6. Ожидание калибровки координаты оси Z.", 7.5),
        (299, 76, 210, 51, "ПРИМЕЧАНИЕ\n1. Нажмите числовое значение дистанции перемещения, чтобы сменить шаг одиночного перемещения.\n2. Нажимайте Z+ или Z- для регулировки высоты нагревательного стола.", 6.6),
        (299, 133, 210, 105, "СОВЕТ\nПри калибровке Z-смещения рекомендуется последовательно переходить от больших шагов к малым. Поместите между соплом и платформой щуп 0,1 мм. Нажимайте Z+ и Z-, одновременно двигая щуп. Когда появится отчётливое сопротивление, нажмите «Confirm».", 6.35),
    ],
    24: [
        (90, 73, 190, 16, "7. Настройки параметров проверочной печати.", 8),
        (300, 73, 190, 16, "8. Калибровка завершена.", 8),
        (130, 218, 360, 69, "СОВЕТ\n1. Если проверочная печать не требуется, сразу нажмите «Save».\n2. Задайте температуры сопла и стола по параметрам материала: смотрите этикетку катушки или настройки слайсера.\n3. Для загрузки или замены филамента нажмите «Filament Settings».\n4. Перед «Start Print» убедитесь, что печатная платформа чиста.", 7.25),
    ],
    31: [
        (90, 652, 190, 18, "Контактная информация", 10),
        (90, 685, 422, 61, "Henan Creatbot Technology Limited\nСайт: www.creatbot.com\nЭлектронная почта: sales@creatbot.com\nАдрес: No.150 Lamei Road, Zhongyuan District, Zhengzhou City, Henan Province, China", 8),
    ],
}

MACRO_ROWS = [
    ("Adaptive_Mash", "Калибровка", "Адаптивная калибровка стола"),
    ("CANCEL_PRINT", "Макрос", "Отменить печать"),
    ("ENABLE_MOTOR", "Макрос", "Включить двигатели"),
    ("END_PRINT", "Макрос", "Завершить печать"),
    ("M141", "Управление", "Задать температуру камеры"),
    ("M191", "Управление", "Ожидать температуру камеры"),
    ("PAUSE", "Макрос", "Пауза / прерывание печати"),
    ("PRINT_END", "Макрос", "Окончание печати"),
    ("PRINT_START", "Макрос", "Начало печати"),
    ("RESUME", "Макрос", "Возобновить печать"),
    ("RIGHT_NOZZLE_PROBE", "Управление", "Зонд правого сопла"),
    ("SET_PAUSE_AT_LAYER", "Макрос", "Пауза на заданном слое"),
    ("SET_PAUSE_NEXT_LAYER", "Макрос", "Пауза на следующем слое"),
    ("START_PRINT", "Макрос", "Начать печать"),
    ("T0", "Управление", "Переключить на левое сопло"),
    ("T1", "Управление", "Переключить на правое сопло"),
]

TOC_ROWS = [
    (0, "Описание изделия", "4"),
    (1, "Внешние компоненты", "4"),
    (1, "Технические характеристики", "7"),
    (0, "Описание интерфейса", "7"),
    (1, "Главная страница", "8"),
    (1, "Предварительный нагрев", "8"),
    (1, "Управление осями", "9"),
    (1, "HOME", "10"),
    (1, "Страница филамента", "10"),
    (1, "Выбор файла печати", "11"),
    (1, "Страница настроек", "11"),
    (1, "Сетка стола", "12"),
    (1, "Ограничения принтера", "12"),
    (1, "Настройки вентиляторов", "13"),
    (1, "Макросы", "13"),
    (1, "Обслуживание", "14"),
    (1, "Расширенные настройки", "15"),
    (1, "Расширенные настройки", "16"),
    (1, "Настройки сети Wi-Fi", "17"),
    (1, "Настройки сети", "18"),
    (1, "Облачные функции", "18"),
    (1, "Страница печати", "19"),
    (1, "Точная настройка", "19"),
    (0, "Калибровка машины", "21"),
    (1, "Input Shaper", "21"),
    (1, "Калибровка смещения датчика", "21"),
    (1, "Управление смещением", "22"),
    (0, "Подготовка к печати", "24"),
    (1, "Загрузка ПО", "24"),
    (1, "Настройка программы-слайсера", "24"),
    (1, "Подключение принтера к программе-слайсеру", "25"),
    (1, "Описание процесса слайсинга", "25"),
    (1, "Файл печати: отправка по сети", "27"),
    (1, "Файл печати: автономная печать", "28"),
]

# Page 8 is a dense two-column specification table.  Its original row geometry
# cannot be safely reused after translation: Russian labels are longer and the
# automatic text-block overlay breaks both cell borders and reading order.
# Keep its visual grammar (light section bands, ruled rows, two columns) and
# rebuild the table at the original position instead.
SPECIFICATION_SECTIONS = [
    ("Печать", [
        ("Технология печати", "FDM/FFF"),
        ("Область печати", "Один экструдер: 420 x 400 x 420 мм\nДва экструдера: 365 x 400 x 420 мм"),
        ("Количество сопел", "2"),
        ("Диаметр филамента", "1,75 мм"),
        ("Совместимые материалы", "PLA, ABS, ASA, PP, PETG, PC, Nylon, TPU, ABS-CF, PC-CF, PET-CF, PET-GF, UltraPA-CF, PPS-CF, PA-GF, PA-CF, PA-ABS, PC-ABS, PP-GF, PP-CF и др."),
    ]),
    ("Температура", [
        ("Макс. температура сопла", "420 °C"),
        ("Макс. температура стола", "120 °C"),
        ("Температура камеры", "70 °C"),
    ]),
    ("Скорость", [
        ("Макс. скорость печати", "300 мм/с"),
        ("Расход материала", "90 мм³/с"),
    ]),
    ("Электрика", [
        ("Питание", "110 В, 50-60 Гц; 240 В, 50-60 Гц"),
        ("Дисплей", "7-дюймовый сенсорный экран"),
        ("Номинальная мощность", "Принтер: 220 В / 3200 Вт; 110 В / 2700 Вт"),
        ("Передача файлов", "USB / U-диск / Wi-Fi / LAN"),
    ]),
    ("Особые функции", [
        ("Воздушный фильтр", "HEPA + угольный"),
        ("Управление камерой", "Удалённый мониторинг по камере"),
        ("Технология выравнивания стола", "Вихретоковое выравнивание"),
        ("Технология смещения XY", "Смещение двух сопел по HD-камере"),
        ("Технология заслонки сопла", "Заслонка двух сопел"),
        ("Контроль открытия двери", "Есть"),
    ]),
    ("Механика", [
        ("Печатная пластина", "Авиационный алюминий + съёмный магнитный лист"),
        ("Выравнивание стола", "Автоматическое"),
        ("Экструдер", "Интеллектуальные два экструдера"),
        ("Автоподъём экструдеров", "Есть"),
        ("Точность позиционирования X/Y", "0,00375 мм"),
        ("Точность позиционирования Z", "0,00156 мм"),
    ]),
    ("Размеры и масса", [
        ("Размеры и масса изделия", "785 x 700 x 985 мм, 110 кг"),
        ("Размеры и масса упаковки", "830 x 760 x 1090 мм, 140 кг"),
    ]),
]


def register_cyrillic_font() -> str:
    for path in DEFAULT_FONT_CANDIDATES:
        if path.exists():
            pdfmetrics.registerFont(TTFont("PdfTranslationCyrillic", str(path)))
            return "PdfTranslationCyrillic"
    raise FileNotFoundError(
        "No Cyrillic-capable TrueType font found. Install Arial Unicode or set up a local font."
    )


def clean_source_text(text: str) -> str:
    """Remove common generated-page labels without changing the source meaning."""
    lines = []
    for line in text.splitlines():
        normalized = line.strip()
        if re.fullmatch(r"(?:第\s*\d+\s*页\s*共\s*\d+\s*页|\d+\s*/\s*\d+)", normalized):
            continue
        lines.append(line.rstrip())
    return "\n".join(lines).strip()


def extract_manifest(input_pdf: Path, output_json: Path, language: str) -> None:
    reader = PdfReader(str(input_pdf))
    pages = []
    for page_number, page in enumerate(reader.pages, start=1):
        pages.append(
            {
                "source_page": page_number,
                "source_text": clean_source_text(page.extract_text() or ""),
                "translation_title": "",
                "translation_body": "",
            }
        )

    manifest = {
        "schema_version": 1,
        "source_pdf": str(input_pdf),
        "target_language": language,
        "output_mode": "paired-pages",
        "translator_note": (
            "Fill translation_title and translation_body for every page. "
            "Keep model names, menu labels, G-code commands, units, URLs, and safety terms exact."
        ),
        "pages": pages,
    }
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_manifest(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1 or data.get("output_mode") != "paired-pages":
        raise ValueError("Expected a schema_version 1 paired-pages translation manifest.")
    if not isinstance(data.get("pages"), list) or not data["pages"]:
        raise ValueError("Manifest contains no pages.")
    return data


def wrap_line(text: str, font: str, size: float, max_width: float) -> list[str]:
    """Wrap a line by measured glyph width, preserving technical tokens when possible."""
    if not text:
        return [""]
    words = text.split()
    result: list[str] = []
    current = ""
    for word in words:
        candidate = word if not current else f"{current} {word}"
        if pdfmetrics.stringWidth(candidate, font, size) <= max_width:
            current = candidate
            continue
        if current:
            result.append(current)
            current = word
            continue
        # Very long URL or identifier: split only when necessary.
        part = ""
        for character in word:
            if pdfmetrics.stringWidth(part + character, font, size) > max_width and part:
                result.append(part)
                part = character
            else:
                part += character
        current = part
    if current:
        result.append(current)
    return result


def page_lines(title: str, body: str, font: str, body_size: float, width: float) -> list[tuple[str, float, bool]]:
    lines: list[tuple[str, float, bool]] = []
    for line in wrap_line(title, font, body_size + 4, width):
        lines.append((line, body_size + 4, True))
    lines.append(("", body_size, False))
    for raw_line in body.splitlines():
        text = raw_line.strip()
        if not text:
            lines.append(("", body_size, False))
            continue
        is_bullet = text.startswith(("- ", "• "))
        prefix = "• " if is_bullet else ""
        source = text[2:] if is_bullet else text
        for index, wrapped in enumerate(wrap_line(source, font, body_size, width - (10 if is_bullet else 0))):
            lines.append(((prefix if index == 0 else "  ") + wrapped, body_size, False))
    return lines


def translated_page(page_number: int, title: str, body: str, page_size: tuple[float, float], font: str):
    width, height = page_size
    left = right = 42
    top = 48
    bottom = 38
    usable_width = width - left - right
    body_size = 10.0
    while body_size >= 6.5:
        lines = page_lines(title, body, font, body_size, usable_width)
        required = sum((size * (1.38 if bold else 1.28)) for _, size, bold in lines)
        if required <= height - top - bottom - 30:
            break
        body_size -= 0.5
    else:
        raise ValueError(f"Translation for source page {page_number} does not fit on one page.")

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=page_size)
    pdf.setFillColor(colors.HexColor("#2878B8"))
    pdf.rect(0, height - 17, width, 17, fill=1, stroke=0)
    pdf.setFillColor(colors.HexColor("#2A2A2A"))
    pdf.setFont(font, 8)
    pdf.drawString(left, height - 31, f"РУССКИЙ ПЕРЕВОД - исходная страница {page_number}")
    y = height - top
    for text, size, bold in lines:
        leading = size * (1.38 if bold else 1.28)
        if text:
            pdf.setFont(font, size)
            pdf.setFillColor(colors.HexColor("#18202A") if bold else colors.HexColor("#303944"))
            pdf.drawString(left, y - size, text)
        y -= leading
    pdf.setStrokeColor(colors.HexColor("#BCD9EE"))
    pdf.line(left, 26, width - right, 26)
    pdf.setFillColor(colors.HexColor("#587084"))
    pdf.setFont(font, 7.5)
    pdf.drawString(left, 15, "Оригинальная страница сохранена непосредственно перед этим листом.")
    pdf.drawRightString(width - right, 15, f"Стр. {page_number}")
    pdf.save()
    buffer.seek(0)
    return PdfReader(buffer).pages[0]


def build_paired(input_pdf: Path, manifest_path: Path, output_pdf: Path) -> None:
    manifest = load_manifest(manifest_path)
    reader = PdfReader(str(input_pdf))
    entries = manifest["pages"]
    if len(entries) != len(reader.pages):
        raise ValueError(
            f"Manifest has {len(entries)} pages, but source PDF has {len(reader.pages)} pages."
        )
    font = register_cyrillic_font()
    writer = PdfWriter()
    for page_number, (source, entry) in enumerate(zip(reader.pages, entries), start=1):
        title = str(entry.get("translation_title", "")).strip()
        body = str(entry.get("translation_body", "")).strip()
        if not title or not body:
            raise ValueError(f"Page {page_number} is missing translation_title or translation_body.")
        writer.add_page(source)
        page_size = (float(source.mediabox.width), float(source.mediabox.height))
        writer.add_page(translated_page(page_number, title, body, page_size, font))
    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    with output_pdf.open("wb") as handle:
        writer.write(handle)


def usable_text_blocks(input_pdf: Path) -> list[list[tuple[float, float, float, float]]]:
    """Return source-text rectangles in visual reading order.

    PDF coordinates from PyMuPDF use a top-left origin, which makes them a good
    fit for visual layout inspection. Page counters and the Chinese production
    labels in this particular family of manuals are intentionally left intact.
    """
    document = pymupdf.open(str(input_pdf))
    result: list[list[tuple[float, float, float, float]]] = []
    for page in document:
        boxes = []
        for x0, y0, x1, y1, text, *_ in page.get_text("blocks"):
            normalized = " ".join(text.split())
            if not normalized or y0 < 30 or y1 > page.rect.height - 30:
                continue
            if re.fullmatch(r"\d+\s*/\s*\d+", normalized):
                continue
            # Numbered callouts are part of diagrams; their captions are
            # translated in the accompanying legend, not painted over lines.
            if re.fullmatch(r"\d+(?:\s+\d+)*", normalized):
                continue
            boxes.append((x0, y0, x1, y1))
        result.append(sorted(boxes, key=lambda box: (box[1], box[0])))
    return result


def content_lines(title: str, body: str, font: str, size: float, max_width: float) -> list[str]:
    content = f"{title}\n\n{body}".strip()
    lines: list[str] = []
    for raw in content.splitlines():
        raw = raw.strip()
        if not raw:
            lines.append("")
            continue
        bullet = raw.startswith(("- ", "• "))
        prefix = "• " if bullet else ""
        words = raw[2:] if bullet else raw
        wrapped = wrap_line(words, font, size, max_width - (10 if bullet else 0))
        lines.extend((prefix if index == 0 else "  ") + line for index, line in enumerate(wrapped))
    return lines


def draw_inplace_flow_page(page_size, blocks, title: str, body: str, font: str):
    width, height = page_size
    if not blocks:
        raise ValueError("No usable source-text blocks were found on a page.")

    selected_size = None
    selected_lines: list[str] = []
    # Normal prose uses one of three intentional sizes.  The prior "try every
    # size" strategy made neighbouring pages visibly inconsistent even when
    # their original layouts were alike.
    for size in (8.0, 7.5, 7.0, 6.5, 6.0):
        lines = content_lines(title, body, font, size, max(box[2] - box[0] for box in blocks) - 8)
        capacity = sum(max(1, int((box[3] - box[1] - 5) // (size * 1.24))) for box in blocks)
        if len(lines) <= capacity:
            selected_size = size
            selected_lines = lines
            break
    if selected_size is None:
        raise ValueError("Translated text does not fit into the source page's text regions.")

    buffer = BytesIO()
    overlay = canvas.Canvas(buffer, pagesize=(width, height))
    overlay.setFillColor(colors.white)
    for x0, y0, x1, y1 in blocks:
        overlay.rect(x0 - 1.5, height - y1 - 1.5, x1 - x0 + 3, y1 - y0 + 3, fill=1, stroke=0)

    cursor = 0
    leading = selected_size * 1.24
    overlay.setFillColor(colors.HexColor("#111827"))
    overlay.setFont(font, selected_size)
    for x0, y0, x1, y1 in blocks:
        available = max(1, int((y1 - y0 - 5) // leading))
        y = height - y0 - selected_size - 2
        for _ in range(available):
            if cursor >= len(selected_lines):
                break
            line = selected_lines[cursor]
            if line:
                overlay.drawString(x0 + 2, y, line)
            y -= leading
            cursor += 1
    if cursor != len(selected_lines):
        raise ValueError("Internal layout error: text was truncated.")
    overlay.save()
    buffer.seek(0)
    return PdfReader(buffer).pages[0]


def draw_direct_replacements(page_size, replacements, font: str):
    width, height = page_size
    buffer = BytesIO()
    overlay = canvas.Canvas(buffer, pagesize=(width, height))
    for replacement in replacements:
        x, y, box_width, box_height, text, size, *optional_text_x = replacement
        text_x = optional_text_x[0] if optional_text_x else x
        overlay.setFillColor(colors.white)
        overlay.rect(x - 1, height - y - box_height - 1, box_width + 2, box_height + 2, fill=1, stroke=0)
        chosen = size
        text_width = box_width - (text_x - x) - 2
        lines = content_lines("", text, font, chosen, text_width)
        while chosen >= 5.5 and (
            max((pdfmetrics.stringWidth(line, font, chosen) for line in lines), default=0) > text_width
            or len(lines) * chosen * 1.18 > box_height - 2
        ):
            chosen -= 0.25
            lines = content_lines("", text, font, chosen, text_width)
        overlay.setFillColor(colors.HexColor("#111827"))
        overlay.setFont(font, chosen)
        baseline = height - y - chosen - 1
        for line in lines:
            if line:
                overlay.drawString(text_x, baseline, line)
            baseline -= chosen * 1.18
    overlay.save()
    buffer.seek(0)
    return PdfReader(buffer).pages[0]


def draw_toc_page(page_size, font: str):
    """Lay out the table of contents as rows with fixed indents and leaders."""
    width, height = page_size
    buffer = BytesIO()
    overlay = canvas.Canvas(buffer, pagesize=(width, height))
    overlay.setFillColor(colors.white)
    overlay.rect(80, height - 760, 440, 705, fill=1, stroke=0)
    overlay.setFillColor(colors.HexColor("#111827"))
    overlay.setFont(font, 15)
    overlay.drawCentredString(width / 2, height - 94, "Содержание")
    body_size = 8.5
    leading = 18
    y = 142
    page_right = 505
    for indent, label, page_number in TOC_ROWS:
        if label in {"Описание интерфейса", "Калибровка машины", "Подготовка к печати"}:
            y += 6
        x = 90 + indent * 22
        overlay.setFont(font, body_size)
        overlay.drawString(x, height - y, label)
        label_end = x + pdfmetrics.stringWidth(label, font, body_size)
        number_width = pdfmetrics.stringWidth(page_number, font, body_size)
        dot_width = pdfmetrics.stringWidth(".", font, body_size)
        count = max(0, int((page_right - number_width - 7 - label_end) / dot_width))
        if count:
            overlay.drawString(label_end + 4, height - y, "." * count)
        overlay.drawRightString(page_right, height - y, page_number)
        y += leading
    overlay.save()
    buffer.seek(0)
    return PdfReader(buffer).pages[0]


def draw_label_table(overlay, page_height: float, x: float, top: float, width: float,
                     rows: list[tuple[str, str]], font: str, size: float = 8.0) -> None:
    """Rebuild a two-column numbered legend as actual cells, never a paragraph."""
    row_height = 16.2
    table_height = row_height * len(rows)
    overlay.setFillColor(colors.white)
    overlay.rect(x - 8, page_height - top - table_height - 5, width + 16, table_height + 10, fill=1, stroke=0)
    overlay.setStrokeColor(colors.HexColor("#1F2937"))
    overlay.setLineWidth(0.55)
    overlay.rect(x, page_height - top - table_height, width, table_height, fill=0, stroke=1)
    divider = x + width / 2
    overlay.line(divider, page_height - top, divider, page_height - top - table_height)
    for index in range(1, len(rows)):
        y = page_height - top - index * row_height
        overlay.line(x, y, x + width, y)
    overlay.setFillColor(colors.HexColor("#111827"))
    overlay.setFont(font, size)
    for index, (left, right) in enumerate(rows):
        baseline = page_height - top - index * row_height - 11.3
        overlay.drawString(x + 8, baseline, left)
        overlay.drawString(divider + 8, baseline, right)


def draw_product_components_page(page_number: int, page_size, font: str):
    """Manual layouts for the three diagram legends on pages 5-7."""
    width, height = page_size
    buffer = BytesIO()
    overlay = canvas.Canvas(buffer, pagesize=(width, height))
    overlay.setFillColor(colors.HexColor("#111827"))
    if page_number == 5:
        for x, top, box_width, text, size in (
            (218, 76, 158, "Описание изделия", 15),
            (90, 121, 180, "Внешние компоненты", 14),
            (270, 409, 100, "Вид спереди", 11),
        ):
            overlay.setFillColor(colors.white)
            overlay.rect(x - 2, height - top - 23, box_width + 4, 27, fill=1, stroke=0)
            overlay.setFillColor(colors.HexColor("#111827"))
            overlay.setFont(font, size)
            overlay.drawString(x, height - top - size - 1, text)
        draw_label_table(overlay, height, 90, 442, 415, [
            ("① Экран", "② Экструдер"),
            ("③ Нагревательный стол", "④ Отсек филамента"),
        ], font)
    elif page_number == 6:
        draw_label_table(overlay, height, 90, 89, 415, [
            ("① Выход фильтрации воздуха", "② Выключатель питания"),
            ("③ Порт USB", "④ Разъём антенны Wi-Fi"),
            ("⑤ Порт LAN", "⑥ Разъём питания"),
        ], font)
        overlay.setFillColor(colors.white)
        overlay.rect(270, height - 485, 100, 27, fill=1, stroke=0)
        overlay.setFillColor(colors.HexColor("#111827"))
        overlay.setFont(font, 11)
        overlay.drawString(276, height - 477, "Экструдер")
        draw_label_table(overlay, height, 90, 496, 415, [
            ("① Серводвигатель сопла", "② Двигатель подачи филамента"),
            ("③ Гайка прижима филамента", "④ Вентилятор радиатора"),
            ("⑤ Кожух экструдера", "⑥ Быстросъёмный хотэнд"),
            ("⑦ Быстросъёмный хотэнд", "⑧ Заслонка сопла"),
            ("⑨ Вихретоковое выравнивание стола", ""),
        ], font, 7.45)
    else:
        overlay.setFillColor(colors.white)
        overlay.rect(168, height - 330, 250, 30, fill=1, stroke=0)
        overlay.setFillColor(colors.HexColor("#111827"))
        overlay.setFont(font, 11)
        overlay.drawCentredString(width / 2, height - 319, "Щётка очистки сопла / калибровка по AI-камере")
        draw_label_table(overlay, height, 90, 338, 415, [
            ("① Щётка очистки сопла", "② Калибровка по AI-камере"),
        ], font, 7.7)
    overlay.save()
    buffer.seek(0)
    return PdfReader(buffer).pages[0]


def draw_attention_icons(page_size):
    """Restore the four coloured attention markers after replacing their text."""
    width, height = page_size
    buffer = BytesIO()
    overlay = canvas.Canvas(buffer, pagesize=(width, height))
    for center_y, color, glyph in (
        (240, "#1CA8E1", "i"),
        (287, "#00A94F", "i"),
        (349, "#F58220", "!"),
        (412, "#E31B23", "!"),
    ):
        overlay.setFillColor(colors.HexColor(color))
        overlay.circle(112, height - center_y, 10, fill=1, stroke=0)
        overlay.setFillColor(colors.white)
        overlay.setFont("Helvetica-Bold", 11)
        overlay.drawCentredString(112, height - center_y - 4, glyph)
    overlay.save()
    buffer.seek(0)
    return PdfReader(buffer).pages[0]


def wrapped_cell_lines(text: str, font: str, size: float, width: float) -> list[str]:
    """Wrap explicit cell breaks as well as lines that exceed their column."""
    result: list[str] = []
    for paragraph in text.splitlines() or [""]:
        result.extend(wrap_line(paragraph, font, size, width))
    return result or [""]


def draw_specifications_page(page_size, font: str):
    """Recreate page 8 as a readable Russian specification table."""
    width, height = page_size
    buffer = BytesIO()
    overlay = canvas.Canvas(buffer, pagesize=(width, height))

    # Remove only the old English title/table.  The page decorations and footer
    # remain part of the original background PDF.
    overlay.setFillColor(colors.white)
    overlay.rect(84, height - 766, 450, 710, fill=1, stroke=0)
    overlay.setFillColor(colors.HexColor("#111827"))
    overlay.setFont(font, 15)
    overlay.drawString(90, height - 91, "Технические характеристики")

    left, divider, right = 90, 251, 526
    top = 116
    cursor = top
    row_fill = colors.HexColor("#F5F6F7")
    line_color = colors.HexColor("#D6DCE1")

    def ruled_rect(top_y: float, row_height: float, fill_color=None) -> None:
        if fill_color:
            overlay.setFillColor(fill_color)
            overlay.rect(left, height - top_y - row_height, right - left, row_height, fill=1, stroke=0)
        overlay.setStrokeColor(line_color)
        overlay.setLineWidth(0.6)
        overlay.rect(left, height - top_y - row_height, right - left, row_height, fill=0, stroke=1)

    for section, rows in SPECIFICATION_SECTIONS:
        section_height = 17
        ruled_rect(cursor, section_height, row_fill)
        overlay.setFillColor(colors.HexColor("#1F2937"))
        overlay.setFont(font, 8)
        overlay.drawCentredString((left + right) / 2, height - cursor - 12, section)
        cursor += section_height
        for label, value in rows:
            label_size = 6.55
            value_size = 6.55
            label_lines = wrapped_cell_lines(label, font, label_size, divider - left - 10)
            value_lines = wrapped_cell_lines(value, font, value_size, right - divider - 10)
            max_lines = max(len(label_lines), len(value_lines))
            row_height = max(15, max_lines * 8.0 + 6)
            ruled_rect(cursor, row_height)
            overlay.setStrokeColor(line_color)
            overlay.line(divider, height - cursor, divider, height - cursor - row_height)
            overlay.setFillColor(colors.HexColor("#202832"))
            overlay.setFont(font, label_size)
            label_y = height - cursor - (row_height - len(label_lines) * 8.0) / 2 - label_size + 1
            for line in label_lines:
                overlay.drawCentredString((left + divider) / 2, label_y, line)
                label_y -= 8.0
            overlay.setFont(font, value_size)
            value_y = height - cursor - (row_height - len(value_lines) * 8.0) / 2 - value_size + 1
            for line in value_lines:
                overlay.drawCentredString((divider + right) / 2, value_y, line)
                value_y -= 8.0
            cursor += row_height

    # The calculated table deliberately has a little breathing room above the
    # original footer; this avoids compressing technical values into unreadable
    # type merely to consume the exact original row height.
    overlay.save()
    buffer.seek(0)
    return PdfReader(buffer).pages[0]


def draw_box_text(overlay, page_height: float, x: float, top: float, box_width: float,
                  box_height: float, text: str, font: str, size: float) -> None:
    """Draw wrapped text into a known visual rectangle without spilling out."""
    chosen = size
    lines = content_lines("", text, font, chosen, box_width)
    while chosen > 5.25 and len(lines) * chosen * 1.18 > box_height - 3:
        chosen -= 0.2
        lines = content_lines("", text, font, chosen, box_width)
    overlay.setFillColor(colors.HexColor("#111827"))
    overlay.setFont(font, chosen)
    baseline = page_height - top - chosen - 1
    for line in lines:
        if line:
            overlay.drawString(x, baseline, line)
        baseline -= chosen * 1.18


def draw_tip_box(overlay, page_height: float, x: float, top: float, width: float,
                 height: float, text: str, font: str, dashed: bool = False) -> None:
    """Rebuild a callout interior after hiding source-language text."""
    overlay.setFillColor(colors.white)
    # Include the source border in the wipe.  Otherwise the old outline remains
    # one point outside the new rounded outline and looks like a double frame.
    overlay.rect(x - 7, page_height - top - height - 7, width + 14, height + 14, fill=1, stroke=0)
    overlay.setStrokeColor(colors.HexColor("#00A94F") if not dashed else colors.HexColor("#417EAF"))
    overlay.setLineWidth(1.2)
    if dashed:
        overlay.setDash(4, 2)
    overlay.roundRect(x, page_height - top - height, width, height, 9, fill=0, stroke=1)
    overlay.setDash()
    overlay.setFillColor(colors.HexColor("#00A94F"))
    overlay.circle(x + 22, page_height - top - 20, 10, fill=1, stroke=0)
    overlay.setFillColor(colors.white)
    overlay.setFont("Helvetica-Bold", 11)
    overlay.drawCentredString(x + 22, page_height - top - 24, "i")
    draw_box_text(overlay, page_height, x + 42, top + 7, width - 50, height - 11, text, font, 8)


def draw_fine_tuning_page(page_size, font: str):
    width, height = page_size
    buffer = BytesIO()
    overlay = canvas.Canvas(buffer, pagesize=(width, height))
    draw_tip_box(
        overlay, height, 90, 88, 415, 63,
        "СОВЕТ\nПо фотографиям ниже оцените печать первого слоя и проверьте, подходит ли зазор между соплом и нагревательным столом.",
        font,
    )
    overlay.setFillColor(colors.white)
    overlay.rect(90, height - 215, 415, 66, fill=1, stroke=0)
    draw_box_text(
        overlay, height, 90, 151, 415, 62,
        "2. Нажимайте Speed+ или Speed- для изменения скорости печати. К значению 100 % можно быстро вернуться кнопкой «Reset» вверху.\n3. Нажимайте Flow+ или Flow- для точной настройки объёма экструзии. К значению 100 % можно быстро вернуться кнопкой «Reset» вверху.",
        font, 8,
    )
    overlay.save()
    buffer.seek(0)
    return PdfReader(buffer).pages[0]


def draw_calibration_offset_page(page_size, font: str):
    width, height = page_size
    buffer = BytesIO()
    overlay = canvas.Canvas(buffer, pagesize=(width, height))
    # Repaint the top-right note/tip column in its entirety.  Unlike a simple
    # text patch, this hides every fragment of the original English paragraph.
    overlay.setFillColor(colors.white)
    overlay.rect(292, height - 241, 220, 171, fill=1, stroke=0)
    overlay.setStrokeColor(colors.HexColor("#A7A7A7"))
    overlay.setLineWidth(0.8)
    overlay.line(292, height - 70, 512, height - 70)
    overlay.line(292, height - 241, 512, height - 241)
    overlay.setFillColor(colors.HexColor("#1CA8E1"))
    overlay.circle(304, height - 85, 8, fill=1, stroke=0)
    overlay.setFillColor(colors.white)
    overlay.setFont("Helvetica-Bold", 9)
    overlay.drawCentredString(304, height - 88, "i")
    draw_box_text(overlay, height, 316, 76, 188, 51,
                  "ПРИМЕЧАНИЕ\n1. Нажмите числовое значение дистанции перемещения, чтобы сменить шаг.\n2. Нажимайте Z+ или Z- для регулировки высоты стола.", font, 6.35)
    overlay.setFillColor(colors.HexColor("#00A94F"))
    overlay.circle(304, height - 142, 8, fill=1, stroke=0)
    overlay.setFillColor(colors.white)
    overlay.setFont("Helvetica-Bold", 9)
    overlay.drawCentredString(304, height - 145, "i")
    draw_box_text(overlay, height, 316, 133, 188, 101,
                  "СОВЕТ\nПри калибровке Z-смещения переходите от больших шагов к малым. Поместите между соплом и платформой щуп 0,1 мм. Нажимайте Z+ и Z-, двигая щуп. Когда появится отчётливое сопротивление, нажмите «Confirm».", font, 6.2)
    # The remaining labels are independent source text regions; keep the
    # photographs and screenshots untouched.
    replacements = [item for item in DIRECT_REPLACEMENTS[23] if item[0] < 299]
    direct = draw_direct_replacements(page_size, replacements, font)
    overlay.save()
    buffer.seek(0)
    base = PdfReader(buffer).pages[0]
    base.merge_page(direct)
    return base


def draw_print_verification_page(page_size, font: str):
    width, height = page_size
    buffer = BytesIO()
    overlay = canvas.Canvas(buffer, pagesize=(width, height))
    for x, text in ((90, "7. Настройки параметров проверочной печати."), (300, "8. Калибровка завершена.")):
        overlay.setFillColor(colors.white)
        overlay.rect(x - 1, height - 90, 200, 20, fill=1, stroke=0)
        draw_box_text(overlay, height, x, 73, 195, 16, text, font, 8)
    draw_tip_box(
        overlay, height, 92, 208, 411, 96,
        "СОВЕТ\n1. Если проверочная печать не требуется, сразу нажмите «Save».\n2. Задайте температуры сопла и стола по параметрам материала: смотрите этикетку катушки или настройки слайсера.\n3. Для загрузки или замены филамента нажмите «Filament Settings».\n4. Перед «Start Print» убедитесь, что печатная платформа чиста.",
        font, dashed=True,
    )
    overlay.save()
    buffer.seek(0)
    return PdfReader(buffer).pages[0]


def draw_contact_page(page_size, font: str):
    width, height = page_size
    buffer = BytesIO()
    overlay = canvas.Canvas(buffer, pagesize=(width, height))
    overlay.setFillColor(colors.white)
    overlay.rect(80, height - 760, 440, 135, fill=1, stroke=0)
    overlay.setFillColor(colors.HexColor("#111827"))
    overlay.setFont(font, 10)
    overlay.drawString(90, height - 657, "Контактная информация")
    overlay.setStrokeColor(colors.HexColor("#111827"))
    overlay.setLineWidth(1)
    overlay.line(90, height - 676, 300, height - 676)
    draw_box_text(overlay, height, 90, 690, 420, 57,
                  "Henan Creatbot Technology Limited\nСайт: www.creatbot.com\nЭлектронная почта: sales@creatbot.com\nАдрес: No.150 Lamei Road, Zhongyuan District, Zhengzhou City, Henan Province, China", font, 8)
    overlay.save()
    buffer.seek(0)
    return PdfReader(buffer).pages[0]


def draw_macros_page(page_size, font: str):
    """Rebuild the macro table as three aligned columns, preserving row rhythm."""
    width, height = page_size
    buffer = BytesIO()
    overlay = canvas.Canvas(buffer, pagesize=(width, height))
    overlay.setFillColor(colors.white)
    overlay.rect(88, height - 348, 420, 280, fill=1, stroke=0)
    overlay.rect(88, height - 388, 150, 26, fill=1, stroke=0)
    overlay.rect(88, height - 688, 320, 72, fill=1, stroke=0)
    # Restore the actual table grid.  A previous iteration only repainted its
    # words, which made a structured macro table look like free-floating text.
    left, col_1, col_2, right = 90, 238, 322, 508
    top, header_height, row_height = 68, 24, 16.0
    total_height = header_height + len(MACRO_ROWS) * row_height
    overlay.setStrokeColor(colors.HexColor("#1F2937"))
    overlay.setLineWidth(0.55)
    overlay.rect(left, height - top - total_height, right - left, total_height, fill=0, stroke=1)
    for x in (col_1, col_2):
        overlay.line(x, height - top, x, height - top - total_height)
    overlay.line(left, height - top - header_height, right, height - top - header_height)
    for index in range(1, len(MACRO_ROWS)):
        y = height - top - header_height - index * row_height
        overlay.line(left, y, right, y)
    overlay.setFillColor(colors.HexColor("#111827"))
    overlay.setFont(font, 7.2)
    for x, label in ((164, "Имя"), (259, "Тип"), (378, "Назначение")):
        overlay.drawCentredString(x, height - 84, label)
    y = top + header_height + 11.3
    for name, category, purpose in MACRO_ROWS:
        overlay.drawString(95, height - y, name)
        overlay.drawString(col_1 + 7, height - y, category)
        overlay.drawString(col_2 + 7, height - y, purpose)
        y += row_height
    overlay.setFont(font, 14)
    overlay.drawString(90, height - 382, "Обслуживание")
    overlay.setFont(font, 8)
    maintenance = (
        "Обновление с USB: обновление прошивки с USB-накопителя.\n"
        "Сброс к заводским настройкам: возврат исходных настроек принтера.\n"
        "Экспорт журналов: сохранить журналы работы на USB-накопитель.\n"
        "Перезапуск: перезапустить компонент, в котором возникла ошибка."
    )
    baseline = height - 638
    for line in maintenance.splitlines():
        overlay.drawString(90, baseline, line)
        baseline -= 15
    overlay.save()
    buffer.seek(0)
    return PdfReader(buffer).pages[0]


def build_inplace_flow(input_pdf: Path, manifest_path: Path, output_pdf: Path) -> None:
    manifest = load_manifest(manifest_path)
    reader = PdfReader(str(input_pdf))
    entries = manifest["pages"]
    if len(entries) != len(reader.pages):
        raise ValueError("Manifest page count does not match source PDF.")
    font = register_cyrillic_font()
    blocks_by_page = usable_text_blocks(input_pdf)
    writer = PdfWriter()
    for number, (page, entry, blocks) in enumerate(zip(reader.pages, entries, blocks_by_page), start=1):
        title = str(entry.get("translation_title", "")).strip()
        body = str(entry.get("translation_body", "")).strip()
        if not title or not body:
            raise ValueError(f"Page {number} is missing translation_title or translation_body.")
        page_size = (float(page.mediabox.width), float(page.mediabox.height))
        if number == 4:
            writer.add_page(page)
            writer.pages[-1].merge_page(draw_toc_page(page_size, font))
            continue
        if number in (5, 6, 7):
            writer.add_page(page)
            writer.pages[-1].merge_page(draw_product_components_page(number, page_size, font))
            continue
        if number == 8:
            writer.add_page(page)
            writer.pages[-1].merge_page(draw_specifications_page(page_size, font))
            continue
        if number == 21:
            writer.add_page(page)
            writer.pages[-1].merge_page(draw_fine_tuning_page(page_size, font))
            continue
        if number == 23:
            writer.add_page(page)
            writer.pages[-1].merge_page(draw_calibration_offset_page(page_size, font))
            continue
        if number == 24:
            writer.add_page(page)
            writer.pages[-1].merge_page(draw_print_verification_page(page_size, font))
            continue
        if number == 31:
            writer.add_page(page)
            writer.pages[-1].merge_page(draw_contact_page(page_size, font))
            continue
        if number == 15:
            writer.add_page(page)
            writer.pages[-1].merge_page(draw_macros_page(page_size, font))
            continue
        if number in DIRECT_REPLACEMENTS:
            writer.add_page(page)
            writer.pages[-1].merge_page(draw_direct_replacements(page_size, DIRECT_REPLACEMENTS[number], font))
            if number == 3:
                writer.pages[-1].merge_page(draw_attention_icons(page_size))
            continue
        try:
            overlay = draw_inplace_flow_page(page_size, blocks, title, body, font)
        except ValueError as error:
            # Diagram-only pages sometimes have only compact label tables. Their
            # main title is part of a raster illustration, so preserve that
            # artwork and fit the translated labels first.
            try:
                overlay = draw_inplace_flow_page(page_size, blocks, body, "", font)
                print(f"Page {number}: title retained in source artwork; labels translated in place")
            except ValueError:
                try:
                    overlay = draw_inplace_flow_page(page_size, blocks, title, "", font)
                    print(f"Page {number}: translated title fits; explanatory copy omitted")
                except ValueError:
                    raise ValueError(f"Could not lay out source page {number}: {error}") from error
        writer.add_page(page)
        writer.pages[-1].merge_page(overlay)
    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    with output_pdf.open("wb") as handle:
        writer.write(handle)


def validate_paired(source_pdf: Path, translation_pdf: Path) -> None:
    source_pages = len(PdfReader(str(source_pdf)).pages)
    translated = PdfReader(str(translation_pdf))
    expected_pages = source_pages * 2
    if len(translated.pages) != expected_pages:
        raise ValueError(f"Expected {expected_pages} pages, found {len(translated.pages)}.")
    for page_number in range(1, expected_pages, 2):
        text = translated.pages[page_number].extract_text() or ""
        if "РУССКИЙ ПЕРЕВОД" not in text:
            raise ValueError(f"Translated page {(page_number + 1) // 2} has no readable translation header.")
    print(f"OK: {source_pages} original pages + {source_pages} translation pages = {expected_pages} pages")


def validate_inplace(source_pdf: Path, translation_pdf: Path) -> None:
    source_pages = len(PdfReader(str(source_pdf)).pages)
    translated = PdfReader(str(translation_pdf))
    if len(translated.pages) != source_pages:
        raise ValueError(f"Expected {source_pages} pages, found {len(translated.pages)}.")
    missing = [
        str(index)
        for index, page in enumerate(translated.pages, start=1)
        if not re.search(r"[А-Яа-яЁё]", page.extract_text() or "")
    ]
    if missing:
        raise ValueError("No readable Cyrillic translation on pages: " + ", ".join(missing))
    print(f"OK: {source_pages} pages; Russian text is readable on every page")


def main() -> None:
    parser = argparse.ArgumentParser(description="Agent-assisted, paired-page PDF translation workflow")
    subparsers = parser.add_subparsers(dest="command", required=True)

    extract = subparsers.add_parser("extract", help="Create a JSON translation manifest from a searchable PDF")
    extract.add_argument("input_pdf", type=Path)
    extract.add_argument("output_json", type=Path)
    extract.add_argument("--language", default="ru")

    build = subparsers.add_parser("build", help="Build original-plus-translation paired pages from a manifest")
    build.add_argument("input_pdf", type=Path)
    build.add_argument("manifest_json", type=Path)
    build.add_argument("output_pdf", type=Path)

    inplace = subparsers.add_parser(
        "build-inplace-flow",
        help="Replace source text inside detected text regions while preserving source artwork",
    )
    inplace.add_argument("input_pdf", type=Path)
    inplace.add_argument("manifest_json", type=Path)
    inplace.add_argument("output_pdf", type=Path)

    validate = subparsers.add_parser("validate", help="Check pair count and readable translation headers")
    validate.add_argument("source_pdf", type=Path)
    validate.add_argument("translation_pdf", type=Path)

    validate_inplace_parser = subparsers.add_parser(
        "validate-inplace", help="Check in-place page count and readable Russian text"
    )
    validate_inplace_parser.add_argument("source_pdf", type=Path)
    validate_inplace_parser.add_argument("translation_pdf", type=Path)

    args = parser.parse_args()
    if args.command == "extract":
        extract_manifest(args.input_pdf, args.output_json, args.language)
    elif args.command == "build":
        build_paired(args.input_pdf, args.manifest_json, args.output_pdf)
    elif args.command == "build-inplace-flow":
        build_inplace_flow(args.input_pdf, args.manifest_json, args.output_pdf)
    elif args.command == "validate-inplace":
        validate_inplace(args.source_pdf, args.translation_pdf)
    else:
        validate_paired(args.source_pdf, args.translation_pdf)


if __name__ == "__main__":
    main()
