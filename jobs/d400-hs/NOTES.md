# D400 HS — рабочие заметки

Источник: CreatBot D400 HS User Manual V1.0, 31 страница, EN. Режим: legacy — заливка текстом по потоку (reportlab), сборщик бывшего `scripts/pdf_translation_service.py`.

## Сборка
```
.venv/bin/python jobs/d400-hs/build.py build-inplace-flow jobs/d400-hs/source.pdf jobs/d400-hs/translation.json jobs/d400-hs/out/D400_HS_User_Manual_ru_inplace.pdf
.venv/bin/python jobs/d400-hs/build.py build jobs/d400-hs/source.pdf jobs/d400-hs/translation.json jobs/d400-hs/out/D400_HS_User_Manual_ru_paired.pdf
```

## Известные проблемы
- В режиме `build-inplace-flow` текст перетекает между несвязанными блоками и рвёт предложения, заголовки теряют оформление.
- В `translation.json` стоит «филамент» вместо «пластик».
- `out/…_paired.pdf` собран до последней правки `translation.json`.

## Статус
Сдано (август 2026), качество слабое. Кандидат на переделку через харнесс; текст из `translation.json` — основа.
