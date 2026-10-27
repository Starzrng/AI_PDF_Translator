# -*- coding: utf-8 -*-
"""RU translations for sermoon-p1s (skeleton from `python -m pdft init`).

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
# P1b0  sz12.0 B  (46.5, 349.4, 225.2, 361.6)
# EN: Creality Sermoon P1S 3D Scanner
t('P1b0', html='3D-сканер Creality Sermoon P1S')
# P1b1  sz7.5  (46.5, 364.9, 117.9, 374.9)
# EN: Quick Start Guide V1.0
t('P1b1', html='Краткое руководство V1.0')

# ==================== PAGE 2 ====================
# P2b0  sz12.0 B  (259.5, 33.1, 336.4, 45.3)
# EN: FOREWORD
t('P2b0', html='ПРЕДИСЛОВИЕ')
# P2b8  sz12.0 B  (527.5, 33.1, 544.8, 45.3)
# EN: EN
t('P2b8', html='RU')
# P2b2  sz7.0  (43.3, 60.4, 323.0, 123.7)
# EN: Thank you for choosing the Creality Sermoon P1S 3D scanner. This manual aims to help you quickly understand the basic information and scanning process of this scanner, opening up a whole new 3D scanning experience. You can visit the Creality ofÏcial Wiki: <span style="color:#00aeef">https://wiki.creality.com/3d-scanner</span> to get the latest "Creality Sermoon P1S 3D Scanner User Manual", detailed tutorials and videos. This manual will be continuously updated; please refer to the latest version for the most up-to-date information.
t('P2b2', lh=1.35, html='Благодарим вас за выбор 3D-сканера Creality Sermoon P1S. Это руководство поможет вам быстро разобраться в базовых сведениях и процессе сканирования, открыв для вас совершенно новый опыт 3D-сканирования.<br>Посетите официальную Wiki Creality: <span style="color:#00aeef">https://wiki.creality.com/3d-scanner</span>, чтобы получить актуальное «Руководство пользователя 3D-сканера Creality Sermoon P1S», подробные инструкции и видео.<br>Руководство постоянно обновляется; самая актуальная информация — в его последней версии.')
# P2b9  sz8.7 B  (365.0, 63.1, 436.3, 74.7)
# EN: Important Notes
t('P2b9', html='<b>Важные примечания</b>')
# P2b4 +3  sz6.0  (346.5, 77.5, 548.9, 112.5)
# EN: ●Do not allow the scanner to come into contact with water or other liquids. Avoid bumping or impact during use. ●To ensure optimal performance, please operate in a suitable working environment.
t('P2b4', merge=['P2b5', 'P2b6', 'P2b7'], html='● Не допускайте контакта сканера с водой или другими жидкостями. Избегайте ударов и толчков при использовании.<br>● Для оптимальной работы эксплуатируйте устройство в подходящих условиях.')
# P2b1  sz12.0 B  (228.0, 143.2, 367.9, 155.4)
# EN: TABLE OF CONTENTS
t('P2b1', html='СОДЕРЖАНИЕ')
# P2b3  sz7.0 B  (43.3, 167.9, 242.5, 345.3)
# EN: <b>1. Product Introduction</b> ● 1.1 Scanner Components ● 1.2 Part List <b>2. First-Time Use</b> ● 2.1 Standalone Mode (No computer connection required) ● 2.2 PC Connection Mode (Connect to Computer) <b>3. Detailed Explanation of Scanning Modes</b> ● 3.1 Blue Laser Mode ● 3.2 Infrared Mode <b>4. Other Functions</b> ● 4.1 Calibration ● 4.2 System Upgrade ● 4.3 File Transfer <b>5.Specifications</b> ● 5.1 Hardware Parameters <b>6.Precautions</b> ● 6.1 Usage Instructions ● 6.2 Maintenance Instructions
t('P2b3', lh=1.4, html='<b>1. Обзор устройства</b><br>● 1.1 Компоненты сканера<br>● 1.2 Комплект поставки<br><b>2. Начало работы</b><br>● 2.1 Автономный режим (без подключения к компьютеру)<br>● 2.2 Режим подключения к ПК (подключение к компьютеру)<br><b>3. Подробное описание режимов сканирования</b><br>● 3.1 Режим синего лазера<br>● 3.2 Инфракрасный режим<br><b>4. Прочие функции</b><br>● 4.1 Калибровка<br>● 4.2 Обновление системы<br>● 4.3 Передача файлов<br><b>5. Характеристики</b><br>● 5.1 Аппаратные параметры<br><b>6. Меры предосторожности</b><br>● 6.1 Указания по эксплуатации<br>● 6.2 Указания по обслуживанию')

# ==================== PAGE 3 ====================
# P3b0  sz12.0 B  (203.6, 32.4, 393.0, 44.6)
# EN: 1. PRODUCT INTRODUCTION
t('P3b0', html='1. ОБЗОР УСТРОЙСТВА')
# P3b1  sz8.0 B  (45.1, 53.7, 145.4, 61.7)
# EN: 1.1 Scanner Components
t('P3b1', html='<b>1.1 Компоненты сканера</b>')
# P3b10.1  sz6.0  (325.5, 127.6, 374.8, 133.7)
# EN: Parallel-Line Laser
t('P3b10.1', html='Лазер параллельных линий')
# P3b10.2  sz6.0  (406.9, 127.6, 453.6, 133.7)
# EN: Single-Line Laser
t('P3b10.2', html='Лазер одиночной линии')
# P3b9  sz6.0  (320.0, 139.1, 353.6, 145.2)
# EN: RGB Camera
t('P3b9', html='RGB-камера')
# P3b11  sz6.0  (429.0, 139.1, 470.8, 145.2)
# EN: MASK Projector
t('P3b11', html='MASK-проектор')
# P3b2  sz6.0  (169.1, 145.2, 212.6, 151.3)
# EN: HD Touchscreen
t('P3b2', html='Сенсорный HD-экран')
# P3b8  sz6.0  (266.0, 150.6, 331.8, 156.7)
# EN: 3D Scanning Camera × 2
t('P3b8', html='Камера 3D-сканирования × 2')
# P3b12  sz6.0  (451.9, 150.6, 497.0, 156.7)
# EN: Cross-Line Laser
t('P3b12', html='Лазер перекрёстных линий')
# P3b3  sz6.0  (204.2, 162.5, 240.6, 168.6)
# EN: Power Button
t('P3b3', html='Кнопка питания')
# P3b13  sz6.0  (474.2, 163.1, 512.3, 169.2)
# EN: DOE Projector
t('P3b13', html='DOE-проектор')
# P3b6  sz6.0  (224.2, 179.3, 322.8, 185.4)
# EN: Blue & White Supplemental Light × 8
t('P3b6', html='Синяя и белая подсветка × 8')
# P3b4  sz6.0  (221.6, 193.7, 272.2, 201.6)
# EN: Start/Pause Button
t('P3b4', html='Кнопка «Старт/Пауза»')
# P3b14  sz6.0  (515.6, 206.6, 547.6, 214.5)
# EN: Type-C Port
t('P3b14', html='Порт Type-C')
# P3b7  sz6.0  (244.2, 211.1, 328.7, 217.2)
# EN: Infrared Supplemental Light × 4
t('P3b7', html='ИК-подсветка × 4')
# P3b5  sz6.0  (216.1, 258.9, 269.7, 266.8)
# EN: Replaceable Battery
t('P3b5', html='Сменный аккумулятор')

# ==================== PAGE 4 ====================
# P4b0  sz8.0 B  (45.1, 25.5, 94.2, 36.1)
# EN: 1.2 Part List
t('P4b0', html='1.2 Комплект поставки')
# P4b1 +1  sz8.0  (55.2, 135.1, 148.5, 155.1)
# EN: Creality Sermoon P1S 3D Scanner × 1
t('P4b1', merge=['P4b2'], html='3D-сканер Creality Sermoon P1S × 1')
# P4b4 +1  sz8.0  (187.0, 135.1, 293.7, 155.1)
# EN: High-Precision Glass Calibra- tion Board × 1
t('P4b4', merge=['P4b5'], html='Высокоточная стеклянная<br>калибровочная плита × 1')
# P4b7  sz8.0  (338.8, 135.1, 399.9, 145.7)
# EN: Marker Block × 6
t('P4b7', align='center', html='Маркерный блок × 6')
# P4b9 +1  sz8.0  (453.6, 135.1, 555.2, 155.1)
# EN: USB 3.0 Type-C Data Cable (2m) × 1
t('P4b9', merge=['P4b10'], html='Кабель USB 3.0 Type-C<br>(2 м) × 1')
# P4b12 +1  sz8.0  (51.9, 237.3, 151.9, 257.4)
# EN: Reflective Markers (D6mm, D3mm) × 20
t('P4b12', merge=['P4b13'], html='Светоотражающие маркеры<br>(D6 мм, D3 мм) × 20')
# P4b3  sz8.0  (205.5, 237.3, 275.1, 247.9)
# EN: Backup Battery × 1
t('P4b3', align='center', html='Запасной аккумулятор × 1')
# P4b6  sz8.0  (347.9, 237.3, 390.8, 247.9)
# EN: Lanyard × 1
t('P4b6', align='center', html='Шнурок × 1')
# P4b8  sz8.0  (469.9, 237.3, 536.8, 247.9)
# EN: Cleaning Cloth × 1
t('P4b8', align='center', html='Салфетка для очистки × 1')
# P4b14  sz8.0  (216.6, 343.3, 264.0, 353.9)
# EN: NIR Filter × 2
t('P4b14', align='center', html='NIR-фильтр × 2')
# P4b11  sz8.0  (42.5, 344.0, 160.7, 364.0)
# EN: Quick Start Guide, Certificate of Conformity & Warranty Card × 1
t('P4b11', align='center', html='Краткое руководство, сертификат<br>соответствия и гарантийный талон × 1')

# ==================== PAGE 5 ====================
# P5b0  sz12.0 B  (236.9, 31.9, 358.5, 44.1)
# EN: 2. FIRST-TIME USE
t('P5b0', html='2. НАЧАЛО РАБОТЫ')
# P5b1  sz7.0 B  (43.1, 54.0, 527.6, 72.2)
# EN: Creality Sermoon P1S supports two working modes: standalone mode and PC connection mode. You can choose the appropriate mode to operate according to your needs.
t('P5b1', html='<b>Creality Sermoon P1S поддерживает два режима работы: автономный и режим подключения к ПК. Выберите подходящий режим в зависимости от ваших задач.</b>')
# P5b6  sz8.7 B  (72.5, 81.7, 195.6, 93.3)
# EN: Important Note for First Use
t('P5b6', html='<b>Важно при первом использовании</b>')
# P5b2 +3  sz6.0 B  (53.9, 95.2, 542.1, 130.1)
# EN: Due to transportation safety regulations, the battery has a low charge at the factory. Combined with natural wear and tear during transportation, the device may not power on upon first use due to insufÏcient charge. <b>Please charge the battery for at least 30 minutes before first use to activate it.</b> Note: The battery of this device supports separate charging (by directly connecting the charging cable to the battery charging port) or it can be inserted into the back of the device and connected to the main unit for charging.
t('P5b2', merge=['P5b3', 'P5b4', 'P5b5'], html='Из-за правил безопасности при перевозке аккумулятор поставляется с завода слабо заряженным, а за время доставки дополнительно разряжается, поэтому при первом использовании устройство может не включиться. <b>Перед первым использованием заряжайте аккумулятор не менее 30 минут, чтобы активировать его.</b><br>Примечание: аккумулятор можно заряжать отдельно (подключив зарядный кабель напрямую к его порту зарядки) или вставить в заднюю часть устройства и заряжать через основной блок.')
# P5b13  sz6.0  (43.1, 142.1, 514.0, 150.0)
# EN: Before first use, please be sure to remove all protective films from the scanner (lens, filter, laser) and touchscreen to ensure optimal scanning accuracy and image display.
t('P5b13', html='Перед первым использованием снимите все защитные плёнки со сканера (объектив, фильтр, лазер) и сенсорного экрана — для наилучшей точности сканирования и качества изображения.')
# P5b7  sz8.0 B  (43.1, 162.9, 273.3, 173.5)
# EN: 2.1 Standalone Mode (No computer connection required)
t('P5b7', html='<b>2.1 Автономный режим (без подключения к компьютеру)</b>')
# P5b8  sz6.0  (43.1, 174.0, 452.7, 182.0)
# EN: The Creality Sermoon P1S scanner has a built-in operating system and screen, allowing it to perform scanning and basic processing independently.
t('P5b8', html='3D-сканер Creality Sermoon P1S имеет встроенную операционную систему и экран, что позволяет ему самостоятельно выполнять сканирование и базовую обработку.')
# P5b9  sz8.0 B  (43.1, 189.9, 163.3, 200.5)
# EN: Step 1: Power-on Preparation
t('P5b9', html='<b>Шаг 1: Подготовка к включению</b>')
# P5b10 +1  sz6.0  (43.1, 201.0, 336.6, 218.0)
# EN: Make sure the scanner has sufÏcient power . Press and hold the power button <span style="color:#00aeef">for 3 seconds to turn on</span> the device, and it will enter the main interface.
t('P5b10', merge=['P5b11'], html='Убедитесь, что сканер достаточно заряжен.<br>Нажмите и удерживайте кнопку питания <span style="color:#00aeef">3 секунды, чтобы включить</span> устройство, — откроется главный экран.')
# P5b12  sz6.0  (43.1, 228.0, 119.3, 236.0)
# EN: Complete First-Time Setup
t('P5b12', html='Завершите первоначальную настройку')
# P5b15  sz6.0  (43.1, 247.7, 215.3, 255.6)
# EN: 1. Language Selection : Select your language and click [Next].
t('P5b15', html='1. Выбор языка: выберите язык и нажмите «Next» (Далее).')
# P5b14  sz6.0  (312.4, 247.8, 553.3, 264.8)
# EN: 2. Network connection: Select an available local area network . After the connection is established, the system will automatically proceed to the next step.
t('P5b14', html='2. Подключение к сети: выберите доступную локальную сеть. После подключения система автоматически перейдёт к следующему шагу.')

# ==================== PAGE 6 ====================
# P6b0  sz6.0  (42.6, 23.3, 338.0, 31.2)
# EN: 3. Privacy Policy: Please read and agree to our Privacy Policy and User Agreement before using the device.
t('P6b0', html='3. Политика конфиденциальности: перед использованием устройства прочтите и примите нашу Политику конфиденциальности и Пользовательское соглашение.')
# P6b1  sz6.0  (42.9, 208.3, 219.5, 216.3)
# EN: 4. Activation: Device activation takes a while, please be patient.
t('P6b1', html='4. Активация: активация устройства занимает некоторое время, подождите.')

# ==================== PAGE 7 ====================
# P7b0  sz6.0  (42.5, 23.3, 408.5, 31.2)
# EN: 5. Account Login: Supports login with Creality Cloud account. You can skip the login without affecting the normal use of the device.
t('P7b0', html='5. Вход в аккаунт: поддерживается вход через аккаунт Creality Cloud. Вход можно пропустить — это не повлияет на обычную работу устройства.')
# P7b1  sz6.0  (42.5, 32.3, 251.1, 40.2)
# EN: Note: You need to log in to your account before upgrading the firmware.
t('P7b1', html='Примечание: перед обновлением прошивки необходимо войти в аккаунт.')
# P7b2  sz6.0  (42.5, 210.4, 385.5, 218.4)
# EN: Skipping login will trigger a confirmation pop-up. If you still do not log in, select "Do Not Use" to proceed to the next page.
t('P7b2', html='Если пропустить вход, появится окно подтверждения. Чтобы всё же продолжить без входа, выберите «Do Not Use» (Не использовать) — откроется следующая страница.')

# ==================== PAGE 8 ====================
# P8b2  sz6.0  (42.5, 23.3, 404.4, 31.2)
# EN: 6. Device Protection: On this page, you can set a device power-on password to prevent unauthorized users from using the device.
t('P8b2', html='6. Защита устройства: на этой странице можно задать пароль включения, чтобы устройством не могли пользоваться посторонние.')
# P8b0  sz6.0  (42.5, 197.4, 244.0, 205.4)
# EN: 7. Welcome page: Tap anywhere on the screen to start using the device .
t('P8b0', html='7. Страница приветствия: коснитесь любого места экрана, чтобы начать работу с устройством.')
# P8b1  sz6.0  (42.5, 359.5, 542.2, 367.4)
# EN: 8. Beginner tutorial video: You can choose whether to skip it. After watching/skipping, you will be taken directly to the device scanning page to start your first scanning experience.
t('P8b1', html='8. Обучающее видео для начинающих: его можно пропустить. После просмотра или пропуска вы сразу перейдёте на страницу сканирования и сможете выполнить первое сканирование.')

# ==================== PAGE 9 ====================
# P9b3  sz8.0 B  (42.5, 20.3, 133.0, 30.9)
# EN: Step 2: Start Scanning
t('P9b3', html='<b>Шаг 2: Начало сканирования</b>')
# P9b0  sz6.0 B  (42.5, 34.2, 254.4, 42.1)
# EN: ● Click " <b>New Project</b> " on the device screen to enter the scan preview page.
t('P9b0', html='● Нажмите «<b>New Project</b>» (Новый проект) на экране устройства, чтобы открыть страницу предпросмотра сканирования.')
# P9b1 +1  sz6.0 B  (42.5, 195.6, 454.1, 212.5)
# EN: ● Select appropriate <b>scanning settings</b> (blue line laser/infrared) and related <span style="color:#00aeef">parameters based on the characteristics of the object being scanned .</span> ● Select the appropriate scanning mode and click " <b>Apply</b> " to scan according to the selected mode.
t('P9b1', merge=['P9b2'], html='● Выберите подходящие <b>настройки сканирования</b> (синий лазер / инфракрасный режим) и связанные <span style="color:#00aeef">параметры в зависимости от особенностей сканируемого объекта.</span><br>● Выберите подходящий режим сканирования и нажмите «<b>Apply</b>» (Применить), чтобы сканировать в выбранном режиме.')

# ==================== PAGE 10 ====================
# P10b0 +1  sz6.0 B  (42.5, 23.4, 535.0, 40.4)
# EN: ● <b>Adjust the scanning distance: </b> Move the scanner to adjust its distance from the scanned object. When the distance indicator bar on the right side of the screen is within the green "Optimal" range, it means the current distance is ideal for scanning.
t('P10b0', merge=['P10b1'], html='● <b>Регулировка расстояния сканирования:</b> перемещайте сканер, изменяя расстояние до объекта. Когда индикатор расстояния справа на экране находится в зелёной зоне «Optimal» (Оптимально), расстояние идеально для сканирования.')
# P10b2 +3  sz6.0 B  (42.5, 315.5, 531.4, 350.5)
# EN: ● <b>Start scanning : Briefly press the start/pause button</b> on the scanner , or tap the [Start] button on the device screen . Keep the scanner pointed at the object and move it smoothly and slowly to scan the object from all angles (360°). ● <b>Complete Scan : Once the data acquisition is complete, press and hold the start/pause button</b> on the scanner for more than 2 seconds, or tap "Finish" on the device screen . The scanned point cloud data will be automatically displayed on the device screen.
t('P10b2', merge=['P10b3', 'P10b4', 'P10b5'], html='● <b>Начало сканирования: кратко нажмите кнопку «Старт/Пауза»</b> на сканере или коснитесь кнопки [Start] (Старт) на экране устройства. Направляйте сканер на объект и плавно, медленно перемещайте его, чтобы отсканировать объект со всех сторон (360°).<br>● <b>Завершение сканирования: после сбора данных нажмите и удерживайте кнопку «Старт/Пауза»</b> на сканере более 2 секунд или коснитесь «Finish» (Готово) на экране устройства. Отсканированное облако точек автоматически отобразится на экране устройства.')

# ==================== PAGE 11 ====================
# P11b1  sz8.0 B  (42.5, 25.7, 144.2, 33.8)
# EN: Step 3: Model Processing
t('P11b1', html='Шаг 3: Обработка модели')
# P11b2  sz6.0  (42.5, 34.5, 509.2, 42.5)
# EN: After the scanning is complete, you can use the processing function built into the Creality Sermoon P1 device to generate the final 3D model from the point cloud data.
t('P11b2', html='После завершения сканирования итоговую 3D-модель можно создать из облака точек с помощью встроенной функции обработки Creality Sermoon P1S.')
# P11b3  sz6.0 B  (42.5, 51.5, 373.1, 69.5)
# EN: <span style="font-size:7.0px"><b>● Processing Flow (Operate on the screen) :</b></span> 1. <b>Fusion</b> : Fuse multiple frames of point cloud data collected during the scanning process into a complete point cloud.
t('P11b3', html='<span style="font-size:7px"><b>● Порядок обработки (на экране устройства):</b></span><br>1. <b>Fusion</b> (Слияние): объединение нескольких кадров облака точек, собранных при сканировании, в единое облако точек.')
# P11b0  sz6.0 B  (42.5, 234.4, 376.8, 242.3)
# EN: 2. <b>Alignment</b> ( if applicable ) : Multiple merged Scans can be aligned together into a complete model to view the effect.
t('P11b0', html='2. <b>Alignment</b> (Выравнивание) (при необходимости): несколько объединённых сканов можно выровнять в единую модель, чтобы оценить результат.')

# ==================== PAGE 12 ====================
# P12b0  sz6.0 B  (42.5, 23.4, 356.8, 31.4)
# EN: 3. <b>Meshing</b> : Perform comprehensive optimization on the fused mesh data to make it more complete and smooth.
t('P12b0', html='3. <b>Meshing</b> (Построение сетки): всесторонняя оптимизация объединённых данных сетки, чтобы сделать её более полной и гладкой.')
# P12b1  sz6.0 B  (42.5, 208.7, 435.5, 216.6)
# EN: 4. <b>Color Mapping</b> (if applicable) : If color information is captured during scanning, this step applies colors and textures to the model surface.
t('P12b1', html='4. <b>Color Mapping</b> (Наложение цвета) (при необходимости): если при сканировании записывалась информация о цвете, на этом шаге цвета и текстуры накладываются на поверхность модели.')
# P12b2 +1  sz6.0  (42.5, 353.6, 306.0, 370.5)
# EN: Note: For more detailed tutorials on model processing, please visit the Creality ofÏcial Wiki. https://wiki.creality.com/3d-scanner
t('P12b2', merge=['P12b3'], html='Примечание: подробные инструкции по обработке модели — на официальной Wiki Creality: https://wiki.creality.com/3d-scanner')

# ==================== PAGE 13 ====================
# P13b0  sz8.0 B  (41.7, 28.8, 233.4, 39.4)
# EN: 2.2 PC Connection Mode (Connect to Computer)
t('P13b0', html='2.2 Режим подключения к ПК (подключение к компьютеру)')
# P13b1  sz6.0  (41.7, 39.9, 411.9, 47.8)
# EN: Connect to a computer via USB 3.0 or Wi-Fi and use the CrealityScan software for advanced scanning control and model processing.
t('P13b1', html='Подключите сканер к компьютеру через USB 3.0 или Wi-Fi и используйте ПО CrealityScan для расширенного управления сканированием и обработки моделей.')
# P13b2  sz6.0  (41.7, 48.9, 460.9, 56.8)
# EN: Note: PC connection mode has specific requirements for computer specifications; please refer to "System Requirements" in section 5.1 for details.
t('P13b2', html='Примечание: для режима подключения к ПК есть требования к характеристикам компьютера; подробнее — «Системные требования» в разделе 5.1.')
# P13b3  sz8.0 B  (41.7, 76.0, 148.1, 84.2)
# EN: 2.2.1 Software Preparation
t('P13b3', html='2.2.1 Подготовка ПО')
# P13b4  sz6.0  (41.7, 84.9, 513.3, 92.8)
# EN: ● Download the Software: Visit the Creality ofÏcial Wiki software download page: <span style="color:#00aeef">https://wiki.creality.com/en/software</span> , find the CrealityScan software and download it.
t('P13b4', html='● Загрузка ПО: перейдите на страницу загрузки ПО на официальной Wiki Creality: <span style="color:#00aeef">https://wiki.creality.com/en/software</span>, найдите ПО CrealityScan и загрузите его.')
# P13b5  sz6.0  (103.5, 252.3, 490.1, 260.2)
# EN: Note: CrealityScan software has specific operating system requirements; please refer to section 5.1 "System Requirements" for details.
t('P13b5', html='Примечание: у ПО CrealityScan есть требования к операционной системе; подробнее — раздел 5.1 «Системные требования».')
# P13b6 +2  sz6.0 B  (41.7, 292.1, 444.4, 326.9)
# EN: ●Install software: ○ Windows: Double-click the installer and follow the prompts to complete the installation. ○ macOS: After installation, <b>please grant the 3D scanner read and write permissions to optimize point clouds and generate models when </b> using the software .
t('P13b6', merge=['P13b7', 'P13b8'], html='● Установка ПО:<br>&nbsp;&nbsp;&nbsp;○ Windows: дважды щёлкните установщик и следуйте подсказкам, чтобы завершить установку.<br>&nbsp;&nbsp;&nbsp;○ macOS: после установки <b>предоставьте 3D-сканеру права на чтение и запись, чтобы при работе с ПО оптимизировать облака точек и создавать модели</b>.')

# ==================== PAGE 14 ====================
# P14b0  sz8.0 B  (40.8, 32.8, 157.7, 40.9)
# EN: 2.2.2 Connecting the Scanner
t('P14b0', html='<b>2.2.2 Подключение сканера</b>')
# P14b1  sz8.0 B  (40.8, 48.6, 152.0, 59.2)
# EN: Wired Connection (USB 3.0)
t('P14b1', html='Проводное подключение (USB 3.0)')
# P14b2 +2  sz6.0  (40.8, 59.7, 289.7, 94.6)
# EN: ● Insert the Type-C connector of the data cable into the scanner and tighten the screws. ● Insert the other end of the data cable (Type-C) into a USB 3.0 or higher port on your computer to ensure stable data transfer. ● In the pop-up window of Creality Sermoon P1S , select "Scan Connection".
t('P14b2', merge=['P14b3', 'P14b4'], html='● Вставьте разъём Type-C кабеля данных в сканер и затяните винты.<br>● Вставьте другой конец кабеля (Type-C) в порт USB 3.0 или выше на компьютере — это обеспечит стабильную передачу данных.<br>● Во всплывающем окне Creality Sermoon P1S выберите «Scan Connection» (Подключение для сканирования).')
# P14b5  sz6.0  (40.8, 191.2, 375.5, 199.1)
# EN: ● Open the CrealityScan software on your computer; the software will automatically detect and connect to the scanner.
t('P14b5', html='● Откройте ПО CrealityScan на компьютере — оно автоматически обнаружит сканер и подключится к нему.')

# ==================== PAGE 15 ====================
# P15b0  sz8.0 B  (42.5, 21.4, 153.8, 32.0)
# EN: Wireless Connection (Wi-Fi)
t('P15b0', html='Беспроводное подключение (Wi-Fi)')
# P15b1 +2  sz6.0  (42.5, 32.5, 393.1, 58.4)
# EN: ● Step 1: Enable Sermoon P1S hotspot ○ On the Creality Sermoon P1S screen, access the "Settings" menu, select the "Hotspot", and enable “Allows Others to Join”. ○ Record the hotspot name and password.
t('P15b1', merge=['P15b2', 'P15b3'], html='● Шаг 1: Включите точку доступа Sermoon P1S<br>&nbsp;&nbsp;&nbsp;○ На экране Creality Sermoon P1S откройте меню «Settings» (Настройки), выберите «Hotspot» (Точка доступа) и включите «Allows Others to Join» (Разрешить подключение другим).<br>&nbsp;&nbsp;&nbsp;○ Запишите имя и пароль точки доступа.')
# P15b4 +1  sz6.0  (42.5, 212.7, 537.0, 238.6)
# EN: ● Step 2: Connect your computer to the Sermoon P1S hotspot Click "Device Connection" in the upper left corner of the CrealityScan software. In "Device Connection" , find the hotspot network name emitted by Creality Sermoon P1S , click to connect and enter the password.
t('P15b4', merge=['P15b5'], html='● Шаг 2: Подключите компьютер к точке доступа Sermoon P1S<br>Нажмите «Device Connection» (Подключение устройства) в левом верхнем углу ПО CrealityScan. В окне «Device Connection» найдите сеть точки доступа Creality Sermoon P1S, нажмите на неё и введите пароль.')

# ==================== PAGE 16 ====================
# P16b0 +2  sz6.0  (49.1, 20.4, 399.3, 46.3)
# EN: ● Step 3: Software Connection ○ Open the CrealityScan software on your computer . ○ In the software interface, the software will automatically identify and display the connected Creality Sermoon P1S device.
t('P16b0', merge=['P16b1', 'P16b2'], html='● Шаг 3: Подключение ПО<br>&nbsp;&nbsp;&nbsp;○ Откройте ПО CrealityScan на компьютере.<br>&nbsp;&nbsp;&nbsp;○ ПО автоматически определит подключённое устройство Creality Sermoon P1S и покажет его в интерфейсе.')
# P16b3  sz8.0 B  (42.5, 217.0, 460.2, 236.1)
# EN: <b>2.2.3 Start Scaning</b> <span style="font-size:6.0px">● In the CrealityScan software, click 【New Project】, enter the "Project Name" in the pop-up window, select the "Folder Path", and then click 【OK】.</span>
t('P16b3', size=6, html='<span style="font-size:8px"><b>2.2.3 Начало сканирования</b></span><br>● В CrealityScan нажмите «New Project» (Новый проект), укажите «Project Name» (Имя проекта) и «Folder Path» (Путь к папке) и нажмите «OK».')

# ==================== PAGE 17 ====================
# P17b0  sz6.0  (49.1, 20.4, 407.9, 28.3)
# EN: ● Select the appropriate scan mode and related parameters based on the type and characteristics of the object being scanned .
t('P17b0', html='● Выберите подходящий режим сканирования и связанные параметры в зависимости от типа и особенностей сканируемого объекта.')
# P17b1  sz7.0  (49.1, 171.4, 438.4, 180.6)
# EN: Note: Please refer to Chapter 3, " Detailed Explanation of Scan Modes " for instructions on selecting the scan mode.
t('P17b1', html='Примечание: о выборе режима сканирования см. главу 3 «Подробное описание режимов сканирования».')
# P17b2 +8  sz6.0  (42.5, 197.5, 325.5, 286.5)
# EN: ● Click the "Preview" button to enter the scan preview interface. ● Adjust scanning distance: Move the scanner to adjust its distance from the object being scanned. When the distance indicator on the software interface is in the green "optimal" range, it indicates that the current scanning distance is optimal. ● Adjust camera exposure: Automatic exposure is used by default during scanning. If unable to image, please manually adjust the IR camera exposure; gray indicates optimal exposure, red indicates overexposure, and blue indicates underexposure. ● Start scanning: Short press the Start/Pause button on the scanner, or click the [Start] button in the software interface. Keep the scanner pointed at the object and move it smoothly and slowly to perform a 360° all-around scan.
t('P17b2', merge=['P17b3', 'P17b4', 'P17b5', 'P17b6', 'P17b7', 'P17b8', 'P17b9', 'P17b10'], html='● Нажмите кнопку «Preview» (Предпросмотр), чтобы открыть интерфейс предпросмотра сканирования.<br>● Регулировка расстояния сканирования: перемещайте сканер, изменяя расстояние до объекта. Когда индикатор расстояния в интерфейсе ПО находится в зелёной зоне «optimal» (оптимально), текущее расстояние сканирования оптимально.<br>● Настройка экспозиции камеры: по умолчанию при сканировании используется автоэкспозиция. Если изображение не формируется, настройте экспозицию ИК-камеры вручную: серый цвет означает оптимальную экспозицию, красный — переэкспонирование, синий — недоэкспонирование.<br>● Начало сканирования: кратко нажмите кнопку «Старт/Пауза» на сканере или нажмите кнопку [Start] (Старт) в интерфейсе ПО. Направляйте сканер на объект и плавно, медленно перемещайте его, чтобы выполнить круговое сканирование на 360°.')

# ==================== PAGE 18 ====================
# P18b0 +1  sz6.0  (49.1, 20.4, 547.4, 37.3)
# EN: ● Complete Scan: Once the data acquisition is complete, press and hold the Start/Pause button on the scanner for more than 2 seconds, or click "Finish" in the software interface. The scanned point cloud data will be automatically displayed in the software.
t('P18b0', merge=['P18b1'], html='● Завершение сканирования: после сбора данных нажмите и удерживайте кнопку «Старт/Пауза» на сканере более 2 секунд или нажмите «Finish» (Готово) в интерфейсе ПО. Отсканированное облако точек автоматически отобразится в ПО.')
# P18b2  sz8.0 B  (45.0, 211.0, 135.9, 219.2)
# EN: 2.2.4 Model Processing
t('P18b2', html='2.2.4 Обработка модели')
# P18b3 +10  sz6.0 B  (45.0, 222.9, 330.4, 338.8)
# EN: After the scan is completed, you need to use the post-processing function of CrealityScan software to generate the final 3D model from the point cloud data. ● One-click processing : For beginner users, the software's "One-Click Process" function can be used, which will automatically complete fusion, meshing, and color mapping (if applicable). ● Manual processing procedure ( recommended ): 1. <b>Fusion</b> : Merging multiple frames of point cloud data collected during the scanning process into a complete mesh data . 2. <b>Alignment</b> (if applicable) : After fusion, multiple Scans can be aligned together into a complete model to view the effect. 3. <b>Meshing</b> : Perform comprehensive optimization on the fused mesh data to make it more complete and smooth. 4. <b>Color Mapping</b> (if applicable) : If color information is captured during scanning, this step applies colors and textures to the model surface.
t('P18b3', merge=['P18b4', 'P18b5', 'P18b6', 'P18b7', 'P18b8', 'P18b9', 'P18b10', 'P18b11', 'P18b12', 'P18b13'], html='После завершения сканирования создайте итоговую 3D-модель из облака точек с помощью функции постобработки ПО CrealityScan.<br>● Обработка в один клик: начинающим пользователям подойдёт функция «One-Click Process» (Обработка в один клик) — она автоматически выполнит слияние, построение сетки и наложение цвета (при необходимости).<br>● Ручная обработка (рекомендуется):<br>1. <b>Fusion</b> (Слияние): объединение нескольких кадров облака точек, собранных при сканировании, в единые данные сетки.<br>2. <b>Alignment</b> (Выравнивание) (при необходимости): после слияния несколько сканов можно выровнять в единую модель, чтобы оценить результат.<br>3. <b>Meshing</b> (Построение сетки): всесторонняя оптимизация объединённых данных сетки, чтобы сделать её более полной и гладкой.<br>4. <b>Color Mapping</b> (Наложение цвета) (при необходимости): если при сканировании записывалась информация о цвете, на этом шаге цвета и текстуры накладываются на поверхность модели.')
# P18b14  sz7.0  (45.0, 349.4, 465.1, 358.7)
# EN: Note: For more detailed model processing tutorials, please visit the ofÏcial Creality Wiki: https://wiki.creality.com/3d-scanner
t('P18b14', html='Примечание: подробные инструкции по обработке модели — на официальной Wiki Creality: https://wiki.creality.com/3d-scanner')

# ==================== PAGE 19 ====================
# P19b3  sz12.0 B  (142.2, 30.8, 438.9, 43.0)
# EN: 3. DETAILED EXPLANATION OF SCAN MODES
t('P19b3', html='3. ПОДРОБНОЕ ОПИСАНИЕ РЕЖИМОВ СКАНИРОВАНИЯ')
# P19b0  sz6.0 B  (35.9, 50.5, 506.3, 132.5)
# EN: <span style="font-size:7.0px"><b>3.1 Blue Laser Mode</b></span> Suitable for scanning objects that require high accuracy and rich detail, it usually needs to be used with markers. ● <b>Cross-Line Laser:</b> ○ Features: Fast scanning speed and high efÏciency. ○ Applicable scenarios: Scanning large objects. It is necessary to attach markers directly to the object's surface. ● <b>Parallel-Line Laser:</b> ○ Features: Best details. ○ Applicable scenarios: For detailed scanning of objects, resulting in richer model details . If the object is small, markers can be placed on the table around the object. ● <b>Single-Line Laser:</b> ○ Features : Excellent at capturing hard-to-reach areas such as deep holes and grooves. ○ Applicable scenarios: Supplemental scanning of objects with deep hole features.
t('P19b0', html='<span style="font-size:7px"><b>3.1 Режим синего лазера</b></span><br>Подходит для сканирования объектов, требующих высокой точности и детализации; обычно используется с маркерами.<br>● <b>Лазер перекрёстных линий:</b><br>&nbsp;&nbsp;&nbsp;○ Особенности: высокая скорость и эффективность сканирования.<br>&nbsp;&nbsp;&nbsp;○ Применение: сканирование крупных объектов. Маркеры необходимо наклеивать прямо на поверхность объекта.<br>● <b>Лазер параллельных линий:</b><br>&nbsp;&nbsp;&nbsp;○ Особенности: наилучшая детализация.<br>&nbsp;&nbsp;&nbsp;○ Применение: детальное сканирование объектов — модель получается более подробной. Если объект небольшой, маркеры можно разместить на столе вокруг него.<br>● <b>Лазер одиночной линии:</b><br>&nbsp;&nbsp;&nbsp;○ Особенности: отлично захватывает труднодоступные участки, например глубокие отверстия и пазы.<br>&nbsp;&nbsp;&nbsp;○ Применение: дополнительное сканирование объектов с глубокими отверстиями.')
# P19b1  sz6.0 B  (35.9, 140.5, 536.0, 177.5)
# EN: <span style="font-size:7.0px"><b>Tips:</b></span> ● <b>Real-Time Resolution:</b> A smaller resolution results in a more detailed model, but it will consume more computer memory and may affect scanning smoothness. Please select according to your computer performance and model requirements. ● <b>Alignment:</b> If you need to scan multiple sides of an object (such as the front and back), you can scan them in multiple steps and then use the software's "Alignment" function to combine them into a complete model.
t('P19b1', html='<span style="font-size:7px"><b>Советы:</b></span><br>● <b>Разрешение в реальном времени:</b> чем меньше значение, тем детальнее модель, но тем больше памяти компьютера требуется и тем ниже может быть плавность сканирования. Выбирайте с учётом производительности компьютера и требований к модели.<br>● <b>Выравнивание:</b> если нужно отсканировать несколько сторон объекта (например, переднюю и заднюю), сканируйте их в несколько этапов, а затем объедините в единую модель функцией «Alignment» (Выравнивание) в ПО.')
# P19b2  sz6.0 B  (35.9, 185.5, 542.1, 245.0)
# EN: <span style="font-size:7.0px"><b>3.2 Infrared Mode</b></span> It is suitable for scanning faces, bodies , sculptures or other objects with rich features, and usually does not require the application of markers. ● <b>Features:</b> Safe, fast, invisible light, and harmless to human eyes. ● <b>Applicable scenarios:</b> Face scanning, cultural relic protection, medical rehabilitation, etc. ● The infrared mode also supports "Texture" tracking to meet different needs. ● <b>Outdoor Scanning Tips (NIR Filter Usage):</b> When performing infrared scanning in strong outdoor light or high ambient brightness, please install the two "NIR Filters" included in the accessories in front of the two "3D Scanning Camera" lenses on the back of the device. The filters effectively filter out strong light interference and prevent overexposure, thus significantly optimizing outdoor scanning results.
t('P19b2', html='<span style="font-size:7px"><b>3.2 Инфракрасный режим</b></span><br>Подходит для сканирования лиц, тела, скульптур и других объектов с выраженным рельефом; маркеры обычно не нужны.<br>● <b>Особенности:</b> безопасно, быстро, невидимый свет, безвреден для глаз.<br>● <b>Применение:</b> сканирование лиц, сохранение культурного наследия, медицинская реабилитация и т. п.<br>● Инфракрасный режим также поддерживает отслеживание по текстуре («Texture») для разных задач.<br>● <b>Сканирование на улице (NIR-фильтры):</b> при инфракрасном сканировании на ярком солнце или при высокой освещённости установите два NIR-фильтра из комплекта перед объективами двух камер 3D-сканирования на задней стороне устройства. Фильтры подавляют засветку и предотвращают переэкспонирование, заметно улучшая результат сканирования на улице.')
# P19b4  sz12.0 B  (218.5, 260.9, 362.7, 273.1)
# EN: 4. OTHER FUNCTIONS
t('P19b4', html='4. ПРОЧИЕ ФУНКЦИИ')
# P19b5  sz6.0 B  (35.9, 280.1, 519.9, 305.1)
# EN: <span style="font-size:7.0px"><b>4.1 Calibration</b></span> If you notice a decrease in scanning accuracy or if the scanner has not been used for an extended period, calibration is recommended. Please use the included "High-Precision Glass Calibration Board" and follow the on-screen instructions on your Creality Sermoon P1S device to restore the scanner's factory accuracy.
t('P19b5', html='<span style="font-size:7px"><b>4.1 Калибровка</b></span><br>Если вы заметили снижение точности сканирования или сканер долго не использовался, рекомендуется выполнить калибровку. Используйте «Высокоточную стеклянную калибровочную плиту» из комплекта и следуйте инструкциям на экране Creality Sermoon P1S, чтобы восстановить заводскую точность сканера.')
# P19b6  sz6.0 B  (35.9, 314.1, 537.7, 345.1)
# EN: <span style="font-size:7.0px"><b>4.2 System Upgrade</b></span> Creality releases system updates periodically to optimize performance and add new features. Please keep your Creality Sermoon P1S device up to the latest system version and upgrade as prompted for the best user experience. <span style="color:#ed1c24">Note: System upgrades require a Wi-Fi connection to check for and download update packages.</span>
t('P19b6', html='<span style="font-size:7px"><b>4.2 Обновление системы</b></span><br>Creality периодически выпускает обновления системы, улучшающие работу и добавляющие новые функции. Поддерживайте Creality Sermoon P1S в актуальной версии системы и обновляйте её по запросу — так устройство будет работать наилучшим образом.<br><span style="color:#ed1c24"><b>Примечание: для проверки и загрузки обновлений нужно подключение к Wi-Fi.</b></span>')
# P19b7  sz6.0 B  (35.9, 354.1, 531.4, 377.1)
# EN: <span style="font-size:7.0px"><b>4.3 File Transfer</b></span> Select the project you want to share from the "Recent Projects" list , tap the "Share" button in the “...” icon at the top left corner, and follow the on-screen instructions to complete the file transfer.
t('P19b7', html='<span style="font-size:7px"><b>4.3 Передача файлов</b></span><br>Выберите проект в списке «Recent Projects» (Недавние проекты), коснитесь значка «...» в левом верхнем углу, затем «Share» (Поделиться) и следуйте инструкциям на экране.')

# ==================== PAGE 20 ====================
# P20b0  sz12.0 B  (235.0, 27.3, 360.4, 39.5)
# EN: 5. SPECIFICATIONS
t('P20b0', html='5. ХАРАКТЕРИСТИКИ')
# P20b1  sz7.0 B  (43.1, 44.3, 132.7, 53.5)
# EN: 5.1 Hardware Parameters
t('P20b1', html='<b>5.1 Аппаратные параметры</b>')
# P20b2  sz8.0  (257.6, 63.4, 337.7, 74.0)
# EN: Creality Sermoon P1S
t('P20b2', html='Creality Sermoon P1S')
# P20b5  sz6.0  (48.2, 84.3, 91.6, 90.4)
# EN: Scanning Mode
t('P20b5', html='Режим сканирования')
# P20b34.1  sz6.0  (166.2, 84.3, 225.0, 90.4)
# EN: Single Blue Laser Line
t('P20b34.1', html='Одна синяя лазерная линия')
# P20b34.2  sz6.0  (263.1, 84.3, 332.1, 90.4)
# EN: 7 Parallel Blue Laser Lines
t('P20b34.2', html='7 параллельных синих линий')
# P20b34.3  sz6.0  (365.6, 84.3, 433.8, 90.4)
# EN: 34 Cross Blue Laser Lines
t('P20b34.3', html='34 перекрёстные синие линии')
# P20b17  sz6.0  (474.4, 84.3, 529.1, 90.4)
# EN: NIR Structured Light
t('P20b17', html='Структурированный свет (ближний ИК)')
# P20b6  sz6.0  (48.2, 102.4, 81.0, 110.4)
# EN: Accuracy [1]
t('P20b6', html='Точность [1]')
# P20b18  sz6.0  (481.1, 102.4, 522.4, 110.4)
# EN: Up to 0.075mm
t('P20b18', html='До 0.075 мм')
# P20b35  sz6.0  (278.6, 102.5, 316.6, 110.4)
# EN: Up to 0.02mm
t('P20b35', html='До 0.02 мм')
# P20b7  sz6.0  (48.2, 122.3, 103.9, 130.2)
# EN: Volumetric Accuracy
t('P20b7', html='Объёмная точность')
# P20b36  sz6.0  (268.0, 122.3, 327.3, 130.2)
# EN: 0.02mm + 0.08 mm /m
t('P20b36', html='0.02 мм + 0.08 мм/м')
# P20b19  sz6.0  (475.2, 122.3, 528.2, 130.2)
# EN: 0.075mm+0.1mm/m
t('P20b19', html='0.075 мм + 0.1 мм/м')
# P20b20  sz6.0  (477.3, 145.0, 526.1, 152.9)
# EN: 4,587,000 points/s
t('P20b20', html='4 587 000 точек/с')
# P20b8  sz6.0  (48.2, 146.4, 122.5, 154.3)
# EN: Scanning Rate (Standalone)
t('P20b8', html='Скорость замеров (автономно)')
# P20b37.1  sz6.0  (175.2, 146.4, 216.0, 154.3)
# EN: 72,000 points/s
t('P20b37.1', html='72 000 точек/с')
# P20b37.2  sz6.0  (275.6, 146.4, 319.7, 154.3)
# EN: 504,000 points/s
t('P20b37.2', html='504 000 точек/с')
# P20b37.3  sz6.0  (375.3, 146.4, 424.1, 154.3)
# EN: 1,224,000 points/s
t('P20b37.3', html='1 224 000 точек/с')
# P20b21  sz6.0  (477.3, 170.5, 526.1, 178.4)
# EN: 6,881,000 points/s
t('P20b21', html='6 881 000 точек/с')
# P20b9  sz6.0  (48.2, 171.9, 131.9, 179.8)
# EN: Scanning Rate (PC Connection)
t('P20b9', html='Скорость замеров (ПК)')
# P20b38.1  sz6.0  (173.5, 171.9, 217.7, 179.9)
# EN: 108,000 points/s
t('P20b38.1', html='108 000 точек/с')
# P20b38.2  sz6.0  (275.6, 171.9, 319.7, 179.9)
# EN: 756,000 points/s
t('P20b38.2', html='756 000 точек/с')
# P20b38.3  sz6.0  (375.3, 171.9, 424.1, 179.9)
# EN: 1,836,000 points/s
t('P20b38.3', html='1 836 000 точек/с')
# P20b29  sz6.0  (283.8, 193.2, 311.5, 201.1)
# EN: 0.05-2mm
t('P20b29', html='0.05–2 мм')
# P20b22  sz6.0  (489.6, 193.2, 513.9, 201.1)
# EN: 0.1-2mm
t('P20b22', html='0.1–2 мм')
# P20b10  sz6.0  (48.2, 194.9, 85.7, 200.9)
# EN: 3D Resolution
t('P20b10', html='3D-разрешение')
# P20b11  sz6.0  (48.2, 217.3, 127.3, 225.2)
# EN: Scanning Speed (Standalone)
t('P20b11', html='Скорость сканирования (автономно)')
# P20b30  sz6.0  (281.9, 217.3, 313.4, 225.2)
# EN: Up to 60fps
t('P20b30', html='До 60 fps')
# P20b23  sz5.5  (487.3, 218.8, 516.2, 226.0)
# EN: Up to 20fps
t('P20b23', html='До 20 fps')
# P20b12  sz6.0  (48.2, 245.6, 136.7, 253.5)
# EN: Scanning Speed (PC Connection)
t('P20b12', html='Скорость сканирования (ПК)')
# P20b31  sz6.0  (280.2, 245.6, 315.1, 253.5)
# EN: Up to 100fps
t('P20b31', html='До 100 fps')
# P20b24  sz5.5  (487.3, 247.1, 516.2, 254.4)
# EN: Up to 30fps
t('P20b24', html='До 30 fps')
# P20b13  sz6.0  (48.2, 269.7, 95.3, 277.6)
# EN: Min. Scan Volume
t('P20b13', html='Мин. объём сканирования')
# P20b32  sz6.0  (271.4, 269.7, 323.9, 277.6)
# EN: 5mm x 5mm x 5mm
t('P20b32', html='5 × 5 × 5 мм')
# P20b25  sz6.0  (465.5, 269.7, 537.9, 277.6)
# EN: 150mm x 150mm x 150mm
t('P20b25', html='150 × 150 × 150 мм')
# P20b33  sz6.0  (262.0, 289.5, 333.2, 306.0)
# EN: 100mm*128mm at 160mm 500mm*400mm at 550mm
t('P20b33', html='100 × 128 мм на 160 мм<br>500 × 400 мм на 550 мм')
# P20b27 +1  sz5.5  (467.6, 289.6, 535.9, 306.8)
# EN: 160mm*130mm at 170mm 975mm*725mm at 1000mm
t('P20b27', merge=['P20b28'], html='160 × 130 мм на 170 мм<br>975 × 725 мм на 1000 мм')
# P20b14  sz6.0  (48.2, 295.5, 107.8, 301.6)
# EN: Single Capture Range
t('P20b14', html='Диапазон одного захвата')
# P20b15  sz6.0  (48.2, 317.9, 95.4, 325.8)
# EN: Working Distance
t('P20b15', html='Рабочее расстояние')
# P20b4.1  sz6.0  (179.1, 317.9, 212.1, 325.8)
# EN: 200-550mm
t('P20b4.1', html='200–550 мм')
# P20b4.2  sz6.0  (276.1, 317.9, 319.2, 325.8)
# EN: 160mm-400mm
t('P20b4.2', html='160–400 мм')
# P20b4.3  sz6.0  (383.2, 317.9, 416.2, 325.8)
# EN: 200-550mm
t('P20b4.3', html='200–550 мм')
# P20b26  sz6.0  (478.5, 317.9, 524.9, 325.8)
# EN: 170mm-1200mm
t('P20b26', html='170–1200 мм')
# P20b3  sz6.0  (344.2, 337.7, 353.2, 345.7)
# EN: Yes
t('P20b3', html='Да')
# P20b16  sz6.0  (48.2, 339.4, 89.8, 345.5)
# EN: Color Mapping
t('P20b16', html='Наложение цвета')

# ==================== PAGE 21 ====================
# P21b1.2  sz6.0  (247.9, 28.5, 347.4, 36.4)
# EN: Marker / Global Marker / Marker-Free
t('P21b1.2', html='Маркер / Глобальный маркер / Без маркеров')
# P21b1.3  sz6.0  (476.4, 28.5, 527.1, 36.4)
# EN: Geometry / Texture
t('P21b1.3', html='Геометрия / Текстура')
# P21b1.1  sz6.0  (48.2, 30.2, 92.7, 36.3)
# EN: Alignment Mode
t('P21b1.1', html='Режим выравнивания')
# P21b2  sz6.0  (48.2, 50.0, 116.5, 56.1)
# EN: Color Supplemental Light
t('P21b2', html='Цветная подсветка')
# P21b0  sz6.0  (330.7, 50.0, 366.6, 56.1)
# EN: 8 White LEDs
t('P21b0', html='8 белых светодиодов')
# P21b3  sz6.0  (48.2, 68.2, 72.7, 76.1)
# EN: NIR Filter
t('P21b3', html='NIR-фильтр')
# P21b33  sz6.0  (497.2, 68.2, 506.2, 76.1)
# EN: Yes
t('P21b33', html='Да')
# P21b34  sz6.0  (459.4, 84.7, 544.1, 101.2)
# EN: Below 80,000 lux (with filter) Below 50,000 lux (without filter)
t('P21b34', html='До 80 000 люкс (с фильтром)<br>До 50 000 люкс (без фильтра)')
# P21b30  sz6.0  (273.4, 88.0, 321.9, 95.9)
# EN: Below 110,000 lux
t('P21b30', html='До 110 000 люкс')
# P21b4  sz6.0  (48.2, 89.7, 97.2, 95.8)
# EN: Outdoor Scanning
t('P21b4', html='Сканирование на улице')
# P21b31  sz6.0  (234.4, 107.8, 360.8, 115.8)
# EN: 8 Blue LEDs (marker recognition enhancement)
t('P21b31', html='8 синих светодиодов (улучшение распознавания маркеров)')
# P21b5  sz6.0  (48.2, 109.5, 100.5, 115.6)
# EN: Supplemental Light
t('P21b5', html='Подсветка')
# P21b35  sz6.0  (481.2, 109.5, 522.2, 115.6)
# EN: 4 Infrared LEDs
t('P21b35', html='4 ИК-светодиода')
# P21b32  sz6.0  (274.7, 127.7, 320.6, 135.6)
# EN: Class II (eye safe)
t('P21b32', html='Класс II (безопасен для глаз)')
# P21b36  sz6.0  (479.5, 127.7, 523.9, 135.6)
# EN: Class I (eye safe)
t('P21b36', html='Класс I (безопасен для глаз)')
# P21b6  sz6.0  (48.2, 129.4, 80.9, 135.5)
# EN: Laser Safety
t('P21b6', html='Лазерная безопасность')
# P21b7  sz6.0  (48.2, 147.5, 86.8, 155.5)
# EN: Device Weight
t('P21b7', html='Вес устройства')
# P21b17  sz6.0  (315.0, 147.5, 382.3, 155.5)
# EN: 807g (batteries included)
t('P21b17', html='807 г (с аккумуляторами)')
# P21b18  sz6.0  (312.1, 167.4, 385.3, 175.3)
# EN: 209mm × 129 mm × 53 mm
t('P21b18', html='209 × 129 × 53 мм')
# P21b8  sz6.0  (48.2, 169.1, 79.2, 175.2)
# EN: Dimensions
t('P21b8', html='Габариты')
# P21b9  sz6.0  (48.2, 188.9, 94.7, 195.0)
# EN: Calibration Board
t('P21b9', html='Калибровочная плита')
# P21b19  sz6.0  (296.9, 188.9, 400.4, 195.0)
# EN: High-Precision Glass Calibration Board
t('P21b19', html='Высокоточная стеклянная калибровочная плита')
# P21b20 +2  sz6.0  (304.3, 203.8, 393.0, 226.9)
# EN: Qualcomm CPU, 8-core 3.36 GHz GPU, Adreno 740 FPGA
t('P21b20', merge=['P21b21', 'P21b22'], html='Qualcomm CPU, 8 ядер, 3.36 ГГц<br>GPU Adreno 740<br>FPGA')
# P21b10  sz6.0  (48.2, 213.0, 74.3, 219.1)
# EN: Processor
t('P21b10', html='Процессор')
# P21b11  sz6.0  (48.2, 237.1, 82.2, 243.2)
# EN: Built-in RAM
t('P21b11', html='Встроенная ОЗУ')
# P21b23  sz6.0  (327.6, 237.1, 369.8, 243.2)
# EN: 16GB LPDDR5X
t('P21b23', html='16 ГБ LPDDR5X')
# P21b24  sz6.0  (328.7, 255.2, 368.6, 263.2)
# EN: 256GB UFS 4.0
t('P21b24', html='256 ГБ UFS 4.0')
# P21b12  sz6.0  (48.2, 256.9, 90.3, 263.0)
# EN: Built-in Storage
t('P21b12', html='Встроенная память')
# P21b13  sz6.0  (48.2, 276.8, 67.6, 282.9)
# EN: Display
t('P21b13', html='Экран')
# P21b25  sz6.0  (317.4, 276.8, 379.9, 282.9)
# EN: 6-inch HD Touchscreen
t('P21b25', html='6-дюймовый сенсорный HD-экран')
# P21b14  sz6.0  (48.2, 294.9, 67.6, 302.9)
# EN: Battery
t('P21b14', html='Аккумулятор')
# P21b26  sz6.0  (282.8, 294.9, 414.5, 302.9)
# EN: Rated 3300mAh*2 (comes with a backup battery)
t('P21b26', html='Номинал 3300 мА·ч × 2 (в комплекте запасной аккумулятор)')
# P21b15  sz6.0  (48.2, 314.8, 71.5, 322.7)
# EN: Interface
t('P21b15', html='Интерфейс')
# P21b27  sz6.0  (326.0, 314.8, 371.3, 322.7)
# EN: Type-C / USB 3.0
t('P21b27', html='Type-C / USB 3.0')
# P21b28  sz6.0  (321.5, 334.6, 375.8, 342.6)
# EN: PD3.0 Fast Charging
t('P21b28', html='Быстрая зарядка PD3.0')
# P21b16  sz6.0  (48.2, 336.3, 72.6, 342.4)
# EN: Charging
t('P21b16', html='Зарядка')

# ==================== PAGE 22 ====================
# P22b13  sz6.0  (344.2, 40.5, 353.1, 48.4)
# EN: Yes
t('P22b13', html='Да')
# P22b5  sz6.0  (48.2, 42.2, 93.9, 48.3)
# EN: Wireless PC Scan
t('P22b5', html='Беспроводное сканирование с ПК')
# P22b14 +1  sz6.0  (324.5, 58.8, 372.8, 80.0)
# EN: Standalone Mode Wireless PC Mode Wired PC Mode
t('P22b14', merge=['P22b15'], html='Автономный режим<br>Беспроводной режим ПК<br>Проводной режим ПК')
# P22b6  sz6.0  (48.2, 60.3, 79.2, 68.3)
# EN: Work Mode
t('P22b6', html='Режим работы')
# P22b7  sz6.0  (48.2, 88.7, 62.9, 96.6)
# EN: Wi-Fi
t('P22b7', html='Wi-Fi')
# P22b16  sz6.0  (338.8, 88.7, 358.5, 96.6)
# EN: Wi-Fi 7
t('P22b16', html='Wi-Fi 7')
# P22b8  sz6.0  (48.2, 108.5, 99.5, 116.5)
# EN: PC System Support
t('P22b8', html='Поддержка ОС на ПК')
# P22b17  sz6.0  (324.2, 108.5, 373.1, 116.5)
# EN: Windows / macOS
t('P22b17', html='Windows / macOS')
# P22b3  sz6.0 B  (155.9, 129.5, 332.5, 167.8)
# EN: <b>Recommended Requirements:</b> OS: Win10/11 (64-bit) CPU: Intel i7 13th Gen or above Dedicated Graphics Card: NVIDIA RTX 4060 or higher (8GB VRAM) RAM: ≥32GB
t('P22b3', html='<b>Рекомендуемые требования:</b><br>ОС: Win10/11 (64-бит)<br>CPU: Intel i7 13-го поколения или выше<br>Дискретная видеокарта: NVIDIA RTX 4060 или выше (8 ГБ VRAM)<br>ОЗУ: ≥32 ГБ')
# P22b1  sz6.0 B  (360.0, 129.5, 510.5, 167.8)
# EN: <b>Minimum Requirements:</b> OS: Win10/11 (64-bit) CPU: Intel i7 7th Gen Dedicated Graphics Card: NVIDIA RTX 1060 (6GB VRAM) RAM: ≥16GB
t('P22b1', html='<b>Минимальные требования:</b><br>ОС: Win10/11 (64-бит)<br>CPU: Intel i7 7-го поколения<br>Дискретная видеокарта: NVIDIA GTX 1060 (6 ГБ VRAM)<br>ОЗУ: ≥16 ГБ')
# P22b9  sz6.0  (48.2, 157.9, 105.9, 165.8)
# EN: System Requirements
t('P22b9', html='Системные требования')
# P22b4  sz6.0  (155.9, 175.8, 221.3, 199.8)
# EN: OS: macOS 14 or above CPU: Apple M3 or above RAM: ≥32GB
t('P22b4', html='ОС: macOS 14 или выше<br>CPU: Apple M3 или выше<br>ОЗУ: ≥32 ГБ')
# P22b2  sz6.0  (360.0, 177.5, 400.1, 199.8)
# EN: OS: macOS 12 CPU: Apple M2 RAM: ≥16GB
t('P22b2', html='ОС: macOS 12<br>CPU: Apple M2<br>ОЗУ: ≥16 ГБ')
# P22b0  sz6.0  (330.7, 207.8, 366.7, 215.7)
# EN: -10°C to 40°C
t('P22b0', html='от −10 °C до 40 °C')
# P22b10  sz6.0  (48.2, 209.4, 110.1, 215.5)
# EN: Operating Temperature
t('P22b10', html='Рабочая температура')
# P22b18  sz6.0  (334.3, 227.6, 363.0, 235.5)
# EN: 10-90%RH
t('P22b18', html='10–90 % RH')
# P22b11  sz6.0  (48.2, 229.3, 101.0, 235.4)
# EN: Operating Humidity
t('P22b11', html='Рабочая влажность')
# P22b12  sz6.0  (48.2, 250.0, 479.9, 258.0)
# EN: [1] Accuracy is evaluated in laboratory conditions and actual results may be affected by operating environments such as vibration, temperature, and other factors.
t('P22b12', html='[1] Точность оценивается в лабораторных условиях; фактический результат может зависеть от условий эксплуатации, таких как вибрация, температура и др.')

# ==================== PAGE 23 ====================
# P23b6  sz12.0 B  (241.5, 32.8, 352.8, 45.0)
# EN: 6. PRECAUTIONS
t('P23b6', html='6. МЕРЫ ПРЕДОСТОРОЖНОСТИ')
# P23b7 +2  sz6.0  (42.5, 56.7, 308.1, 84.7)
# EN: About the Creality Sermoon P1S 3D Scanner ● Please do not disassemble or assemble the equipment yourself. ● Please use the dedicated accessories included with the product, such as calibration plates.
t('P23b7', merge=['P23b8', 'P23b9'], html='О 3D-сканере Creality Sermoon P1S<br>● Не разбирайте и не собирайте оборудование самостоятельно.<br>● Используйте только фирменные принадлежности из комплекта, например калибровочную плиту.')
# P23b10  sz8.0 B  (42.5, 94.6, 133.4, 105.2)
# EN: 6.1 Usage Instructions
t('P23b10', html='<b>6.1 Указания по эксплуатации</b>')
# P23b11 +4  sz6.0  (42.5, 106.7, 536.7, 154.7)
# EN: Please note the following points, otherwise it may lead to equipment damage or machine malfunction. ● Please avoid significant vibrations and impacts when using this product. The Creality Sermoon P1S 3D scanner is a high-precision device with a delicate internal structure; severe vibrations or impacts may damage the structure and cause damage to the optical components. ● Please use this device at the recommended temperature and humidity. ● Please ensure the usage environment is suitable, and when using a wired connection, ensure the cable connector is intact.
t('P23b11', merge=['P23b12', 'P23b13', 'P23b14', 'P23b15'], html='Соблюдайте следующие указания, иначе возможны повреждение оборудования или его неисправность.<br>● Избегайте сильной вибрации и ударов при использовании. 3D-сканер Creality Sermoon P1S — высокоточное устройство со сложной внутренней конструкцией; сильная вибрация или удары могут повредить конструкцию и оптические компоненты.<br>● Используйте устройство при рекомендуемых температуре и влажности.<br>● Убедитесь, что условия эксплуатации подходят, а при проводном подключении — что разъём кабеля исправен.')
# P23b16  sz8.0 B  (42.5, 164.6, 160.0, 175.2)
# EN: 6.2 Maintenance Instructions
t('P23b16', html='<b>6.2 Указания по обслуживанию</b>')
# P23b17 +6  sz6.0  (42.5, 176.7, 539.8, 244.7)
# EN: ● To clean the equipment, please use a cotton cloth dampened with diluted neutral detergent, wring it out, and wipe it. Do not use a damp cloth, volatile oil, thinner, or other liquids to wipe the equipment, as this may damage the equipment's exterior or, in severe cases, damage the equipment parts. ● Store the equipment in its instrument case in a cool, dry place with a relatively stable temperature. Avoid storing it in the following places: - Places with excessively high or low temperature and humidity - Places with a lot of dust - Places containing corrosive or flammable gases - Places containing corrosive or flammable liquids
t('P23b17', merge=['P23b18', 'P23b19', 'P23b20', 'P23b21', 'P23b22', 'P23b23'], html='● Для очистки используйте хлопковую ткань, смоченную разбавленным нейтральным моющим средством и хорошо отжатую. Не протирайте оборудование мокрой тканью, летучими маслами, растворителем или другими жидкостями — это может повредить корпус, а в тяжёлых случаях и детали.<br>● Храните оборудование в футляре, в прохладном сухом месте со стабильной температурой. Не храните его:<br>- в местах со слишком высокой или низкой температурой и влажностью;<br>- в запылённых местах;<br>- рядом с едкими или горючими газами;<br>- рядом с едкими или горючими жидкостями.')
# P23b0  sz8.0 B  (42.5, 274.6, 212.8, 285.2)
# EN: Shenzhen Creality 3D Technology Co., Ltd.
t('P23b0', html='<b>Shenzhen Creality 3D Technology Co., Ltd.</b>')
# P23b1 +2  sz5.0  (42.5, 285.7, 287.9, 308.4)
# EN: OfÏcial website: www.creality.com Tel: +86 755 3396 5666 Customer Service : cs@creality.com Company Address: 18F, JinXiuHongDu Building, Meilong Blvd., Longhua Dist. Shenzhen, 518131 China
t('P23b1', merge=['P23b2', 'P23b3'], html='Официальный сайт: www.creality.com<br>Тел.: +86 755 3396 5666&nbsp;&nbsp;Служба поддержки: cs@creality.com<br>Адрес: 18F, JinXiuHongDu Building, Meilong Blvd., Longhua Dist. Shenzhen, 518131 China')
# P23b24  sz6.0 B  (373.2, 302.8, 439.1, 318.8)
# EN: <b>Facebook Community</b> Discuss, Share, Interact
t('P23b24', align='center', html='<b>Сообщество в Facebook</b><br>Обсуждение, обмен опытом, общение')
# P23b25  sz6.0 B  (459.9, 304.0, 565.2, 318.3)
# EN: <b>Creality wiki</b> Tutorials, FAQs, Troubleshooting, etc.
t('P23b25', align='center', html='<b>Creality Wiki</b><br>Инструкции, FAQ, устранение неполадок и др.')
# P23b4 +1  sz5.0  (42.5, 329.0, 516.8, 343.6)
# EN: Your device has been certified by the relevant countries and regions. You can view this electronic certification information on your device: Go to the device's "Settings" menu, select "My Device", tap "Certification Information" to find all applicable electronic certification marks and details.
t('P23b4', merge=['P23b5'], html='Ваше устройство сертифицировано в соответствующих странах и регионах. Электронные сведения о сертификации можно посмотреть на устройстве: откройте меню «Settings» (Настройки), выберите «My Device» (Моё устройство) и коснитесь «Certification Information» (Сведения о сертификации) — там приведены все применимые электронные знаки и сведения.')
