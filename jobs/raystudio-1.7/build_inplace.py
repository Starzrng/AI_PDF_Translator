from io import BytesIO
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.pdfgen import canvas


JOB_DIR = Path(__file__).resolve().parent
SOURCE = JOB_DIR / "source.pdf"
OUTPUT = JOB_DIR / "out" / "RayStudio_For_Windows_Manual_V1.7_ru_inplace_layout.pdf"


PAGE_PANELS = {
    1: [
        {"blocks": [1], "text": "<b>Версия 1.7</b>", "expand": (18, 18, 24, 18), "size": 20},
        {
            "blocks": [2],
            "text": (
                "<b>Содержание</b><br/>"
                "Стартовая страница<br/>"
                "Установка ПО<br/>"
                "Требования к системе<br/>"
                "Как скачать и установить<br/>"
                "Загрузка и импорт проекта<br/>"
                "Основной интерфейс<br/>"
                "Обработка данных<br/>"
                "Gaussian Splatting<br/>"
                "Редактирование<br/>"
                "Сшивка панорам<br/>"
                "Координаты контрольных точек<br/>"
                "Экспорт модели<br/>"
                "RTK, базовая станция и GPS<br/>"
                "Измерения, обрезка и коррекция"
            ),
            "expand": (22, 22, 26, 22),
            "size": 14,
        },
        {
            "blocks": [3, 4],
            "text": "<b>RayStudio</b><br/>Руководство для Windows",
            "expand": (90, 36, 130, 48),
            "size": 18,
        },
        {
            "blocks": [5, 6],
            "text": (
                "<b>Актуальные ссылки</b><br/>"
                "Руководство:<br/>forum.jimumeta.com/.../manual/...<br/>"
                "Загрузка RayStudio:<br/>forum.jimumeta.com/.../download.html"
            ),
            "expand": (18, 18, 18, 18),
            "size": 11,
        },
    ],
    2: [
        {"blocks": [1], "text": "<b>Установка ПО</b>", "expand": (18, 14, 18, 14), "size": 18},
        {
            "blocks": [2, 3],
            "text": (
                "<b>Требования к компьютеру</b><br/>"
                "Рекомендуется: Intel Core i7, 64 ГБ ОЗУ, NVIDIA 4060 16 ГБ.<br/>"
                "Минимум: Intel Core i7, 32 ГБ ОЗУ, NVIDIA 3060 12 ГБ."
            ),
            "expand": (18, 18, 18, 18),
            "size": 13,
        },
        {
            "blocks": [4],
            "text": "<b>Как скачать</b><br/>Установочный файл можно получить на официальном сайте.",
            "expand": (18, 18, 18, 18),
            "size": 13,
        },
        {
            "blocks": [5],
            "text": (
                "<b>Как установить</b><br/>"
                "В Windows запустите файл приложения и проходите мастер установки, "
                "нажимая <b>Next</b> до завершения."
            ),
            "expand": (18, 18, 18, 18),
            "size": 13,
        },
    ],
    3: [
        {
            "blocks": [1, 2, 3],
            "text": (
                "<b>Стартовая страница</b><br/>"
                "Раздел <b>Data Transmission</b> используется для передачи данных.<br/>"
                "<b>View Mode</b> показывает миниатюры, <b>List Mode</b> — подробную информацию.<br/>"
                "Доступны действия: открыть связанный проект или создать новый пустой проект."
            ),
            "expand": (20, 18, 20, 20),
            "size": 13,
        }
    ],
    4: [
        {
            "blocks": [1, 2, 3, 4],
            "text": (
                "<b>Загрузка проекта</b><br/>"
                "Поддерживаются три способа: USB-накопитель, кардридер и загрузка через точку доступа.<br/>"
                "Для <b>Hawk до 5.0.6</b> и <b>Eagle</b> работа с картой выполняется через RayStudio.<br/>"
                "Для <b>Hawk 5.0.6+</b> и <b>Raven</b> файлы отображаются на странице <b>Data Transmission</b>, "
                "откуда их можно скачать."
            ),
            "expand": (18, 18, 18, 18),
            "size": 12,
        },
        {
            "blocks": [7, 8, 13],
            "text": (
                "<b>Загрузка через точку доступа</b><br/>"
                "Включите Wi‑Fi на сканере, подключите к нему ПК, откройте <b>Data Transmission</b> и нажмите "
                "<b>Connect</b>. После соединения файлы появятся в списке."
            ),
            "expand": (18, 18, 18, 18),
            "size": 12,
        },
        {
            "blocks": [15, 16],
            "text": (
                "<b>Если передача не стартует</b><br/>"
                "Включите службу геолокации на локальном ПК и подключитесь повторно."
            ),
            "expand": (18, 18, 18, 18),
            "size": 12,
        },
        {
            "blocks": [9, 10, 11, 12],
            "text": (
                "<b>Wi‑Fi и пароли</b><br/>"
                "Eagle: Rayzoom G100 / JMK6XXXXXX<br/>"
                "Hawk: Rayzoom G200 / JMK7XXXXXX<br/>"
                "Пароль по умолчанию: <b>12345678</b><br/>"
                "У Raven имя сети совпадает с серийным номером."
            ),
            "expand": (14, 14, 14, 14),
            "size": 11,
        },
        {
            "blocks": [14],
            "text": (
                "<b>IP устройства</b><br/>"
                "Eagle: 192.168.1.5<br/>"
                "Hawk: 192.168.2.88<br/>"
                "Raven: 192.168.20.110"
            ),
            "expand": (18, 18, 18, 18),
            "size": 11,
        },
    ],
    5: [
        {
            "blocks": [1],
            "text": "<b>Импорт проекта</b><br/>Перед обработкой нужно открыть локальный файл сканирования.",
            "expand": (18, 18, 18, 18),
            "size": 14,
        }
    ],
    6: [
        {
            "blocks": [1, 2],
            "text": (
                "<b>Основной интерфейс</b><br/>"
                "Здесь доступны сохранение данных, полноэкранный режим, системные настройки, импорт файла, "
                "возврат на стартовую страницу и работа с калибровочным файлом."
            ),
            "expand": (18, 18, 18, 18),
            "size": 13,
        },
        {
            "blocks": [3],
            "text": (
                "<b>Основные модули</b><br/>"
                "1. <b>Gaussian Splatting</b> — фотореалистичная 3D-реконструкция.<br/>"
                "2. <b>Panorama Stitching</b> и meshing — панорамы и меш-модели.<br/>"
                "3. <b>Point cloud post-processing</b> — вычисление, раскраска, прореживание и фильтрация."
            ),
            "expand": (18, 18, 18, 18),
            "size": 12,
        },
        {
            "blocks": [4],
            "text": (
                "<b>Account Information</b><br/>"
                "Здесь отображаются сведения о текущей учетной записи и подключенных услугах."
            ),
            "expand": (18, 18, 18, 18),
            "size": 12,
        },
    ],
    7: [
        {
            "blocks": [1, 2],
            "text": (
                "<b>Обработка данных</b><br/>"
                "Нажмите <b>Data Processing</b>, выберите нужные операции и запустите обработку."
            ),
            "expand": (18, 18, 18, 18),
            "size": 13,
        },
        {
            "blocks": [3, 4, 5, 6, 7, 8],
            "text": (
                "<b>Сцена, цвет и изображения</b><br/>"
                "<b>Scan Scene</b>: Indoor / Outdoor / Stairwell подбирают алгоритм под тип сцены.<br/>"
                "<b>Point Cloud Coloring</b> накладывает реальный цвет с камеры на облако точек.<br/>"
                "<b>Resolve Image</b> сохраняет изображения, снятые во время сканирования."
            ),
            "expand": (18, 18, 18, 18),
            "size": 11,
        },
        {
            "blocks": [9, 10, 11, 12],
            "text": (
                "<b>Фильтрация, прореживание и RTK</b><br/>"
                "<b>Filtering</b>: Weak / Medium / Strong для разных уровней шума.<br/>"
                "<b>Thinning</b>: Fast Mode — быстрее, Performance Mode — больше деталей.<br/>"
                "<b>RTK</b> добавляет абсолютные геодезические координаты.<br/>"
                "У Eagle может отображаться <b>Generate Depth Map</b>, у Hawk — <b>Use GPU</b>."
            ),
            "expand": (18, 18, 18, 18),
            "size": 11,
        },
        {
            "blocks": [13, 14, 15, 16, 17, 18, 19, 20],
            "text": (
                "<b>Файлы результатов</b><br/>"
                "После расчета можно получить <b>recalculate_result</b>, <b>recalculate_trj</b>, "
                "<b>filter_result</b>, <b>thinning_result</b>, <b>color</b>, "
                "<b>color_normals_result</b>, <b>rtk_color</b> и <b>rtk_recalculate_result</b>.<br/>"
                "Часть данных скрыта по умолчанию и включается значком видимости в списке."
            ),
            "expand": (18, 18, 18, 18),
            "size": 11,
        },
    ],
    8: [
        {
            "blocks": [1, 2],
            "text": (
                "<b>Gaussian Splatting</b><br/>"
                "Откройте модуль и выберите сцену обработки. Анализ может занять некоторое время."
            ),
            "expand": (18, 18, 18, 18),
            "size": 13,
        },
        {
            "blocks": [3, 4, 5, 6],
            "text": (
                "<b>Этапы и тип сцены</b><br/>"
                "Этапы: <b>Data Preprocessing</b>, <b>Global Optimization</b>, <b>Gaussian Training</b>.<br/>"
                "Тип сцены: <b>Indoor</b>, <b>Open</b> и <b>Half open</b>. Программа подбирает параметры под "
                "масштаб, освещение и структуру сцены."
            ),
            "expand": (18, 18, 18, 18),
            "size": 11,
        },
        {
            "blocks": [7, 8],
            "text": (
                "<b>Качество и режим</b><br/>"
                "<b>High Quality</b> дает максимальную детализацию, <b>Normal</b> — баланс, "
                "<b>High Speed</b> — быстрый черновой результат.<br/>"
                "Режим <b>GPU</b> рекомендуется для ускорения расчета, <b>CPU</b> работает медленнее."
            ),
            "expand": (18, 18, 18, 18),
            "size": 11,
        },
        {
            "blocks": [9, 10, 11, 12, 13, 14, 15],
            "text": (
                "<b>Preview / Export / Upload</b><br/>"
                "Сначала используйте <b>Preview</b> для проверки модели. Затем можно сделать "
                "<b>Export</b> или загрузить результат в облако через <b>Upload</b>.<br/>"
                "Лимиты зависят от плана: Free — до 2 файлов, Basic — до 100, Enterprise — без ограничений."
            ),
            "expand": (18, 18, 18, 18),
            "size": 11,
        },
    ],
    9: [
        {
            "blocks": [1, 2],
            "text": (
                "<b>Panorama Stitching</b><br/>"
                "Модуль создает либо меш из облака точек, либо панораму для fixed-point сканирования."
            ),
            "expand": (18, 18, 18, 18),
            "size": 13,
        },
        {
            "blocks": [3, 4, 5, 6],
            "text": (
                "<b>Mesh и панорама</b><br/>"
                "<b>Constructing-net</b> превращает облако точек в 3D-меш.<br/>"
                "<b>Panorama Stitching</b> сшивает 2D-изображения в панораму без опоры на лазерное облако."
            ),
            "expand": (18, 18, 18, 18),
            "size": 11,
        },
        {
            "blocks": [7, 8, 9, 10, 11, 12],
            "text": (
                "<b>Параметры мешинга</b><br/>"
                "<b>Depth</b> отвечает за уровень детализации.<br/>"
                "<b>Trim</b> подрезает шумы по краям модели.<br/>"
                "<b>Density</b> задает топологию: можно оставить естественные отверстия или сделать модель замкнутой.<br/>"
                "<b>Texture Mapping</b> накладывает текстуры с камеры."
            ),
            "expand": (18, 18, 18, 18),
            "size": 10,
        },
        {
            "blocks": [13, 14, 15, 16, 17],
            "text": (
                "<b>Параметры панорамы</b><br/>"
                "<b>Size</b> управляет разрешением от 4000x2000 до 12000x6000.<br/>"
                "<b>Output Pose Information</b> сохраняет положение камеры для дальнейшей 3D-обработки."
            ),
            "expand": (18, 18, 18, 18),
            "size": 10,
        },
        {
            "blocks": [18, 19, 20, 21, 22, 23, 24, 25, 26, 27],
            "text": (
                "<b>Результаты</b><br/>"
                "В списке данных появляются файлы <b>poissonMeshing_trimmed</b> и <b>texturedMesh</b>.<br/>"
                "Панорамы доступны в текущем окне и в локальных файлах проекта. "
                "Их можно просмотреть, загрузить в облако и переключать стрелками между несколькими изображениями."
            ),
            "expand": (18, 18, 18, 18),
            "size": 10,
        },
    ],
    10: [
        {
            "blocks": [1, 2, 3, 4],
            "text": (
                "<b>Редактирование</b><br/>"
                "Доступны: координаты контрольных точек, обрезка, замыкание траектории, коррекция облака точек и измерения.<br/>"
                "Также можно переключать шесть стандартных видов, входить в first view и сбрасывать камеру к исходному виду."
            ),
            "expand": (18, 18, 18, 18),
            "size": 11,
        },
        {
            "blocks": [5, 6, 7, 8],
            "text": (
                "<b>Отображение облака точек</b><br/>"
                "Настраиваются режим цвета (<b>RGB</b>, <b>Elevation</b>, <b>Intensity</b>), "
                "форма точки, размер точки и цвет фона."
            ),
            "expand": (18, 18, 18, 18),
            "size": 11,
        },
        {
            "blocks": [9, 10, 11, 12, 13],
            "text": (
                "<b>Прозрачность и тени</b><br/>"
                "Ползунок прозрачности делает облако более прозрачным при меньших значениях.<br/>"
                "<b>Shadow Strength</b> меняет плотность тени, <b>Shadow Radius</b> — мягкость ее краев."
            ),
            "expand": (18, 18, 18, 18),
            "size": 11,
        },
    ],
    11: [
        {
            "blocks": [1, 2, 3, 4, 5, 6, 7, 8, 9],
            "text": (
                "<b>Координаты контрольных точек</b><br/>"
                "Инструмент переносит облако точек в мировую систему координат по минимум трем точкам.<br/>"
                "Координаты можно получить RTK-прибором во время съемки или определить их во внешнем ПО, например "
                "<b>Google Earth Pro</b>, переключив систему на <b>UTM</b>."
            ),
            "expand": (18, 18, 18, 18),
            "size": 10,
        },
        {
            "blocks": [10, 11, 12, 13, 14, 15, 16],
            "text": (
                "<b>Ввод координат вручную</b><br/>"
                "Откройте инструмент под данными filtering / thinning / coloring, выберите характерные точки "
                "или точки, добавленные при съемке, и введите для них реальные UTM-координаты X, Y, Z.<br/>"
                "Нужно заполнить минимум три точки."
            ),
            "expand": (18, 18, 18, 18),
            "size": 10,
        },
        {
            "blocks": [17, 18, 19, 20],
            "text": (
                "<b>Экспорт перед Apply</b><br/>"
                "Если нужно сохранить текущие вручную поправленные координаты, экспортируйте их до нажатия <b>Apply</b>.<br/>"
                "Результат обработки появляется как новый файл, например <b>gcp_result.las</b>."
            ),
            "expand": (18, 18, 18, 18),
            "size": 10,
        },
        {
            "blocks": [21, 22, 23, 24, 25],
            "text": (
                "<b>Импорт из TXT</b><br/>"
                "Можно экспортировать пустой TXT-шаблон, заполнить в нем строки координатами X Y Z и затем импортировать его обратно.<br/>"
                "После проверки значений нажмите подтверждение, чтобы получить новый набор координат."
            ),
            "expand": (18, 18, 18, 18),
            "size": 10,
        },
    ],
    12: [
        {
            "blocks": [1, 2, 3, 4],
            "text": (
                "<b>Clip</b><br/>"
                "Поддерживаются polygon clipping и rect clipping.<br/>"
                "Можно удалить точки <b>внутри</b> или <b>снаружи</b> выделенной области, отменить удаление и затем "
                "сохранить новый результат кнопкой <b>Apply</b>."
            ),
            "expand": (18, 18, 18, 18),
            "size": 11,
        },
        {
            "blocks": [5, 6, 7, 8, 9, 10, 11],
            "text": (
                "<b>Результат</b><br/>"
                "После успешного экспорта обрезанные данные добавляются в главное окно и появляются в списке как новый файл, "
                "например <b>all_color_cutting.pcd</b>."
            ),
            "expand": (18, 18, 18, 18),
            "size": 11,
        },
    ],
    13: [
        {
            "blocks": [1, 2],
            "text": (
                "<b>Измерения</b><br/>"
                "Поддерживаются измерение точки, линии, высоты и объема.<br/>"
                "Линейное измерение дает прямое расстояние между точками, "
                "а измерение высоты — вертикальную разницу."
            ),
            "expand": (18, 18, 18, 18),
            "size": 11,
        },
        {
            "blocks": [3, 5, 8],
            "text": (
                "<b>Подготовка</b><br/>"
                "Откройте цветное облако точек без лишних слоев. При необходимости сначала обрежьте все точки вне объекта.<br/>"
                "Размер точек в панели атрибутов можно увеличить, чтобы проще выбирать нужные точки."
            ),
            "expand": (18, 18, 18, 18),
            "size": 11,
        },
        {
            "blocks": [10, 12, 13, 17, 21],
            "text": (
                "<b>Как измерять</b><br/>"
                "<b>Point</b>: щелкните точку и получите координаты.<br/>"
                "<b>Linear</b>: поставьте минимум две точки.<br/>"
                "<b>Height</b>: две точки дают вертикальную высоту.<br/>"
                "<b>Volume</b>: удерживайте Ctrl и выделяйте область мышью."
            ),
            "expand": (18, 18, 18, 18),
            "size": 10,
        },
    ],
    14: [
        {
            "blocks": [1, 2, 3, 4],
            "text": (
                "<b>Start-to-end loop closure</b><br/>"
                "Этот режим повышает точность, если начало и конец маршрута совпадают по месту.<br/>"
                "Перед запуском сначала выполните data calculation, чтобы получить траекторию съемки."
            ),
            "expand": (18, 18, 18, 18),
            "size": 11,
        },
        {
            "blocks": [5, 6, 7, 8],
            "text": (
                "<b>Процедура</b><br/>"
                "Откройте инструмент из списка данных, двойным щелчком выберите стартовую и конечную точки, "
                "затем подгоните зеленое облако по осям X/Y/Z и по углам поворота, пока кадры не совпадут."
            ),
            "expand": (18, 18, 18, 18),
            "size": 11,
        },
        {
            "blocks": [9, 10, 11, 12, 13, 14, 15],
            "text": (
                "<b>Apply и результат</b><br/>"
                "После применения создается новый файл с замкнутой траекторией, например "
                "<b>process_result_manual_loop.amap</b>."
            ),
            "expand": (18, 18, 18, 18),
            "size": 11,
        },
    ],
    15: [
        {
            "blocks": [1, 2, 3, 4],
            "text": (
                "<b>Коррекция облака точек</b><br/>"
                "Откройте интерфейс коррекции, меняйте положение и поворот по осям X/Y/Z, "
                "используйте шесть фиксированных видов и управляющую круговую систему координат."
            ),
            "expand": (18, 18, 18, 18),
            "size": 11,
        },
        {
            "blocks": [5, 6, 7, 8, 9, 10, 11, 12, 13],
            "text": (
                "<b>Сохранение результата</b><br/>"
                "Нажмите <b>Apply</b>, чтобы сохранить исправленное облако точек и добавить его в список данных. "
                "После этого можно выйти через <b>Close</b>."
            ),
            "expand": (18, 18, 18, 18),
            "size": 11,
        },
    ],
    16: [
        {
            "blocks": [1, 2],
            "text": (
                "<b>RTK: способы получения мировых координат</b><br/>"
                "Поддерживаются три варианта: встроенный GPS, базовая станция с файлами наблюдений и параметров, "
                "либо сетевой RTK-сервис дифференциальных поправок.<br/>"
                "Варианты с базовой станцией и RTK доступны только на устройствах с RTK-чипом и внешним GPS."
            ),
            "expand": (18, 18, 18, 18),
            "size": 11,
        },
        {
            "blocks": [3, 4, 5, 6],
            "text": (
                "<b>Built-in GPS</b><br/>"
                "Во время съемки GPS должен быть включен, а в экспортированном наборе данных должен присутствовать "
                "файл <b>GPS_XXXXXX.bag</b>.<br/>"
                "После импорта включите RTK configuration — результат появится в списке данных."
            ),
            "expand": (18, 18, 18, 18),
            "size": 11,
        },
    ],
    17: [
        {
            "blocks": [1, 2, 3, 4, 5, 6, 7, 8, 9],
            "text": (
                "<b>Базовая станция</b><br/>"
                "Нужен сканер с RTK-аксессуарами. Перед съемкой включите базовую станцию, оставьте основной блок неподвижным, "
                "подключите контроллер и используйте режим <b>Static Station</b>. Во время съемки GPS должен быть включен."
            ),
            "expand": (18, 18, 18, 18),
            "size": 10,
        },
        {
            "blocks": [10, 11, 12, 13],
            "text": (
                "<b>Файлы и обработка</b><br/>"
                "В экспортированном наборе должен быть файл <b>RTK_XXXXXX.bin</b>. "
                "Также нужны файлы базовой станции: Observation Data и Parameters / Position Data "
                "(например .25o/.25p или .26o/.26p в зависимости от года).<br/>"
                "После выбора локальной папки с этими файлами запустите обработку."
            ),
            "expand": (18, 18, 18, 18),
            "size": 10,
        },
    ],
    18: [
        {
            "blocks": [1, 2, 3, 4],
            "text": (
                "<b>RTK differential service</b><br/>"
                "Нужен сканер с RTK-чипом и внешним GPS. Перед съемкой устройство должно иметь доступ к сети. "
                "Нужно заранее получить у стороннего провайдера домен, порт, имя пользователя и пароль сервиса поправок.<br/>"
                "Точность зависит от окружающей обстановки, препятствий, скорости движения, состояния ионосферы и спутников."
            ),
            "expand": (18, 18, 18, 18),
            "size": 10,
        },
        {
            "blocks": [5, 6, 7],
            "text": (
                "<b>Процедура</b><br/>"
                "Во время сканирования включите GPS и RTK, затем импортируйте файл <b>RTK_XXXXXX.bin</b>, "
                "включите RTK configuration и дождитесь появления результата в списке данных."
            ),
            "expand": (18, 18, 18, 18),
            "size": 10,
        },
    ],
    19: [
        {
            "blocks": [1, 2, 3],
            "text": (
                "<b>Экспорт модели</b><br/>"
                "Нажмите <b>Export</b> в списке слоев данных справа внизу.<br/>"
                "Сейчас поддерживаются форматы <b>LAS</b>, <b>PCD</b>, <b>PLY</b>, <b>e57</b> и <b>xyz</b>. "
                "В будущем будут добавлены и другие форматы."
            ),
            "expand": (18, 18, 18, 18),
            "size": 12,
        }
    ],
}


def register_font() -> str:
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
        "/Library/Fonts/Arial Unicode.ttf",
        "/System/Library/Fonts/Supplemental/Times New Roman.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            pdfmetrics.registerFont(TTFont("RuOverlay", path))
            return "RuOverlay"
    raise FileNotFoundError("No Cyrillic-capable font found.")


def extract_blocks(page):
    items = []

    def visitor(text, cm, tm, font_dict, font_size):
        t = text.strip().replace("\n", " ")
        x, y = tm[4], tm[5]
        if t and (x > 1 or y > 1):
            items.append((x, y, t))

    page.extract_text(visitor_text=visitor)

    lines = []
    for x, y, t in sorted(items, key=lambda it: (-it[1], it[0])):
        for line in lines:
            if abs(line["y"] - y) < 8:
                line["parts"].append((x, t))
                line["y_vals"].append(y)
                break
        else:
            lines.append({"y": y, "y_vals": [y], "parts": [(x, t)]})

    norm = []
    for line in lines:
        text = " ".join(t for x, t in sorted(line["parts"]))
        minx = min(x for x, t in line["parts"])
        maxx = max(x + len(t) * 6 for x, t in line["parts"])
        norm.append((sum(line["y_vals"]) / len(line["y_vals"]), minx, maxx, text))

    blocks = []
    for y, minx, maxx, text in norm:
        for block in blocks:
            if abs(block["last_y"] - y) < 55 and abs(block["minx"] - minx) < 120:
                block["lines"].append((y, text))
                block["minx"] = min(block["minx"], minx)
                block["maxx"] = max(block["maxx"], maxx)
                block["miny"] = min(block["miny"], y)
                block["maxy"] = max(block["maxy"], y)
                block["last_y"] = y
                break
        else:
            blocks.append(
                {
                    "minx": minx,
                    "maxx": maxx,
                    "miny": y,
                    "maxy": y,
                    "last_y": y,
                    "lines": [(y, text)],
                }
            )

    return sorted(blocks, key=lambda b: (-b["maxy"], b["minx"]))


def union_box(blocks, indices, page_width, page_height, expand):
    selected = [blocks[i - 1] for i in indices]
    x0 = min(b["minx"] for b in selected) - expand[0]
    y0 = min(b["miny"] for b in selected) - expand[1]
    x1 = max(b["maxx"] for b in selected) + expand[2]
    y1 = max(b["maxy"] for b in selected) + expand[3]
    x0 = max(18, x0)
    y0 = max(18, y0)
    x1 = min(page_width - 18, x1)
    y1 = min(page_height - 18, y1)
    return x0, y0, x1, y1


def draw_text_in_box(c, text, box, font_name, font_size):
    x0, y0, x1, y1 = box
    width = x1 - x0 - 14
    height = y1 - y0 - 14
    for size in range(font_size, 7, -1):
        style = ParagraphStyle(
            name=f"box_{size}",
            fontName=font_name,
            fontSize=size,
            leading=size * 1.22,
            textColor=colors.white,
        )
        para = Paragraph(text, style)
        w, h = para.wrap(width, height)
        if h <= height:
            para.drawOn(c, x0 + 7, y1 - 7 - h)
            return
    # Draw at the smallest accepted size if it still overflows.
    style = ParagraphStyle(
        name="box_min",
        fontName=font_name,
        fontSize=7,
        leading=8.4,
        textColor=colors.white,
    )
    para = Paragraph(text, style)
    w, h = para.wrap(width, height)
    para.drawOn(c, x0 + 7, max(y0 + 4, y1 - 7 - min(h, height)))


def build_overlay(page_number, page, blocks, font_name):
    page_width = float(page.mediabox.width)
    page_height = float(page.mediabox.height)
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=(page_width, page_height))
    c.setFillColor(colors.black)

    for panel in PAGE_PANELS.get(page_number, []):
        box = union_box(
            blocks,
            panel["blocks"],
            page_width,
            page_height,
            panel.get("expand", (16, 16, 16, 16)),
        )
        x0, y0, x1, y1 = box
        c.rect(x0, y0, x1 - x0, y1 - y0, fill=1, stroke=0)
        draw_text_in_box(c, panel["text"], box, font_name, panel.get("size", 12))

    c.showPage()
    c.save()
    buffer.seek(0)
    return PdfReader(buffer).pages[0]


def main():
    font_name = register_font()
    reader = PdfReader(str(SOURCE))
    writer = PdfWriter()

    for page_number, page in enumerate(reader.pages, start=1):
        blocks = extract_blocks(page)
        overlay = build_overlay(page_number, page, blocks, font_name)
        page.merge_page(overlay)
        writer.add_page(page)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("wb") as f:
        writer.write(f)

    print(OUTPUT)


if __name__ == "__main__":
    main()
