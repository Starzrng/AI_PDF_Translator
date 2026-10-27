# PDF Translator

Перевод технических PDF на русский с сохранением вёрстки. Переводит ИИ-агент (термины, безопасность, единицы — под контролем человека), а код извлекает текст, собирает PDF и проверяет его. Правила для агентов — [`AGENTS.md`](AGENTS.md), список работ и команды сборки — [`jobs/README.md`](jobs/README.md).

## Установка

```bash
python3 -m venv .venv
.venv/bin/pip install -e .
```

Шрифт перевода — Arial из macOS; на другой системе задайте `PDFT_FONT_REGULAR` и `PDFT_FONT_BOLD`. XM-100 собирается системным `python3` с Playwright (`pip install playwright && playwright install chromium`).

## Инструменты ядра

Харнесс для оверлей-работ (подробно — [`docs/harness.md`](docs/harness.md)):

```bash
.venv/bin/python -m pdft inspect jobs/<id>            # что внутри исходника
.venv/bin/python -m pdft init jobs/<id>               # каркас translations.py: абзацы, TODO, память переводов
.venv/bin/python -m pdft build jobs/<id> --pages 2-5  # сборка + автопроверки → out/qa.json
.venv/bin/python -m pdft review jobs/<id> --pages 2-5 # пары «оригинал | перевод» в tmp/<id>/
```

Отдельные утилиты:

```bash
.venv/bin/python -m pdft.blocks jobs/<id>/source.pdf          # инвентарь текстовых блоков → blocks.json / blocks.txt
.venv/bin/python -m pdft.render jobs/<id>/out/<file>.pdf 3-7  # PNG страниц в tmp/render/
.venv/bin/python -m pdft.diff old.pdf new.pdf                 # попиксельная регрессия, exit 1 при разнице
```

## Устройство

- `pdft/` — общее ядро (оверлей, блоки, рендер, сравнение, шрифты).
- `jobs/<id>/` — одна работа на мануал: `build.py`, переводы, `source.pdf`, `out/`.
- `articles/` — переводы веб-статей.
- `docs/` — правила перевода, техника, глоссарии, [`HANDOFF.md`](docs/HANDOFF.md) (история и план).
