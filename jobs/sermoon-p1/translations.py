# -*- coding: utf-8 -*-
"""RU translations for sermoon-p1 (skeleton from `python -m pdft init`).

Fill every html=TODO. Each t() is one segment: `merge` lists the line blocks
joined into it. "TM" comments show translations of matching text from other
jobs: exact ones are prefilled (check them), close ones are hints to adapt.
Rules: docs/translation-conventions.md. Format: pdft/job.py docstring."""

TODO = None
W = "#ffffff"   # white text on dark title bars

TR, OPS, KEEP = {}, [], set()
def t(k, **kw): TR[k] = kw
def op(pg, rect, html, **kw): OPS.append(dict(pg=pg, rect=rect, html=html, **kw))
def keep(*keys): KEEP.update(keys)

# ==================== PAGE 1 ====================
# P1b0  sz10.0 B  (60.7, 362.3, 204.1, 389.7)
# EN: Creality Sermoon P1 3D Scanner Quick Start Guide V1.0
t('P1b0', html='3D-сканер Creality Sermoon P1<br>Краткое руководство V1.0')

# ==================== PAGE 2 ====================
# P2b0  sz12.0 B  (273.7, 43.8, 350.5, 59.8)
# EN: FOREWORD
t('P2b0', html='ПРЕДИСЛОВИЕ')  # TM exact: sermoon-p1s P2b0
# P2b6  sz12.0 B  (542.0, 43.8, 559.4, 59.8)
# EN: EN
t('P2b6', html='RU')  # TM exact: sermoon-p1s P2b8
# P2b2  sz7.0  (57.5, 74.6, 339.0, 131.9)
# EN: Thank you for choosing the Creality Sermoon P1 3D scanner. This guide aims to help you quickly understand the basic information and scanning process of this scanner, opening up a whole new 3D scanning experience. You can visit the Creality official Wiki: https://wiki.creality.com/3d-scanner to get the latest "Creality Sermoon P1 Quick Start Guide", detailed tutorials and videos. This guide will be continuously updated; please refer to the latest version for the most up-to-date information.
t('P2b2', html='Благодарим вас за выбор 3D-сканера Creality Sermoon P1. Это руководство поможет вам быстро разобраться в базовых сведениях и процессе сканирования, открыв для вас совершенно новый опыт 3D-сканирования.<br>Вы можете посетить официальную Wiki Creality: https://wiki.creality.com/3d-scanner, чтобы получить актуальную версию «Краткого руководства Creality Sermoon P1», подробные инструкции и видео.<br>Руководство постоянно обновляется; для получения наиболее актуальной информации обращайтесь к последней версии.')  # TM exact: sermoon-p1/legacy P2b2
# P2b7  sz8.7 B  (379.2, 77.3, 450.5, 88.9)
# EN: Important Notes
t('P2b7', html='<b>Важные примечания</b>')  # TM exact: sermoon-p1s P2b9
# P2b5  sz6.0  (360.6, 91.7, 563.0, 123.7)
# EN: ●Do not allow the scanner to come into contact with water or other liquids. Avoid bumping or impact during use. ●To ensure optimal performance, please operate in a suitable working environment.
t('P2b5', html='● Не допускайте контакта сканера с водой или другими жидкостями. Избегайте ударов и толчков при использовании.<br>● Для оптимальной работы эксплуатируйте устройство в подходящих условиях.')  # TM exact: sermoon-p1s P2b4
# P2b1  sz12.0 B  (242.2, 148.3, 382.1, 164.2)
# EN: TABLE OF CONTENTS
t('P2b1', html='СОДЕРЖАНИЕ')  # TM exact: sermoon-p1s P2b1
# P2b3 +1  sz7.0 B  (57.5, 174.4, 256.7, 362.2)
# EN: <b>1. Product Introduction</b> ● 1.1 Scanner Components ● 1.2 Packing List <b>2. First-Time Use</b> ● 2.1 Standalone Mode (No computer connection required) ● 2.2 PC Connection Mode (Connect to Computer) <b>3. Detailed Explanation of Scanning Modes</b> ● 3.1 Blue Laser Mode ● 3.2 Infrared Mode <b>4. Other Functions</b> ● 4.1 Calibration ● 4.2 System Upgrade ● 4.3 File Transfer <b>5.Specifications</b> ● 5.1 Hardware Parameters <b>6.Precautions</b> ● 6.1 Usage Notes ● 6.2 Maintenance Notes
# TM 97% (sermoon-p1s P2b3): 1. Product Introduction ● 1.1 Scanner Components ● 1.2 Part List 2. First-Time Use ● 2.1 Standalone Mode (No computer connection required) ● 2.2 PC Connection Mode (Connect to Computer) 3. Detailed Explanation of Scanning Modes ● 3.1 Blue Laser Mode ● 3.2 Infrared Mode 4. Other Functions ● 4.1 Calibration ● 4.2 System Upgrade ● 4.3 File Transfer 5.Specifications ● 5.1 Hardware Parameters 6.Precautions ● 6.1 Usage Instructions ● 6.2 Maintenance Instructions
#   → <b>1. Обзор устройства</b><br>● 1.1 Компоненты сканера<br>● 1.2 Комплект поставки<br><b>2. Начало работы</b><br>● 2.1 Автономный режим (без подключения к компьютеру)<br>● 2.2 Режим подключения к ПК (подключение к компьютеру)<br><b>3. Подробное описание режимов сканирования</b><br>● 3.1 Режим синего лазера<br>● 3.2 Инфракрасный режим<br><b>4. Прочие функции</b><br>● 4.1 Калибровка<br>● 4.2 Обновление системы<br>● 4.3 Передача файлов<br><b>5. Характеристики</b><br>● 5.1 Аппаратные параметры<br><b>6. Меры предосторожности</b><br>● 6.1 Указания по эксплуатации<br>● 6.2 Указания по обслуживанию
t('P2b3', merge=['P2b4'], html='<b>1. Обзор устройства</b><br>● 1.1 Компоненты сканера<br>● 1.2 Комплект поставки<br><b>2. Начало работы</b><br>● 2.1 Автономный режим (без подключения к компьютеру)<br>● 2.2 Режим подключения к ПК (подключение к компьютеру)<br><b>3. Подробное описание режимов сканирования</b><br>● 3.1 Режим синего лазера<br>● 3.2 Инфракрасный режим<br><b>4. Прочие функции</b><br>● 4.1 Калибровка<br>● 4.2 Обновление системы<br>● 4.3 Передача файлов<br><b>5. Характеристики</b><br>● 5.1 Аппаратные параметры<br><b>6. Меры предосторожности</b><br>● 6.1 Указания по эксплуатации<br>● 6.2 Указания по обслуживанию')

# ==================== PAGE 3 ====================
# P3b0  sz12.0 B  (219.3, 42.7, 408.6, 58.6)
# EN: 1. PRODUCT INTRODUCTION
t('P3b0', html='1. ОБЗОР УСТРОЙСТВА')  # TM exact: sermoon-p1s P3b0
# P3b19  sz7.0 B  (59.3, 66.6, 147.0, 75.9)
# EN: 1.1 Scanner Components
t('P3b19', html='<b>1.1 Компоненты сканера</b>')  # TM exact: sermoon-p1s P3b1
# P3b23  sz4.0  (404.9, 69.9, 436.4, 81.3)
# EN: Single-Line Laser
t('P3b23', html='Лазер одиночной линии')
# P3b22  sz4.0  (377.7, 75.9, 415.1, 87.3)
# EN: Infrared Fill Light×4
t('P3b22', html='ИК-подсветка × 4')
# P3b24  sz4.0  (419.6, 83.6, 453.4, 95.0)
# EN: Parallel-Line Laser
t('P3b24', html='Лазер паралл.')
# P3b21  sz4.0  (393.5, 85.2, 416.5, 96.6)
# EN: RGB Camera
t('P3b21', html='RGB-камера')  # TM exact: sermoon-p1s P3b9
# P3b26  sz4.0  (448.8, 88.0, 474.7, 99.4)
# EN: DOE Projector
t('P3b26', html='DOE-проектор')  # TM exact: sermoon-p1s P3b13
# P3b32  sz4.0  (194.2, 90.2, 224.2, 101.6)
# EN: HD Touchscreen
t('P3b32', html='Сенсорный HD-экран')  # TM exact: sermoon-p1s P3b2
# P3b25  sz4.0  (426.0, 91.7, 456.2, 103.2)
# EN: Cross-Line Laser
t('P3b25', html='Лазер перекр.')
# P3b33  sz4.0  (225.5, 100.8, 250.7, 112.2)
# EN: Power Button
t('P3b33', html='Кнопка питания')  # TM exact: sermoon-p1s P3b3
# P3b30  sz4.0  (304.6, 103.4, 353.0, 114.8)
# EN: Blue & White Fill Light×12
t('P3b30', html='Синяя и белая подсветка × 12')
# P3b28  sz4.0  (304.6, 119.7, 353.0, 131.1)
# EN: High-Precision Camera×2
t('P3b28', html='Высокоточная камера × 2')
# P3b34  sz4.0  (234.3, 127.7, 269.3, 139.1)
# EN: Start/Pause Button
t('P3b34', html='Кнопка «Старт/Пауза»')  # TM exact: sermoon-p1s P3b4
# P3b29  sz4.0  (310.6, 130.5, 353.0, 141.9)
# EN: Wide-Angle Camera×2
t('P3b29', html='Широкоугольная камера × 2')
# P3b27  sz4.0  (501.8, 134.6, 531.8, 146.0)
# EN: Type-C Interface
t('P3b27', html='Порт Type-C')
# P3b35  sz4.0  (229.8, 173.0, 267.6, 184.4)
# EN: Replaceable Battery
t('P3b35', html='Сменный аккумулятор')  # TM exact: sermoon-p1s P3b5
# P3b20  sz7.0 B  (59.3, 230.0, 115.1, 239.3)
# EN: 1.2 Packing List
t('P3b20', html='<b>1.2 Комплект поставки</b>')  # TM exact: sermoon-p1/legacy P3b20
# P3b1  sz6.0  (90.4, 317.3, 188.3, 334.4)
# EN: Creality Sermoon P1 3D Scanner * 1
t('P3b1', html='3D-сканер Creality Sermoon P1 × 1')
# P3b6  sz6.0  (326.0, 317.8, 372.3, 334.9)
# EN: Spare Battery * 1
t('P3b6', html='Запасной аккумулятор × 1')
# P3b2  sz6.0  (90.4, 330.3, 205.6, 347.4)
# EN: High-Precision Glass Calibration Board * 1
t('P3b2', html='Высокоточная стеклянная калибровочная плита × 1')
# P3b7  sz6.0  (326.0, 330.8, 357.1, 347.9)
# EN: Lanyard * 1
t('P3b7', html='Шнурок × 1')
# P3b3  sz6.0  (90.4, 343.3, 177.6, 360.4)
# EN: Power Adapter + Connectors * 1
t('P3b3', html='Блок питания + переходники × 1')
# P3b8  sz6.0  (326.0, 343.8, 375.1, 360.9)
# EN: Cleaning Cloth * 1
t('P3b8', html='Салфетка для очистки × 1')
# P3b4  sz6.0  (90.4, 356.3, 182.5, 373.4)
# EN: 2m USB 3.0 Type-C Data Cable * 1
t('P3b4', html='Кабель USB 3.0 Type-C, 2 м × 1')
# P3b9  sz6.0  (326.0, 356.8, 503.7, 373.9)
# EN: Quick Start Guide & Certiﬁcate of Conformity & Warranty Card * 1
t('P3b9', html='Краткое руководство, сертификат и гарантийный талон × 1')
# P3b5  sz6.0  (90.4, 369.3, 209.8, 386.4)
# EN: Reﬂective Markers (D6mm * 10, D3mm * 10)
t('P3b5', html='Светоотражающие маркеры (D6 мм × 10, D3 мм × 10)')

# ==================== PAGE 4 ====================
# P4b0  sz12.0 B  (251.1, 42.7, 372.7, 58.6)
# EN: 2. FIRST-TIME USE
t('P4b0', html='2. НАЧАЛО РАБОТЫ')  # TM exact: sermoon-p1s P5b0
# P4b1  sz7.0 B  (57.2, 68.1, 566.9, 86.4)
# EN: Creality Sermoon P1 supports two working modes: standalone mode and PC connection mode. You can choose the appropriate mode to operate according to your needs.
t('P4b1', html='<b>Creality Sermoon P1 поддерживает два режима работы: автономный режим и режим подключения к ПК. Вы можете выбрать подходящий режим в зависимости от ваших задач.</b>')  # TM exact: sermoon-p1/legacy P4b1
# P4b6  sz7.0 B  (57.2, 104.3, 472.9, 121.4)
# EN: <b>2.1 Standalone Mode (No computer connection required)</b> <span style="font-size:6.0px">The Creality Sermoon P1 3D scanner has a built-in operating system and screen, allowing it to perform scanning and basic processing independently.</span>
t('P4b6', size=6, html='<span style="font-size:7px"><b>2.1 Автономный режим (без подключения к компьютеру)</b></span><br>3D-сканер Creality Sermoon P1 имеет встроенную операционную систему и экран, что позволяет ему выполнять сканирование и базовую обработку самостоятельно.')  # TM exact: sermoon-p1/legacy P4b6
# P4b2  sz6.0 B  (57.2, 132.3, 556.5, 167.3)
# EN: <span style="font-size:7.0px"><b>Step 1: Power-on Preparation</b></span> Make sure the scanner has sufficient power. <span style="color:#cc5e2c">Note: Before charging, users should select the appropriate connector according to their country and push the selected connector into the adapter body (the adapter body prongs </span> <span style="color:#cc5e2c">are fixed and cannot be lifted directly for use) .</span>
t('P4b2', html='<span style="font-size:7px"><b>Шаг 1: Подготовка к включению</b></span><br>Убедитесь, что сканер достаточно заряжен.<br>Примечание: перед зарядкой выберите подходящий переходник в соответствии с вашей страной и вставьте его в корпус адаптера (штыри корпуса адаптера зафиксированы и не могут быть подняты для использования напрямую).')  # TM exact: sermoon-p1/legacy P4b2
# P4b3  sz6.0  (57.2, 177.4, 330.7, 185.3)
# EN: Press and hold the power button for 2 seconds to turn on the device and enter the main interface.
t('P4b3', html='Нажмите и удерживайте кнопку питания 2 секунды, чтобы включить устройство и войти в главный интерфейс.')  # TM exact: sermoon-p1/legacy P4b3
# P4b4  sz6.0  (57.2, 195.4, 131.7, 203.3)
# EN: Complete First-Time Setup
t('P4b4', html='Завершите первоначальную настройку')  # TM exact: sermoon-p1s P5b12
# P4b5.1  sz6.0  (57.2, 221.2, 229.4, 229.2)
# EN: 1. Language Selection : Select your language and click [Next].
t('P4b5.1', html='1. Выбор языка: выберите язык и нажмите «Next» (Далее).')  # TM exact: sermoon-p1s P5b15
# P4b5.2  sz6.0  (326.5, 221.4, 562.8, 236.3)
# EN: 2. Network Connection: Select an available local area network. Once connected, you will be automatically prompted to proceed to the next step.
# TM 82% (sermoon-p1s P5b14): 2. Network connection: Select an available local area network . After the connection is established, the system will automatically proceed to the next step.
#   → 2. Подключение к сети: выберите доступную локальную сеть. После подключения система автоматически перейдёт к следующему шагу.
t('P4b5.2', html='2. Подключение к сети: выберите доступную локальную сеть. После подключения система автоматически предложит перейти к следующему шагу.')

# ==================== PAGE 5 ====================
# P5b0  sz6.0  (56.8, 37.5, 376.3, 45.4)
# EN: 3. Privacy Policy: Please read and agree to our relevant Privacy Policy and User Agreement before using the device.
t('P5b0', html='3. Политика конфиденциальности: перед использованием устройства прочтите и примите нашу Политику конфиденциальности и Пользовательское соглашение.')  # TM exact: sermoon-p1/legacy P5b0
# P5b1  sz6.0  (57.1, 222.5, 233.7, 230.5)
# EN: 4. Activation: Device activation takes a while, please be patient.
t('P5b1', html='4. Активация: активация устройства занимает некоторое время, подождите.')  # TM exact: sermoon-p1s P6b1

# ==================== PAGE 6 ====================
# P6b0  sz6.0  (56.7, 37.5, 393.9, 45.4)
# EN: 5. Account Login: Supports login with Creality Cloud account . Login can be skipped without affecting normal device use.
t('P6b0', html='5. Вход в аккаунт: поддерживается вход через аккаунт Creality Cloud. Вход можно пропустить без ущерба для нормальной работы устройства.')  # TM exact: sermoon-p1/legacy P6b0
# P6b1  sz6.0  (56.7, 224.6, 394.9, 232.6)
# EN: Skipping login will trigger a confirmation pop-up. If you still do not log in, select "Don’t Use" to proceed to the next page.
t('P6b1', html="Пропуск входа вызовет всплывающее подтверждение. Если вы всё же не входите, выберите «Don't Use» (Не использовать), чтобы перейти на следующую страницу.")  # TM exact: sermoon-p1/legacy P6b1

# ==================== PAGE 7 ====================
# P7b2  sz6.0  (56.7, 37.5, 418.5, 45.4)
# EN: 6. Device Protection: On this page, you can set a device power-on password to prevent unauthorized users from using the device.
t('P7b2', html='6. Защита устройства: на этой странице можно задать пароль включения, чтобы устройством не могли пользоваться посторонние.')  # TM exact: sermoon-p1s P8b2
# P7b0  sz6.0  (56.7, 211.6, 256.1, 219.6)
# EN: 7. Welcome Page: Tap anywhere on the screen to start using the device.
t('P7b0', html='7. Страница приветствия: коснитесь любого места экрана, чтобы начать работу с устройством.')  # TM exact: sermoon-p1s P8b0
# P7b1  sz6.0  (56.7, 376.5, 557.5, 384.4)
# EN: 8. Beginner Tutorial Video: You can choose whether to skip it. After watching/skipping, you will be taken directly to the device scanning page to start your first scanning experience.
t('P7b1', html='8. Обучающее видео для начинающих: его можно пропустить. После просмотра или пропуска вы сразу перейдёте на страницу сканирования и сможете выполнить первое сканирование.')  # TM exact: sermoon-p1s P8b1

# ==================== PAGE 8 ====================
# P8b2  sz7.0 B  (56.7, 35.5, 135.8, 44.8)
# EN: Step 2: Start Scanning
t('P8b2', html='<b>Шаг 2: Начало сканирования</b>')  # TM exact: sermoon-p1s P9b3
# P8b0  sz6.0  (56.7, 47.3, 419.4, 73.3)
# EN: ● Tap "New Project" on the screen to enter the scan preview page. ● Select the appropriate scan mode (Blue Laser/Infrared) and related settings based on the features of the object being scanned. ● Select the appropriate scan settings and click "Apply" to scan in the selected settings.
t('P8b0', html='● Коснитесь «New Project» (Новый проект) на экране, чтобы перейти на страницу предпросмотра сканирования.<br>● Выберите подходящий режим сканирования (синий лазер / инфракрасный) и связанные настройки в зависимости от особенностей сканируемого объекта.<br>● Выберите подходящие настройки сканирования и нажмите «Apply» (Применить), чтобы сканировать с выбранными настройками.')  # TM exact: sermoon-p1/legacy P8b0
# P8b1  sz6.0  (56.7, 239.5, 546.5, 254.5)
# EN: ● Adjust the Scanning Distance : Move the scanner to adjust its distance from the scanned object. When the distance indicator bar on the right side of the screen is within the green "Optimal" range, it means the current distance is ideal for scanning.
t('P8b1', html='● Регулировка расстояния сканирования: перемещайте сканер, изменяя расстояние до объекта. Когда индикатор расстояния справа на экране находится в зелёной зоне «Optimal» (Оптимально), расстояние идеально для сканирования.')  # TM exact: sermoon-p1s P10b0

# ==================== PAGE 9 ====================
# P9b0  sz6.0  (56.7, 41.9, 546.9, 56.9)
# EN: ● Start Scanning: Short press the Start/Pause button on the scanner, or tap the [Start] button on the screen. Keep the scanner aimed at the object, move it steadily and slowly, and scan the object from all angles.
t('P9b0', html='● Начало сканирования: коротко нажмите кнопку «Старт/Пауза» на сканере или коснитесь кнопки «Start» (Старт) на экране. Держите сканер направленным на объект, перемещайте его плавно и медленно, сканируя объект со всех сторон.')  # TM exact: sermoon-p1/legacy P9b0
# P9b1  sz6.0  (56.7, 62.9, 556.2, 77.9)
# EN: ● Complete Scanning: Once the data acquisition is complete, press and hold the Start/Pause button on the scanner for more than 2 seconds, or tap "Finish" on the device screen . The scanned point cloud data will be automatically displayed on the screen.
t('P9b1', html='● Завершение сканирования: после завершения сбора данных нажмите и удерживайте кнопку «Старт/Пауза» на сканере более 2 секунд или коснитесь «Finish» (Готово) на экране устройства. Полученные данные облака точек автоматически отобразятся на экране.')  # TM exact: sermoon-p1/legacy P9b1
# P9b2  sz8.0 B  (56.7, 95.2, 523.4, 114.3)
# EN: <b>Step 3: Model Processing </b> <span style="font-size:6.0px">After the scanning is complete, you can use the processing function built into the Creality Sermoon P1 device to generate the final 3D model from the point cloud data.</span>
t('P9b2', size=6, html='<span style="font-size:8px"><b>Шаг 3: Обработка модели</b></span><br>После завершения сканирования вы можете использовать встроенную функцию обработки Creality Sermoon P1, чтобы создать итоговую 3D-модель из данных облака точек.')  # TM exact: sermoon-p1/legacy P9b2
# P9b3  sz6.0 B  (56.7, 123.3, 467.5, 168.3)
# EN: <span style="font-size:7.0px"><b>● Processing Flow (Operate on the screen) :</b></span> 1. Fusion: Fuse multiple frames of point cloud data collected during the scanning process into a complete point cloud. 2. Alignment: Multiple scans can be aligned into a complete model for result preview. 3. Meshing: Convert point cloud data into triangular mesh surfaces to generate the basic shape of the model. 4. Color Mapping (if applicable): If color information was captured during scanning, this step will map the color and texture onto the model surface.
t('P9b3', html='<span style="font-size:7px"><b>● Порядок обработки (на экране):</b></span><br>1. Fusion (Слияние): объединение нескольких кадров облака точек, собранных при сканировании, в единое облако точек.<br>2. Alignment (Выравнивание): несколько сканов можно совместить в единую модель для предпросмотра.<br>3. Meshing (Построение сетки): преобразование облака точек в треугольную полигональную сетку для создания базовой формы модели.<br>4. Color Mapping (Наложение цвета, если применимо): если при сканировании был захвачен цвет, на этом этапе цвет и текстура накладываются на поверхность модели.')  # TM exact: sermoon-p1/legacy P9b3
# P9b4  sz6.0  (114.6, 333.2, 466.0, 341.2)
# EN: For more detailed tutorials on model processing, please visit the Creality official Wiki. https://wiki.creality.com/3d-scanner
t('P9b4', html='Подробные инструкции по обработке модели смотрите на официальной Wiki Creality. https://wiki.creality.com/3d-scanner')  # TM exact: sermoon-p1/legacy P9b4

# ==================== PAGE 10 ====================
# P10b0  sz8.0 B  (55.8, 42.9, 423.1, 62.0)
# EN: <b>2.2 PC Connection Mode (Connect to Computer)</b> <span style="font-size:6.0px">Connect to your computer via USB or Wi-Fi and use CrealityScan 4 software for more advanced scan control and model processing.</span>
t('P10b0', size=6, html='<span style="font-size:8px"><b>2.2 Режим подключения к ПК (подключение к компьютеру)</b></span><br>Подключите сканер к компьютеру через USB или Wi-Fi и используйте ПО CrealityScan 4 для расширенного контроля сканирования и обработки моделей.')  # TM exact: sermoon-p1/legacy P10b0
# P10b1  sz6.0 B  (55.8, 69.9, 522.4, 98.0)
# EN: <span style="font-size:8.0px"><b>2.2.1 Software Preparation</b></span> ● Download the Software: Visit the Creality official Wiki software download page: https://wiki.creality.com/en/software/scan-software, find CrealityScan 4 software and download it.
t('P10b1', html='<span style="font-size:8px"><b>2.2.1 Подготовка ПО</b></span><br>● Загрузка ПО: перейдите на страницу загрузки ПО официальной Wiki Creality: https://wiki.creality.com/en/software/scan-software, найдите ПО CrealityScan 4 и загрузите его.')  # TM exact: sermoon-p1/legacy P10b1
# P10b2  sz6.0  (55.8, 297.8, 467.8, 332.7)
# EN: ● Install the Software: ○ Windows: Double-click the installer and follow the prompts to complete the installation. ○ macOS: After installation, please grant the 3D scanner read and write permissions to optimize point clouds and generate models when using the software .
t('P10b2', html='● Установка ПО:<br>○ Windows: дважды щёлкните установщик и следуйте подсказкам для завершения установки.<br>○ macOS: после установки предоставьте 3D-сканеру права на чтение и запись, чтобы оптимизировать облака точек и создавать модели при работе с ПО.')  # TM exact: sermoon-p1/legacy P10b2

# ==================== PAGE 11 ====================
# P11b0  sz8.0 B  (55.0, 44.7, 171.9, 55.3)
# EN: 2.2.2 Connecting the Scanner
t('P11b0', html='<b>2.2.2 Подключение сканера</b>')  # TM exact: sermoon-p1s P14b0
# P11b1  sz6.0 B  (55.0, 62.7, 300.7, 108.8)
# EN: <span style="font-size:8.0px"><b>Wired Connection (USB)</b></span> ● Insert the Type-C connector of the data cable into the scanner and tighten the screw. ● Insert the other end of the data cable (Type-C) into a USB 3.0 or higher port on your computer to ensure stable data transfer. ● In the pop-up window of Creality Sermoon P1, select "Scan Connection".
t('P11b1', html='<span style="font-size:8px"><b>Проводное подключение (USB)</b></span><br>● Вставьте разъём Type-C кабеля данных в сканер и затяните винт.<br>● Вставьте другой конец кабеля (Type-C) в порт USB 3.0 или выше на компьютере для стабильной передачи данных.<br>● Во всплывающем окне Creality Sermoon P1 выберите «Scan Connection» (Подключение для сканирования).')  # TM exact: sermoon-p1/legacy P11b1
# P11b2  sz6.0  (55.0, 205.4, 403.2, 213.3)
# EN: ● Open the CrealityScan 4 software on your computer, the software will automatically recognize and connect to the scanner.
t('P11b2', html='● Откройте ПО CrealityScan 4 на компьютере — оно автоматически распознает и подключит сканер.')  # TM exact: sermoon-p1/legacy P11b2

# ==================== PAGE 12 ====================
# P12b0  sz6.0 B  (56.7, 35.5, 398.5, 72.6)
# EN: <span style="font-size:8.0px"><b>Wireless Connection (Wi-Fi)</b></span> ● Step 1: Enable P1 Hotspot ○ On the Creality Sermoon P1 device screen, access the "Settings" menu, tap "Hotspot", and enable "Allow Others to Join" . ○ Record the hotspot name and password.
t('P12b0', html='<span style="font-size:8px"><b>Беспроводное подключение (Wi-Fi)</b></span><br>● Шаг 1: Включите точку доступа P1<br>○ На экране устройства Creality Sermoon P1 откройте меню «Settings» (Настройки), коснитесь «Hotspot» (Точка доступа) и включите «Allow Others to Join» (Разрешить подключение другим).<br>○ Запишите имя и пароль точки доступа.')  # TM exact: sermoon-p1/legacy P12b0
# P12b1  sz6.0  (56.7, 229.7, 441.1, 246.6)
# EN: ● Step 2: Connect Your Computer to the P1 Hotspot ○ In your computer's Wi-Fi settings, find the hotspot network name of the Creality Sermoon P1, click to connect, and enter the password.
t('P12b1', html='● Шаг 2: Подключите компьютер к точке доступа P1<br>○ В настройках Wi-Fi компьютера найдите имя сети точки доступа Creality Sermoon P1, нажмите для подключения и введите пароль.')  # TM exact: sermoon-p1/legacy P12b1

# ==================== PAGE 13 ====================
# P13b0  sz6.0  (63.3, 34.5, 404.8, 60.5)
# EN: ● Step 3: Software Connection ○ Open the CrealityScan 4 software on your computer. ○ In the software interface, the software will automatically identify and display the connected Creality Sermoon P1 device.
t('P13b0', html='● Шаг 3: Подключение ПО<br>○ Откройте ПО CrealityScan 4 на компьютере.<br>○ В интерфейсе ПО автоматически появится подключённое устройство Creality Sermoon P1.')  # TM exact: sermoon-p1/legacy P13b0
# P13b1  sz8.0 B  (56.7, 231.2, 462.7, 250.2)
# EN: <b>2.2.3 Start Scaning</b> <span style="font-size:6.0px">● In the CrealityScan 4 software, click "New Project", enter the "Project Name" in the pop-up window, select the "Folder Path", and then click "OK".</span>
t('P13b1', size=6, html='<span style="font-size:8px"><b>2.2.3 Начало сканирования</b></span><br>● В ПО CrealityScan 4 нажмите «New Project» (Новый проект), введите «Project Name» (Имя проекта) во всплывающем окне, выберите «Folder Path» (Путь к папке) и нажмите «OK».')  # TM exact: sermoon-p1/legacy P13b1

# ==================== PAGE 14 ====================
# P14b0  sz6.0  (63.3, 34.5, 367.2, 42.5)
# EN: ● Select the appropriate scan mode and related settings based on the features of the object being scanned.
t('P14b0', html='● Выберите подходящий режим сканирования и связанные настройки в зависимости от особенностей сканируемого объекта.')  # TM exact: sermoon-p1/legacy P14b0
# P14b1  sz6.0  (56.7, 230.2, 236.1, 238.1)
# EN: ● Click the "Preview" button to enter the scan preview interface.
t('P14b1', html='● Нажмите кнопку «Preview» (Предпросмотр), чтобы перейти в интерфейс предпросмотра сканирования.')  # TM exact: sermoon-p1/legacy P14b1

# ==================== PAGE 15 ====================
# P15b0  sz6.0  (63.3, 34.5, 542.8, 49.5)
# EN: ● Adjust the Scanning Distance: Move the scanner to adjust its distance from the scanned object. When the distance indicator bar on the software interface is in the green "optimal" range, it indicates that the current scanning distance is ideal for scanning.
t('P15b0', html='● Регулировка расстояния сканирования: перемещайте сканер, регулируя его расстояние до объекта. Когда индикатор расстояния в интерфейсе ПО находится в зелёной зоне «optimal» (Оптимально), текущее расстояние идеально для сканирования.')  # TM exact: sermoon-p1/legacy P15b0
# P15b1  sz6.0  (59.2, 233.3, 562.1, 250.3)
# EN: ● Start Scanning: Short press the Start/Pause button on the scanner, or click the [Start] button in the software interface. Keep the scanner aimed at the object, move it steadily and slowly, and scan the object from all angles.
t('P15b1', html='● Начало сканирования: коротко нажмите кнопку «Старт/Пауза» на сканере или нажмите кнопку «Start» (Старт) в интерфейсе ПО. Держите сканер направленным на объект, перемещайте его плавно и медленно, сканируя со всех сторон.')  # TM exact: sermoon-p1/legacy P15b1
# P15b2  sz6.0  (59.2, 260.3, 542.3, 277.3)
# EN: ● Complete Scanning: Once the data acquisition is complete, press and hold the Start/Pause button on the scanner for more than 2 seconds, or click "Finish" in the software interface. The scanned point cloud data will be automatically displayed in the software.
t('P15b2', html='● Завершение сканирования: после сбора данных нажмите и удерживайте кнопку «Старт/Пауза» более 2 секунд или нажмите «Finish» (Готово) в интерфейсе ПО. Данные облака точек автоматически отобразятся в ПО.')  # TM exact: sermoon-p1/legacy P15b2

# ==================== PAGE 16 ====================
# P16b0  sz8.0 B  (68.0, 35.5, 512.0, 54.6)
# EN: <b>2.2.4 Model Processing</b> <span style="font-size:6.0px">After the scan is completed, you need to use the post-processing function of CrealityScan 4 software to generate the final 3D model from the point cloud data.</span>
t('P16b0', size=6, html='<span style="font-size:8px"><b>2.2.4 Обработка модели</b></span><br>После завершения сканирования используйте функцию постобработки ПО CrealityScan 4, чтобы создать итоговую 3D-модель из данных облака точек.')  # TM exact: sermoon-p1/legacy P16b0
# P16b1  sz6.0  (68.0, 64.7, 574.8, 81.6)
# EN: ● One-Click Process: For beginner users, the software's "One-Click Process" function can be used, which will automatically complete point cloud fusion, meshing, and color mapping (if applicable).
t('P16b1', html='● Обработка в один клик: для начинающих можно использовать функцию «One-Click Process» (Обработка в один клик), которая автоматически выполнит слияние облака точек, полигонизацию и наложение цвета (если применимо).')  # TM exact: sermoon-p1/legacy P16b1
# P16b2  sz6.0  (68.0, 91.7, 478.9, 135.6)
# EN: ● Manual Processing Procedure (recommended): 1. Fusion: Fuse multiple frames of point cloud data collected during the scanning process into a complete point cloud. 2. Alignment: Multiple scans can be aligned into a complete model for result preview. 3. Meshing: Convert point cloud data into triangular mesh surfaces to generate the basic shape of the model. 4. Color Mapping (if applicable): If color information was captured during scanning, this step will map the color and texture onto the model surface.
t('P16b2', html='● Ручная процедура обработки (рекомендуется):<br>1. Fusion (Слияние): объединение нескольких кадров облака точек в единое облако точек.<br>2. Alignment (Выравнивание): несколько сканов можно совместить в единую модель для предпросмотра.<br>3. Meshing (Построение сетки): преобразование облака точек в треугольную сетку для создания базовой формы модели.<br>4. Color Mapping (Наложение цвета, если применимо): если при сканировании был захвачен цвет, цвет и текстура накладываются на поверхность модели.')  # TM exact: sermoon-p1/legacy P16b2
# P16b3  sz6.0  (140.5, 328.4, 483.0, 336.4)
# EN: For more detailed model processing tutorials, please visit the official Creality Wiki: https://wiki.creality.com/3d-scanner
t('P16b3', html='Подробные инструкции по обработке модели смотрите на официальной Wiki Creality: https://wiki.creality.com/3d-scanner')  # TM exact: sermoon-p1/legacy P16b3

# ==================== PAGE 17 ====================
# P17b3  sz12.0 B  (156.4, 41.6, 453.1, 57.5)
# EN: 3. DETAILED EXPLANATION OF SCAN MODES
t('P17b3', html='3. ПОДРОБНОЕ ОПИСАНИЕ РЕЖИМОВ СКАНИРОВАНИЯ')  # TM exact: sermoon-p1s P19b3
# P17b0  sz6.0 B  (50.1, 68.4, 515.3, 157.4)
# EN: <span style="font-size:7.0px"><b>3.1 Blue Laser Mode</b></span> Suitable for scanning objects requiring high accuracy and rich details, it usually needs to be used with markers. ● Cross Line Laser: ○ Features: Fast scanning speed and high efficiency. ○ Applicable scenarios: Scanning large objects. It is necessary to attach markers directly to the object's surface. ● Parallel Line Laser: ○ Features: Best details. ○ Applicable scenarios: For detailed scanning of objects, resulting in richer model details . If the object is small, markers can be placed on the table around the object. ● Single Line Laser: ○ Features: Excellent at capturing hard-to-reach areas such as deep holes and grooves. ○ Applicable scenarios: Supplemental scanning of objects with deep hole features.
t('P17b0', html='<span style="font-size:7px"><b>3.1 Режим синего лазера</b></span><br>Подходит для сканирования объектов, требующих высокой точности и детализации; обычно используется с маркерами.<br>● Лазер перекрёстных линий:<br>○ Особенности: высокая скорость и эффективность сканирования.<br>○ Применение: сканирование крупных объектов. Маркеры необходимо наносить прямо на поверхность объекта.<br>● Лазер параллельных линий:<br>○ Особенности: лучшая детализация.<br>○ Применение: детальное сканирование объектов с богатой детализацией модели. Для малых объектов маркеры можно разместить на столе вокруг объекта.<br>● Лазер одиночной линии:<br>○ Особенности: отлично захватывает труднодоступные участки, такие как глубокие отверстия и канавки.<br>○ Применение: дополнительное сканирование объектов с глубокими отверстиями.')  # TM exact: sermoon-p1/legacy P17b0
# P17b1  sz6.0 B  (50.1, 164.4, 547.5, 205.4)
# EN: <span style="font-size:7.0px"><b>Tips:</b></span> ● Real-Time Resolution: The smaller the resolution, the finer the model. However, this will occupy more computer memory and may affect scanning smoothness. Please select according to your computer performance and model requirements. ● Alignment: If you need to scan multiple sides of an object (such as the front and back), you can scan them in multiple steps and then use the software's "Alignment" function to combine them into a complete model.
t('P17b1', html='<span style="font-size:7px"><b>Советы:</b></span><br>● Разрешение в реальном времени: чем меньше разрешение, тем детальнее модель. Однако это занимает больше памяти компьютера и может влиять на плавность сканирования. Выбирайте в зависимости от производительности компьютера и требований к модели.<br>● Выравнивание: если нужно отсканировать несколько сторон объекта (например, перёд и зад), сканируйте их в несколько этапов, а затем используйте функцию «Alignment» (Выравнивание) в ПО, чтобы объединить их в единую модель.')  # TM exact: sermoon-p1/legacy P17b1
# P17b2  sz6.0 B  (50.1, 212.4, 404.8, 253.4)
# EN: <span style="font-size:7.0px"><b>3.2 Infrared Mode</b></span> Suitable for scanning faces, bodies , sculptures , or other objects with rich features, usually without the need to attach markers. ● Features: Safe, fast, invisible light, and harmless to human eyes . ● Applicable scenarios: Face scanning, cultural relic protection, medical rehabilitation, etc. ● Infrared mode also supports "Texture" tracking and "Marker" tracking to meet different needs.
t('P17b2', html='<span style="font-size:7px"><b>3.2 Инфракрасный режим</b></span><br>Подходит для сканирования лиц, тел, скульптур и других объектов с богатой детализацией; обычно без необходимости наносить маркеры.<br>● Особенности: безопасный, быстрый, невидимый свет, безвреден для глаз человека.<br>● Применение: сканирование лиц, сохранение культурных ценностей, медицинская реабилитация и т. д.<br>● Инфракрасный режим также поддерживает отслеживание по текстуре «Texture» и по маркерам «Marker» для разных задач.')  # TM exact: sermoon-p1/legacy P17b2
# P17b4  sz12.0 B  (232.7, 271.7, 376.9, 287.6)
# EN: 4. OTHER FUNCTIONS
t('P17b4', html='4. ПРОЧИЕ ФУНКЦИИ')  # TM exact: sermoon-p1s P19b4
# P17b5  sz6.0 B  (47.7, 297.1, 562.6, 324.1)
# EN: <span style="font-size:7.0px"><b>4.1 Calibration</b></span> If you notice a decrease in scanning accuracy or if the scanner has not been used for an long time, calibration is recommended. Please use the included "High-Precision Glass Calibration Board" and follow the on-screen instructions on your Creality Sermoon P1 device to restore the scanner's factory accuracy.
t('P17b5', html='<span style="font-size:7px"><b>4.1 Калибровка</b></span><br>Если вы заметили снижение точности сканирования или сканер долго не использовался, рекомендуется калибровка. Используйте входящую в комплект «Высокоточную стеклянную калибровочную плиту» и следуйте инструкциям на экране устройства Creality Sermoon P1, чтобы восстановить заводскую точность сканера.')  # TM exact: sermoon-p1/legacy P17b5
# P17b6  sz6.0 B  (47.7, 333.1, 560.0, 360.1)
# EN: <span style="font-size:7.0px"><b>4.2 System Upgrade</b></span> Creality releases system updates periodically to optimize performance and add new features. Please keep your Creality Sermoon P1 device up to the latest system version and upgrade as prompted for the best user experience.
t('P17b6', html='<span style="font-size:7px"><b>4.2 Обновление системы</b></span><br>Creality периодически выпускает обновления системы для оптимизации работы и добавления новых функций. Поддерживайте устройство Creality Sermoon P1 в актуальной версии системы и обновляйте по запросу для наилучшего опыта использования.')  # TM exact: sermoon-p1/legacy P17b6
# P17b7  sz6.0 B  (47.7, 369.1, 556.4, 396.1)
# EN: <span style="font-size:7.0px"><b>4.3 File Transfer</b></span> Select the project you want to share from the "Recent Projects" list , tap the "Share" button in the “...” icon at the top left corner, and follow the on-screen instructions to complete the file transfer.
t('P17b7', html='<span style="font-size:7px"><b>4.3 Передача файлов</b></span><br>Выберите проект в списке «Recent Projects» (Недавние проекты), коснитесь значка «...» в левом верхнем углу, затем «Share» (Поделиться) и следуйте инструкциям на экране.')  # TM exact: sermoon-p1s P19b7

# ==================== PAGE 18 ====================
# P18b0  sz12.0 B  (249.2, 38.1, 374.6, 54.0)
# EN: 5. SPECIFICATIONS
t('P18b0', html='5. ХАРАКТЕРИСТИКИ')  # TM exact: sermoon-p1s P20b0
# P18b1  sz7.0 B  (57.2, 58.4, 146.9, 67.7)
# EN: 5.1 Hardware Parameters
t('P18b1', html='<b>5.1 Аппаратные параметры</b>')  # TM exact: sermoon-p1s P20b1
# P18b2  sz6.5  (285.5, 78.0, 349.2, 86.6)
# EN: Creality Sermoon P1
t('P18b2', html='Creality Sermoon P1')  # TM exact: sermoon-p1/legacy P18b2
# P18b29 +1  sz6.0  (413.4, 93.6, 476.8, 108.1)
# EN: Close-Range Infrared Structured Light
t('P18b29', merge=['P18b30'], html='Структурированный ИК-свет (ближний)')
# P18b31 +1  sz6.0  (496.4, 93.6, 558.5, 108.1)
# EN: Long-Range Infrared Structured Light
t('P18b31', merge=['P18b32'], html='Структурированный ИК-свет (дальний)')
# P18b26.1  sz6.0  (169.3, 96.7, 232.8, 104.7)
# EN: Single Blue Laser Line
t('P18b26.1', html='Одна синяя линия')
# P18b26.2  sz6.0  (243.8, 96.7, 318.8, 104.7)
# EN: 7 Parallel Blue Laser Lines
t('P18b26.2', html='7 параллельных линий')
# P18b26.3  sz6.0  (325.8, 96.7, 399.4, 104.7)
# EN: 22 Cross Blue Laser Lines
# TM 92% (sermoon-p1s P20b34.3): 34 Cross Blue Laser Lines
#   → 34 перекрёстные синие линии
t('P18b26.3', html='22 перекрёстные линии')
# P18b3  sz6.0  (61.5, 97.4, 105.9, 105.3)
# EN: Scanning Mode
t('P18b3', html='Режим сканирования')  # TM exact: sermoon-p1s P20b5
# P18b18.1  sz6.0  (258.8, 114.7, 304.3, 122.7)
# EN: Up to 0.02mm[1]
# TM 89% (sermoon-p1s P20b35): Up to 0.02mm
#   → До 0.02 мм
t('P18b18.1', html='До 0.02 мм<span style="font-size:3.5px">[1]</span>')
# P18b18.2  sz6.0  (461.4, 114.7, 510.5, 122.7)
# EN: Up to 0.075mm[1]
# TM 90% (sermoon-p1s P20b18): Up to 0.075mm
#   → До 0.075 мм
t('P18b18.2', html='До 0.075 мм<span style="font-size:3.5px">[1]</span>')
# P18b4  sz6.0  (61.5, 115.9, 87.5, 123.8)
# EN: Accuracy
t('P18b4', html='Точность')  # TM exact: sermoon-p1/legacy P18b4
# P18b5  sz6.0  (61.5, 134.4, 120.0, 142.3)
# EN: Volumetric Accuracy
t('P18b5', html='Объёмная точность')  # TM exact: sermoon-p1s P20b7
# P18b19  sz6.0  (253.2, 134.6, 310.0, 142.6)
# EN: 0.02mm+0.06mm/m
# TM 82% (sermoon-p1s P20b36): 0.02mm + 0.08 mm /m
#   → 0.02 мм + 0.08 мм/м
t('P18b19', html='0.02 мм + 0.06 мм/м')
# P18b24  sz6.0  (457.5, 134.6, 514.4, 142.6)
# EN: 0.075mm+0.1mm/m
t('P18b24', html='0.075 мм + 0.1 мм/м')  # TM exact: sermoon-p1s P20b19
# P18b27.1  sz6.0  (166.4, 152.8, 234.7, 160.8)
# EN: 61,000 measurements/s
t('P18b27.1', html='61 000 замеров/с')
# P18b27.2  sz6.0  (245.5, 152.8, 317.4, 160.8)
# EN: 430,000 measurements/s
t('P18b27.2', html='430 000 замеров/с')
# P18b27.3  sz6.0  (325.1, 152.8, 402.2, 160.8)
# EN: 1,044,000 measurements/s
t('P18b27.3', html='1 044 000 замеров/с')
# P18b6  sz6.0  (61.5, 152.9, 141.9, 160.8)
# EN: Scanning Rate (Standalone)
t('P18b6', html='Скорость замеров (автономно)')  # TM exact: sermoon-p1s P20b8
# P18b25  sz6.0  (441.9, 153.3, 519.1, 161.2)
# EN: 3,440,000 measurements/s
t('P18b25', html='3 440 000 замеров/с')
# P18b28.1  sz6.0  (164.1, 171.3, 236.0, 179.3)
# EN: 102,000 measurements/s
t('P18b28.1', html='102 000 замеров/с')
# P18b28.2  sz6.0  (245.0, 171.3, 316.9, 179.3)
# EN: 716,000 measurements/s
t('P18b28.2', html='716 000 замеров/с')
# P18b28.3  sz6.0  (324.6, 171.3, 401.7, 179.3)
# EN: 1,740,000 measurements/s
t('P18b28.3', html='1 740 000 замеров/с')
# P18b28.4  sz6.0  (441.9, 171.3, 519.1, 179.3)
# EN: 6,881,000 measurements/s
t('P18b28.4', html='6 881 000 замеров/с')
# P18b7  sz6.0  (61.5, 171.4, 151.9, 179.3)
# EN: Scanning Rate (PC Connection)
t('P18b7', html='Скорость замеров (ПК)')  # TM exact: sermoon-p1s P20b9
# P18b20.1  sz6.0  (266.9, 189.4, 296.3, 197.4)
# EN: 0.05-2mm
t('P18b20.1', html='0.05–2 мм')  # TM exact: sermoon-p1s P20b29
# P18b20.2  sz6.0  (473.0, 189.4, 498.9, 197.4)
# EN: 0.1-2mm
t('P18b20.2', html='0.1–2 мм')  # TM exact: sermoon-p1s P20b22
# P18b8  sz6.0  (61.5, 189.9, 101.9, 197.8)
# EN: 3D Resolution
t('P18b8', html='3D-разрешение')  # TM exact: sermoon-p1s P20b10
# P18b21.1  sz6.0  (264.6, 208.1, 298.6, 216.1)
# EN: Up to 60fps
t('P18b21.1', html='До 60 fps')  # TM exact: sermoon-p1s P20b30
# P18b21.2  sz6.0  (469.0, 208.1, 502.9, 216.1)
# EN: Up to 15fps
# TM 87% (sermoon-p1s P20b31): Up to 100fps
#   → До 100 fps
t('P18b21.2', html='До 15 fps')
# P18b9  sz6.0  (61.5, 208.4, 146.7, 216.3)
# EN: Scanning Speed (Standalone)
t('P18b9', html='Скорость сканирования (автономно)')  # TM exact: sermoon-p1s P20b11
# P18b22.1  sz6.0  (262.8, 226.7, 300.4, 234.6)
# EN: Up to 100fps
t('P18b22.1', html='До 100 fps')  # TM exact: sermoon-p1s P20b31
# P18b22.2  sz6.0  (469.0, 226.7, 502.9, 234.6)
# EN: Up to 30fps
t('P18b22.2', html='До 30 fps')  # TM exact: sermoon-p1s P20b24
# P18b10  sz6.0  (61.5, 226.9, 156.7, 234.8)
# EN: Scanning Speed (PC Connection)
t('P18b10', html='Скорость сканирования (ПК)')  # TM exact: sermoon-p1s P20b12
# P18b23.1  sz6.0  (253.7, 244.2, 309.4, 252.2)
# EN: 5mm x 5mm x 5mm
t('P18b23.1', html='5 × 5 × 5 мм')  # TM exact: sermoon-p1s P20b32
# P18b23.2  sz6.0  (447.3, 244.2, 524.6, 252.2)
# EN: 150mm x 150mm x 150mm
t('P18b23.2', html='150 × 150 × 150 мм')  # TM exact: sermoon-p1s P20b25
# P18b11  sz6.0  (61.5, 245.4, 112.0, 253.3)
# EN: Min. Scan Volume
t('P18b11', html='Мин. объём сканирования')  # TM exact: sermoon-p1s P20b13
# P18b33  sz6.0  (184.0, 261.0, 258.5, 285.9)
# EN: 85mm*105mm @160mm 135mm*130mm @200mm 265mm*200mm @300mm
t('P18b33', html='85 × 105 мм на 160 мм<br>135 × 130 мм на 200 мм<br>265 × 200 мм на 300 мм')
# P18b36  sz6.0  (279.0, 261.0, 353.5, 277.4)
# EN: 310mm*265mm @400mm 380mm*365mm @550mm
t('P18b36', html='310 × 265 мм на 400 мм<br>380 × 365 мм на 550 мм')
# P18b34  sz6.0  (407.2, 261.4, 477.5, 286.4)
# EN: 135mm*130mm @200mm 265mm*200mm @300mm 310mm*265mm @400mm
t('P18b34', html='135 × 130 мм на 200 мм<br>265 × 200 мм на 300 мм<br>310 × 265 мм на 400 мм')
# P18b35.2  sz5.7  (488.4, 261.4, 559.5, 286.4)
# EN: 689mm×375mm@500mm 1245mm×754mm@1000mm 1450mm*1020mm@1200mm
t('P18b35.2', html='689 × 375 мм на 500 мм<br>1245 × 754 мм на 1000 мм<br>1450 × 1020 мм на 1200 мм')
# P18b35.1  sz5.7  (61.7, 269.5, 124.2, 277.4)
# EN: Single Capture Range
t('P18b35.1', html='Диапазон одного захвата')  # TM exact: sermoon-p1s P20b14
# P18b39.1  sz6.0  (183.7, 292.4, 218.8, 300.4)
# EN: 200-550mm
t('P18b39.1', html='200–550 мм')
# P18b39.2  sz6.0  (261.3, 292.4, 307.0, 300.4)
# EN: 160mm-400mm
# TM 78% (sermoon-p1s P20b26): 170mm-1200mm
#   → 170–1200 мм
t('P18b39.2', html='160–400 мм')
# P18b39.3  sz6.0  (345.6, 292.4, 380.7, 300.4)
# EN: 200-550mm
t('P18b39.3', html='200–550 мм')
# P18b42.1  sz6.0  (420.2, 292.4, 465.8, 300.4)
# EN: 170mm-400mm
# TM 87% (sermoon-p1s P20b26): 170mm-1200mm
#   → 170–1200 мм
t('P18b42.1', html='170–400 мм')
# P18b42.2  sz6.0  (499.4, 292.4, 548.7, 300.4)
# EN: 200mm-1200mm
# TM 83% (sermoon-p1s P20b26): 170mm-1200mm
#   → 170–1200 мм
t('P18b42.2', html='200–1200 мм')
# P18b12  sz6.0  (61.5, 293.3, 110.5, 301.3)
# EN: Working Distance
t('P18b12', html='Рабочее расстояние')  # TM exact: sermoon-p1s P20b15
# P18b37  sz6.0  (358.4, 311.6, 367.9, 319.6)
# EN: Yes
t('P18b37', html='Да')  # TM exact: sermoon-p1s P22b13
# P18b13  sz6.0  (61.5, 311.8, 102.7, 319.8)
# EN: Color Mapping
t('P18b13', html='Наложение цвета')  # TM exact: sermoon-p1s P20b16
# P18b14  sz6.0  (61.5, 330.3, 107.5, 338.3)
# EN: Alignment Mode
t('P18b14', html='Режим выравнивания')  # TM exact: sermoon-p1s P21b1.1
# P18b38.1  sz6.0  (248.4, 330.3, 314.8, 338.2)
# EN: Marker / Global Marker
t('P18b38.1', html='Маркер / Глобальный маркер')
# P18b38.2  sz6.0  (422.5, 330.3, 549.4, 338.2)
# EN: Marker / Global Marker / Geometry / Texture
t('P18b38.2', html='Маркер / Глобальный маркер / Геометрия / Текстура')
# P18b15  sz6.0  (61.5, 348.8, 102.1, 356.8)
# EN: Color Fill Light
t('P18b15', html='Цветная подсветка')  # TM exact: sermoon-p1/legacy P18b15
# P18b41  sz6.0  (342.0, 349.0, 384.2, 356.9)
# EN: 12 White LEDs
# TM 88% (sermoon-p1s P21b0): 8 White LEDs
#   → 8 белых светодиодов
t('P18b41', html='12 белых светодиодов')
# P18b40.1  sz6.0  (180.4, 367.2, 233.0, 375.2)
# EN: Below 100,000 lux
# TM 94% (sermoon-p1s P21b30): Below 110,000 lux
#   → До 110 000 люкс
t('P18b40.1', html='До 100 000 люкс')
# P18b40.2  sz6.0  (262.9, 367.2, 311.9, 375.2)
# EN: Below 50,000 lux
# TM 91% (sermoon-p1s P21b30): Below 110,000 lux
#   → До 110 000 люкс
t('P18b40.2', html='До 50 000 люкс')
# P18b40.3  sz6.0  (342.0, 367.2, 394.6, 375.2)
# EN: Below 100,000 lux
# TM 94% (sermoon-p1s P21b30): Below 110,000 lux
#   → До 110 000 люкс
t('P18b40.3', html='До 100 000 люкс')
# P18b40.4  sz6.0  (457.7, 367.2, 506.8, 375.2)
# EN: Below 30,000 lux
# TM 91% (sermoon-p1s P21b30): Below 110,000 lux
#   → До 110 000 люкс
t('P18b40.4', html='До 30 000 люкс')
# P18b16  sz6.0  (61.5, 367.3, 112.3, 375.3)
# EN: Outdoor Scanning
t('P18b16', html='Сканирование на улице')  # TM exact: sermoon-p1s P21b4
# P18b17  sz6.0  (61.5, 385.8, 155.8, 393.8)
# EN: Marker Recognition Enhancement
t('P18b17', html='Улучшение распознавания маркеров')  # TM exact: sermoon-p1/legacy P18b17
# P18b43  sz6.0  (344.6, 386.0, 382.5, 393.9)
# EN: 12 Blue LEDs
t('P18b43', html='12 синих светодиодов')

# ==================== PAGE 19 ====================
# P19b11  sz6.0  (65.1, 29.2, 100.8, 37.1)
# EN: Laser Safety
t('P19b11', html='Лазерная безопасность')  # TM exact: sermoon-p1s P21b6
# P19b0.1  sz6.0  (256.6, 29.7, 306.6, 37.7)
# EN: Class II (eye safe)
t('P19b0.1', html='Класс II (безопасен для глаз)')  # TM exact: sermoon-p1s P21b32
# P19b0.2  sz6.0  (442.4, 29.7, 490.6, 37.7)
# EN: Class I (eye safe)
t('P19b0.2', html='Класс I (безопасен для глаз)')  # TM exact: sermoon-p1s P21b36
# P19b24.1  sz6.0  (295.7, 47.1, 391.0, 55.0)
# EN: Qualcomm CPU, 8 core, 3.36 GHz
t('P19b24.1', html='Qualcomm CPU, 8 ядер, 3.36 ГГц')
# P19b24.3  sz6.0  (407.1, 47.1, 456.1, 55.0)
# EN: GPU, Adreno 740
t('P19b24.3', html='GPU Adreno 740')
# P19b12  sz6.0  (65.1, 47.7, 93.2, 55.6)
# EN: Processor
t('P19b12', html='Процессор')  # TM exact: sermoon-p1s P21b10
# P19b25  sz6.0  (353.2, 65.6, 398.6, 73.5)
# EN: 24GB LPDDR5X
# TM 83% (sermoon-p1s P21b23): 16GB LPDDR5X
#   → 16 ГБ LPDDR5X
t('P19b25', html='24 ГБ LPDDR5X')
# P19b13  sz6.0  (65.1, 66.2, 102.0, 74.1)
# EN: Built-in RAM
t('P19b13', html='Встроенная ОЗУ')  # TM exact: sermoon-p1s P21b11
# P19b26  sz6.0  (354.4, 84.1, 397.4, 92.0)
# EN: 256GB UFS 4.0
t('P19b26', html='256 ГБ UFS 4.0')  # TM exact: sermoon-p1s P21b24
# P19b14  sz6.0  (65.1, 84.7, 111.0, 92.6)
# EN: Built-in Storage
t('P19b14', html='Встроенная память')  # TM exact: sermoon-p1s P21b12
# P19b27  sz6.0  (342.5, 102.6, 409.3, 110.5)
# EN: 6-inch HD Touchscreen
t('P19b27', html='6-дюймовый сенсорный HD-экран')  # TM exact: sermoon-p1s P21b25
# P19b15  sz6.0  (65.1, 103.2, 107.2, 111.1)
# EN: Display Screen
t('P19b15', html='Экран')  # TM exact: sermoon-p1/legacy P19b15
# P19b28  sz6.0  (346.6, 121.1, 405.3, 129.0)
# EN: PD3.0 Fast Charging
t('P19b28', html='Быстрая зарядка PD3.0')  # TM exact: sermoon-p1s P21b28
# P19b16  sz6.0  (65.1, 121.7, 88.1, 129.6)
# EN: Charger
t('P19b16', html='Зарядное устройство')  # TM exact: sermoon-p1/legacy P19b16
# P19b29  sz6.0  (371.1, 139.6, 380.7, 147.5)
# EN: Yes
t('P19b29', html='Да')  # TM exact: sermoon-p1s P22b13
# P19b17  sz6.0  (65.1, 140.2, 114.3, 148.1)
# EN: Wireless PC Scan
t('P19b17', html='Беспроводное сканирование с ПК')  # TM exact: sermoon-p1s P22b5
# P19b30  sz6.0  (296.9, 158.1, 454.9, 166.0)
# EN: Standalone Mode / Wireless PC Mode / Wired PC Mode
t('P19b30', html='Автономный / Беспроводной ПК / Проводной ПК')  # TM exact: sermoon-p1/legacy P19b30
# P19b18  sz6.0  (65.1, 158.7, 98.0, 166.6)
# EN: Work Mode
t('P19b18', html='Режим работы')  # TM exact: sermoon-p1s P22b6
# P19b31  sz6.0  (366.9, 176.6, 384.9, 184.5)
# EN: WiFi 7
# TM 92% (sermoon-p1s P22b16): Wi-Fi 7
#   → Wi-Fi 7
t('P19b31', html='Wi-Fi 7')
# P19b19  sz6.0  (65.1, 177.2, 77.8, 185.1)
# EN: WiFi
t('P19b19', html='Wi-Fi')
# P19b32  sz6.0  (368.7, 195.1, 383.1, 203.0)
# EN: 830g
t('P19b32', html='830 г')
# P19b20  sz6.0  (65.1, 195.7, 106.5, 203.6)
# EN: Device Weight
t('P19b20', html='Вес устройства')  # TM exact: sermoon-p1s P21b7
# P19b33  sz6.0  (336.0, 213.6, 415.8, 221.5)
# EN: 209 mm × 129 mm × 53 mm
# TM 98% (sermoon-p1s P21b18): 209mm × 129 mm × 53 mm
#   → 209 × 129 × 53 мм
t('P19b33', html='209 × 129 × 53 мм')
# P19b21  sz6.0  (65.1, 214.1, 98.1, 222.1)
# EN: Dimensions
t('P19b21', html='Габариты')  # TM exact: sermoon-p1s P21b8
# P19b34  sz6.0  (320.0, 232.1, 431.8, 240.0)
# EN: High-Precision Glass Calibration Board
t('P19b34', html='Высокоточная стеклянная калибровочная плита')  # TM exact: sermoon-p1s P21b19
# P19b22  sz6.0  (65.1, 232.6, 115.5, 240.6)
# EN: Calibration Board
t('P19b22', html='Калибровочная плита')  # TM exact: sermoon-p1s P21b9
# P19b35  sz6.0  (350.0, 250.6, 401.8, 258.5)
# EN: Windows / macOS
t('P19b35', html='Windows / macOS')  # TM exact: sermoon-p1s P22b17
# P19b23  sz6.0  (65.1, 251.1, 120.4, 259.1)
# EN: PC System Support
t('P19b23', html='Поддержка ОС на ПК')  # TM exact: sermoon-p1s P22b8
# P19b9  sz6.0  (392.1, 267.0, 541.8, 305.0)
# EN: Minimum Requirements: OS: Win10/11 (64-bit) CPU: Intel i7-Gen7 Dedicated Graphics Card: NVIDIA 1060 (6GB VRAM) RAM: ≥16GB
t('P19b9', html='Минимальные требования:<br>ОС: Win10/11 (64-бит)<br>CPU: Intel i7-Gen7<br>Видеокарта: NVIDIA 1060 (6 ГБ VRAM)<br>ОЗУ: ≥16 ГБ')  # TM exact: sermoon-p1/legacy P19b9
# P19b7  sz6.0  (185.7, 267.1, 363.6, 305.1)
# EN: Recommended Configuration: OS: Win10/11 (64-bit) CPU: Intel i7 13th Gen or above Dedicated Graphics Card: NVIDIA 4060 or higher (8GB VRAM) RAM: ≥64GB
t('P19b7', html='Рекомендуемая конфигурация:<br>ОС: Win10/11 (64-бит)<br>CPU: Intel i7 13-го поколения или выше<br>Видеокарта: NVIDIA 4060 или выше (8 ГБ VRAM)<br>ОЗУ: ≥64 ГБ')  # TM exact: sermoon-p1/legacy P19b7
# P19b1  sz6.0  (65.1, 297.1, 136.9, 312.5)
# EN: Computer Configuration Requirements
t('P19b1', html='Требования к конфигурации компьютера')  # TM exact: sermoon-p1/legacy P19b1
# P19b10  sz6.0  (392.1, 312.0, 435.2, 335.0)
# EN: OS: macOS 12 CPU: Apple M1 RAM: ≥16GB
t('P19b10', html='ОС: macOS 12<br>CPU: Apple M1<br>ОЗУ: ≥16 ГБ')  # TM exact: sermoon-p1/legacy P19b10
# P19b8  sz6.0  (185.7, 312.1, 253.5, 335.1)
# EN: OS: macOS 14 or above CPU: Apple M3/M4 /M5 RAM: ≥32GB
t('P19b8', html='ОС: macOS 14 или выше<br>CPU: Apple M3/M4/M5<br>ОЗУ: ≥32 ГБ')  # TM exact: sermoon-p1/legacy P19b8
# P19b2  sz6.0  (65.1, 346.0, 131.9, 354.0)
# EN: Operating Temperature
t('P19b2', html='Рабочая температура')  # TM exact: sermoon-p1s P22b10
# P19b5  sz6.0  (341.4, 346.0, 380.5, 354.0)
# EN: -10°C to 40°C
t('P19b5', html='от −10 °C до 40 °C')  # TM exact: sermoon-p1s P22b0
# P19b3  sz6.0  (65.1, 364.5, 122.2, 372.5)
# EN: Operating Humidity
t('P19b3', html='Рабочая влажность')  # TM exact: sermoon-p1s P22b11
# P19b6  sz6.0  (345.5, 364.5, 376.4, 372.5)
# EN: 10-90%RH
t('P19b6', html='10–90 % RH')  # TM exact: sermoon-p1s P22b18
# P19b4  sz6.0  (65.1, 381.8, 532.8, 389.8)
# EN: [1] Accuracy is evaluated in laboratory conditions and actual results may be affected by operating environments such as vibration, temperature, and other factors.
t('P19b4', html='[1] Точность оценивается в лабораторных условиях; фактический результат может зависеть от условий эксплуатации, таких как вибрация, температура и др.')  # TM exact: sermoon-p1s P22b12

# ==================== PAGE 20 ====================
# P20b6  sz12.0 B  (250.9, 43.6, 371.7, 59.5)
# EN: 6. SAFETY NOTICE
t('P20b6', html='6. МЕРЫ ПРЕДОСТОРОЖНОСТИ')
# P20b7 +2  sz6.0  (56.7, 70.9, 357.7, 98.8)
# EN: About the Creality Sermoon P1 3D Scanner ● Please do not disassemble or assemble the equipment yourself. ● Please use the dedicated accessories included with the product, such as charger and calibration board.
# TM 95% (sermoon-p1s P23b7): About the Creality Sermoon P1S 3D Scanner ● Please do not disassemble or assemble the equipment yourself. ● Please use the dedicated accessories included with the product, such as calibration plates.
#   → О 3D-сканере Creality Sermoon P1S<br>● Не разбирайте и не собирайте оборудование самостоятельно.<br>● Используйте только фирменные принадлежности из комплекта, например калибровочную плиту.
t('P20b7', merge=['P20b8', 'P20b9'], html='О 3D-сканере Creality Sermoon P1<br>● Не разбирайте и не собирайте оборудование самостоятельно.<br>● Используйте только фирменные принадлежности из комплекта, например зарядное устройство и калибровочную плиту.')
# P20b10  sz8.0 B  (56.7, 108.8, 147.6, 119.4)
# EN: 6.1 Usage Instructions
t('P20b10', html='<b>6.1 Указания по эксплуатации</b>')  # TM exact: sermoon-p1s P23b10
# P20b11 +4  sz6.0  (56.7, 120.9, 567.4, 168.9)
# EN: Please note the following points, otherwise it may cause equipment damage or machine malfunction. ● Please avoid significant vibrations and impacts when using this product. The Creality Sermoon P1 3D scanner is a high-precision device with a delicate internal structure; severe vibrations or impacts may damage the structure and cause damage to the optical components. ● Please use this device at the recommended temperature and humidity. ● Please ensure the usage environment is suitable, and when using a wired connection, ensure the cable connector is intact.
# TM 99% (sermoon-p1s P23b11): Please note the following points, otherwise it may lead to equipment damage or machine malfunction. ● Please avoid significant vibrations and impacts when using this product. The Creality Sermoon P1S 3D scanner is a high-precision device with a delicate internal structure; severe vibrations or impacts may damage the structure and cause damage to the optical components. ● Please use this device at the recommended temperature and humidity. ● Please ensure the usage environment is suitable, and when using a wired connection, ensure the cable connector is intact.
#   → Соблюдайте следующие указания, иначе возможны повреждение оборудования или его неисправность.<br>● Избегайте сильной вибрации и ударов при использовании. 3D-сканер Creality Sermoon P1S — высокоточное устройство со сложной внутренней конструкцией; сильная вибрация или удары могут повредить конструкцию и оптические компоненты.<br>● Используйте устройство при рекомендуемых температуре и влажности.<br>● Убедитесь, что условия эксплуатации подходят, а при проводном подключении — что разъём кабеля исправен.
t('P20b11', merge=['P20b12', 'P20b13', 'P20b14', 'P20b15'], html='Соблюдайте следующие указания, иначе возможны повреждение оборудования или его неисправность.<br>● Избегайте сильной вибрации и ударов при использовании. 3D-сканер Creality Sermoon P1 — высокоточное устройство со сложной внутренней конструкцией; сильная вибрация или удары могут повредить конструкцию и оптические компоненты.<br>● Используйте устройство при рекомендуемых температуре и влажности.<br>● Убедитесь, что условия эксплуатации подходят, а при проводном подключении — что разъём кабеля исправен.')
# P20b16  sz8.0 B  (56.7, 178.8, 174.1, 189.4)
# EN: 6.2 Maintenance Instructions
t('P20b16', html='<b>6.2 Указания по обслуживанию</b>')  # TM exact: sermoon-p1s P23b16
# P20b17 +6  sz6.0  (56.7, 190.9, 554.0, 258.9)
# EN: ● To clean the equipment, please use a cotton cloth dampened with diluted neutral detergent, wring it out, and wipe it. Do not use a damp cloth, volatile oil, thinner, or other liquids to wipe the equipment, as this may damage the equipment's exterior or, in severe cases, damage the equipment parts. ● Store the equipment in its instrument case in a cool, dry place with a relatively stable temperature. Avoid storing it in the following places: - Places with excessively high or low temperature and humidity - Places with a lot of dust - Places containing corrosive or flammable gases - Places containing corrosive or flammable liquids
t('P20b17', merge=['P20b18', 'P20b19', 'P20b20', 'P20b21', 'P20b22', 'P20b23'], html='● Для очистки используйте хлопковую ткань, смоченную разбавленным нейтральным моющим средством и хорошо отжатую. Не протирайте оборудование мокрой тканью, летучими маслами, растворителем или другими жидкостями — это может повредить корпус, а в тяжёлых случаях и детали.<br>● Храните оборудование в футляре, в прохладном сухом месте со стабильной температурой. Не храните его:<br>- в местах со слишком высокой или низкой температурой и влажностью;<br>- в запылённых местах;<br>- рядом с едкими или горючими газами;<br>- рядом с едкими или горючими жидкостями.')  # TM exact: sermoon-p1s P23b17
# P20b0  sz8.0 B  (56.7, 304.6, 227.0, 315.2)
# EN: Shenzhen Creality 3D Technology Co., Ltd.
t('P20b0', html='<b>Shenzhen Creality 3D Technology Co., Ltd.</b>')  # TM exact: sermoon-p1s P23b0
# P20b1 +2  sz5.0  (56.7, 315.8, 302.1, 338.4)
# EN: Official website: www.creality.com Tel: +86 755 3396 5666 Customer Service : cs@creality.com Company Address: 18F, JinXiuHongDu Building, Meilong Blvd., Longhua Dist. Shenzhen, 518131 China
# TM 100% (sermoon-p1s P23b1): OfÏcial website: www.creality.com Tel: +86 755 3396 5666 Customer Service : cs@creality.com Company Address: 18F, JinXiuHongDu Building, Meilong Blvd., Longhua Dist. Shenzhen, 518131 China
#   → Официальный сайт: www.creality.com<br>Тел.: +86 755 3396 5666&nbsp;&nbsp;Служба поддержки: cs@creality.com<br>Адрес: 18F, JinXiuHongDu Building, Meilong Blvd., Longhua Dist. Shenzhen, 518131 China
t('P20b1', merge=['P20b2', 'P20b3'], html='Официальный сайт: www.creality.com<br>Тел.: +86 755 3396 5666&nbsp;&nbsp;Служба поддержки: cs@creality.com<br>Адрес: 18F, JinXiuHongDu Building, Meilong Blvd., Longhua Dist. Shenzhen, 518131 China')
# P20b24  sz6.0  (387.4, 347.5, 453.3, 363.4)
# EN: Facebook Community Discuss, Share, Interact
t('P20b24', align='center', html='Сообщество в Facebook<br>Обсуждение, обмен опытом, общение')  # TM exact: sermoon-p1s P23b24
# P20b25 +1  sz6.0  (480.2, 347.5, 575.0, 371.4)
# EN: Creality wiki Tutorials, FAQs, Troubleshooting, etc.
t('P20b25', merge=['P20b26'], html='Creality Wiki<br>Инструкции, FAQ, устранение неполадок и др.')  # TM exact: sermoon-p1s P23b25
# P20b4 +1  sz5.0  (56.7, 374.1, 531.0, 388.8)
# EN: Your device has been certified by the relevant countries and regions. You can view this electronic certification information on your device: Go to the device's "Settings" menu, select "My Device", tap "Certification Information" to find all applicable electronic certification marks and details.
t('P20b4', merge=['P20b5'], html='Ваше устройство сертифицировано в соответствующих странах и регионах. Электронные сведения о сертификации можно посмотреть на устройстве: откройте меню «Settings» (Настройки), выберите «My Device» (Моё устройство) и коснитесь «Certification Information» (Сведения о сертификации) — там приведены все применимые электронные знаки и сведения.')  # TM exact: sermoon-p1s P23b4
