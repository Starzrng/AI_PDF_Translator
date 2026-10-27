# Работы

Команды запускаются из корня репозитория. `source.pdf` и `out/` лежат только локально (в git их нет).

| Работа | Исходник | Режим | Статус | Сборка → результат |
|---|---|---|---|---|
| `d1000-pro-hs` | CreatBot D1000 Pro HS, EN, 32 с. | оверлей (`pdft`) | готово | `.venv/bin/python jobs/d1000-pro-hs/build.py` → `out/D1000 pro HS-user manual-RU.pdf` |
| `sermoon-p1` | Creality Sermoon P1 (3D-сканер), EN, 20 с. альбомных | оверлей (`pdft`) | готово | `.venv/bin/python jobs/sermoon-p1/build.py` → `out/sermoon_p1_scanner_RU.pdf` |
| `sermoon-p1s` | Creality Sermoon P1S (3D-сканер), EN, 23 с. альбомных | оверлей через харнесс | пилот (стр. 2, 3, 5, 20) на одобрении | `.venv/bin/python -m pdft build jobs/sermoon-p1s` → `out/sermoon-p1s_RU.pdf` + `out/qa.json` |
| `falcon2-pro` | Creality Falcon2 Pro (лазерный гравёр), EN, 33 с. | пересборка PyMuPDF | готово, 27 с. | `.venv/bin/python jobs/falcon2-pro/build.py` → `out/Falcon2Pro_RU.pdf`; `imgtr.py` готовит `imgs_ru/` |
| `xm100` | Xhorse XM-100 (5-осевой ЧПУ), ZH, 161 с. | HTML → Chromium | первый полный черновик, 155 с. | `python3 jobs/xm100/build.py` → `jobs/xm100/XM-100_manual_RU.pdf`; полный порядок — `xm100/NOTES.md` |
| `d400-hs` | CreatBot D400 HS, EN, 31 с. | legacy: заливка по потоку (reportlab) | сдано, качество слабое (см. ниже) | `.venv/bin/python jobs/d400-hs/build.py build-inplace-flow jobs/d400-hs/source.pdf jobs/d400-hs/translation.json jobs/d400-hs/out/D400_HS_User_Manual_ru_inplace.pdf` |
| `raystudio-1.7` | RayStudio for Windows 1.7, EN, 19 с. | legacy: наложение панелей (reportlab) | готово; PDF ~100 МБ — сжатие отложено | `.venv/bin/python jobs/raystudio-1.7/build_inplace.py` (19 с.), `build_paired.py` (оригинал + перевод, 40 с.) → `out/` |
| `eagle-1.6` | Eagle LiDAR 1.6, EN, 24 с. | legacy: документ с нуля без иллюстраций | готово | `.venv/bin/python jobs/eagle-1.6/build.py` → `out/Eagle_Manual_V1.6_ru.pdf` |
| `articles/gaussian-splats-part1`, `-part2` | AlphaPixel, веб-статьи | веб-статья | части 1–2 готовы, серия продолжится | — (`.md` + `images/`) |

## Известные проблемы

- **d400-hs**: в режиме `build-inplace-flow` текст перетекает между несвязанными блоками и рвёт предложения, заголовки теряют оформление. В `translation.json` стоит «филамент» вместо «пластик». Кандидат на переделку оверлеем; текст из `translation.json` можно взять за основу. `out/…_paired.pdf` собран до последней правки `translation.json`.
- **raystudio-1.7**: оба PDF ~100 МБ, вероятно, из-за полностью встроенных шрифтов.
