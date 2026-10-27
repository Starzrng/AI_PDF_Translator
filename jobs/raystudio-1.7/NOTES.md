# RayStudio 1.7 — рабочие заметки

Источник: RayStudio for Windows Manual V1.7, 19 страниц, EN. Режим: legacy — наложение панелей (reportlab).

## Сборка
```
.venv/bin/python jobs/raystudio-1.7/build_inplace.py   → out/…_ru_inplace_layout.pdf (19 с.)
.venv/bin/python jobs/raystudio-1.7/build_paired.py    → out/…_ru_with_original_pages.pdf (оригинал + перевод, 40 с.)
```

## Известные проблемы
Оба PDF около 100 МБ, вероятно, из-за полностью встроенных шрифтов. Сжатие отложено пользователем.

## Статус
Готово (август 2026).
