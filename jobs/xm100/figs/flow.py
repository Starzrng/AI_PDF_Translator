"""Vector redraw of the menu flowcharts (ch.1.3). Coordinates follow the source rasters (px).
Chips carry EN UI labels; hub titles are Russian.  python3 figs/flow.py -> figs/fc1..fc5.svg"""
import base64, math
from pathlib import Path

HERE = Path(__file__).resolve().parent
ICONS = HERE.parent / 'assets' / 'icons'

C = {'dark': ('#2e2e2e', '#2e2e2e', '#fff'), 'green': ('#8cc63f', '#5f9a25', '#fff'),
     'lgreen': ('#a2c83e', '#83a82a', '#fff'), 'dgreen': ('#3f8f2c', '#2d6e1f', '#fff'),
     'mgreen': ('#5cb534', '#3f8f24', '#fff')}
LINE = {'dark': '#333', 'green': '#8cc63f', 'lgreen': '#a2c83e', 'dgreen': '#3f8f2c', 'mgreen': '#5cb534'}


def _icon(name):
    return 'data:image/png;base64,' + base64.b64encode((ICONS / f'{name}.png').read_bytes()).decode()


def tw(text, fs):
    """rough text width for Inter SemiBold"""
    w = 0
    for ch in text:
        w += 0.36 if ch in 'il.,:;|!()[] ' else (0.62 if ch in 'MWmw' else (0.66 if ch.isupper() else 0.55))
    return w * fs


class Flow:
    def __init__(self, W, H):
        self.W, self.H, self.el = W, H, []

    def chip(self, x, y, w, h, text, kind='dark', fs=None, icon=None, letter=None):
        f, s, t = C[kind]
        c = h * 0.32
        self.el.append(f'<path d="M{x + c},{y} H{x + w - c} L{x + w},{y + h / 2} L{x + w - c},{y + h} H{x + c} L{x},{y + h / 2}Z" '
                       f'fill="{f}" stroke="{s}" stroke-width="2.5"/>')
        x0, w0 = x, w
        if icon or letter:
            r = h * 0.36
            cx, cy = x + h * 0.55, y + h / 2
            self.el.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#fff"/>')
            if icon:
                d = r * 1.25
                self.el.append(f'<image href="{_icon(icon)}" x="{cx - d / 2}" y="{cy - d / 2}" width="{d}" height="{d}" '
                               f'preserveAspectRatio="xMidYMid meet" filter="url(#dk)"/>')
            else:
                self.el.append(f'<text x="{cx}" y="{cy + r * 0.45}" text-anchor="middle" font-size="{r * 1.3:.1f}" '
                               f'font-weight="700" fill="#222">{letter}</text>')
            x0, w0 = x + h * 0.95, w - h * 0.95
        avail = w0 - 2 * c * 0.6 - 6
        fs = fs or h * 0.42
        lines = text.split('|')
        if len(lines) == 1 and tw(text, fs) > avail and ' ' in text:
            # wrap at the space closest to the middle instead of shrinking
            sp = [i for i, ch in enumerate(text) if ch == ' ']
            k = min(sp, key=lambda i: abs(i - len(text) / 2))
            lines = [text[:k], text[k + 1:]]
        if len(lines) > 1:
            fs = min(fs, h * 0.37)
        fs = min(fs, min(avail / max(tw(L, 1), 0.1) for L in lines))
        lh = fs * 1.05
        y0 = y + h / 2 - lh * (len(lines) - 1) / 2 + fs * 0.36
        for i, L in enumerate(lines):
            self.el.append(f'<text x="{x0 + w0 / 2}" y="{y0 + i * lh:.1f}" text-anchor="middle" font-size="{fs:.1f}" '
                           f'font-weight="600" fill="{t}">{L}</text>')

    def line(self, pts, kind='dark', w=3):
        p = ' '.join(f'{a},{b}' for a, b in pts)
        self.el.append(f'<polyline points="{p}" fill="none" stroke="{LINE[kind]}" stroke-width="{w}"/>')

    def bracket(self, x, y1, y2, kind='dark', d=12):
        self.line([(x + d, y1), (x, y1), (x, y2), (x + d, y2)], kind)

    def tri(self, x, y, dir='up', s=11, kind='dark'):
        col = '#111' if kind == 'dark' else LINE[kind]
        pts = {'up': [(x - s, y + s * 0.6), (x + s, y + s * 0.6), (x, y - s * 0.6)],
               'down': [(x - s, y - s * 0.6), (x + s, y - s * 0.6), (x, y + s * 0.6)],
               'right': [(x - s * 0.6, y - s), (x - s * 0.6, y + s), (x + s * 0.6, y)]}[dir]
        self.el.append(f'<polygon points="{" ".join(f"{a},{b}" for a, b in pts)}" fill="{col}"/>')

    def hexnode(self, x, y, r, kind='dark'):
        pts = ' '.join(f'{x + r * math.cos(math.radians(a)):.1f},{y + r * math.sin(math.radians(a)):.1f}' for a in range(0, 360, 60))
        f = '#1f1f1f' if kind == 'dark' else C[kind][0]
        self.el.append(f'<polygon points="{pts}" fill="{f}" stroke="#fff" stroke-width="2"/>')

    def hub(self, cx, cy, R, title, dots='dggg', nodes=(), fs=None):
        def hexpts(r):
            return ' '.join(f'{cx + r * math.cos(math.radians(a)):.1f},{cy + r * math.sin(math.radians(a)):.1f}' for a in range(0, 360, 60))
        self.el.append(f'<polygon points="{hexpts(R)}" fill="none" stroke="#2a2a2a" stroke-width="{R * 0.07:.1f}" '
                       f'stroke-dasharray="{R * 0.16:.1f} {R * 0.09:.1f}" stroke-linejoin="round"/>')
        self.el.append(f'<polygon points="{hexpts(R * 0.76)}" fill="url(#hubg)" stroke="#cfcfcf" stroke-width="1.5"/>')
        self.el.append(f'<polygon points="{hexpts(R * 0.62)}" fill="url(#hubi)"/>')
        lines = title.split('|')
        fs = fs or R * 0.2
        for i, L in enumerate(lines):
            self.el.append(f'<text x="{cx}" y="{cy - (len(lines) - 1) * fs * 0.6 + i * fs * 1.15 + fs * 0.25:.1f}" text-anchor="middle" '
                           f'font-family="PT Sans" font-weight="700" font-size="{fs:.1f}" fill="#111">{L}</text>')
        n = len(dots)
        for i, k in enumerate(dots):
            col = '#222' if k == 'd' else '#6ab42f'
            self.el.append(f'<circle cx="{cx + (i - (n - 1) / 2) * R * 0.11:.1f}" cy="{cy + R * 0.26 + (len(lines) - 1) * fs * 0.55:.1f}" r="{R * 0.035:.1f}" fill="{col}"/>')
        for x, y, k in nodes:
            self.hexnode(x, y, R * 0.075, k)

    def svg(self):
        defs = ('<defs><filter id="dk"><feColorMatrix type="matrix" values="0 0 0 0 0.15  0 0 0 0 0.15  0 0 0 0 0.15  0 0 0 1 0"/></filter>'
                '<radialGradient id="hubg" cx="50%" cy="40%" r="65%"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#9a9a9a"/></radialGradient>'
                '<radialGradient id="hubi" cx="50%" cy="45%" r="60%"><stop offset="0" stop-color="#ffffff"/><stop offset="0.8" stop-color="#f4f4f4"/>'
                '<stop offset="1" stop-color="#dcdcdc"/></radialGradient></defs>')
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-8 -4 {self.W + 16} {self.H + 8}" font-family="Inter, Helvetica, sans-serif">'
                + defs + ''.join(self.el) + '</svg>')


# ---------------------------------------------------------------- 1.3.1 main flow
def fc1():
    f = Flow(1412, 626)
    f.line([(260, 284), (260, 77), (408, 77)])
    f.line([(322, 336), (322, 272), (408, 272)])
    f.line([(385, 405), (408, 405)], 'green')
    f.line([(320, 474), (320, 582), (408, 582)], 'green')
    f.hub(118, 405, 118, 'Главное|меню', 'ddggg', [(172, 302, 'dark'), (203, 350, 'dark'), (231, 403, 'green'), (205, 456, 'green'), (172, 506, 'green')], fs=25)
    f.chip(205, 282, 108, 34, 'Machining', 'dark', icon='tab_machining')
    f.chip(245, 334, 112, 34, 'Tools', 'dark', icon='tab_tools')
    f.chip(278, 388, 110, 34, 'Program', 'green', icon='tab_program')
    f.chip(245, 440, 112, 34, 'System', 'green', icon='tab_system')
    f.chip(205, 494, 108, 34, 'Help', 'green', icon='help')
    W, H, X = 104, 30, [408 + 112 * k for k in range(9)]
    for k, t in enumerate(['Classic View', 'Graphic View', 'Guide View', 'AUTO', 'JOG', 'MDI', 'Home']):
        f.chip(X[k], 62, W, H, t)
    for k, t in enumerate(['Handwheel', 'Rapid', 'Increment']):
        f.chip(X[4 + k], 0, W, H, t)
    f.tri(X[4] + W / 2, 45, 'up')
    for k, t in enumerate(['Handwheel Trial', 'Auto', 'Single Block']):
        f.chip(X[3 + k], 122, W, H, t)
    f.tri(X[3] + W / 2, 107, 'down')
    f.chip(408, 197, 104, 30, 'Details')
    f.chip(520, 197, 104, 30, 'Tool Change')
    f.chip(632, 197, 150, 30, 'Spindle Release (Clamp)')
    f.chip(790, 197, 140, 30, 'Magazine In (Out)')
    f.tri(460, 242, 'up')
    f.chip(408, 257, 104, 30, 'Tool List')
    f.chip(520, 257, 104, 30, 'Offsets')
    for k, t in enumerate(['Local Files', 'USB Drive', 'SD Card', 'Toolpath Preview']):
        f.chip(X[k], 390, W, H, t, 'green')
    f.tri(460, 437, 'down', kind='green')
    f.chip(408, 450, W, H, 'Edit Program', 'green')
    f.chip(520, 450, W, H, 'Load File', 'green')
    for k, t in enumerate(['Alarm Info', 'Alarm History', 'Monitor Data', 'Update Center', 'Machine Config',
                           'HMI Settings', 'Axis Calib.', 'Probe Pairing', 'Machine Calib.']):
        f.chip(X[k], 567, W, H, t, 'green')
    return f


# ---------------------------------------------------------------- 1.3.2 machining
def fc2():
    f = Flow(1585, 1012)
    f.line([(455, 537), (455, 155), (665, 155)])
    f.bracket(665, 118, 190)
    f.line([(548, 622), (548, 527), (665, 527)], 'lgreen')
    f.bracket(665, 448, 605, 'lgreen')
    f.line([(600, 757), (600, 858), (668, 858)], 'lgreen')
    f.bracket(668, 820, 890, 'lgreen')
    f.hub(182, 722, 182, 'Обработка', 'dggg', [(265, 570, 'dark'), (318, 655, 'green'), (352, 722, 'green'), (311, 808, 'green')], fs=40)
    f.chip(335, 535, 193, 50, 'AUTO', 'dark', letter='A')
    f.chip(392, 620, 186, 50, 'JOG', 'lgreen', letter='J')
    f.chip(432, 705, 190, 50, 'MDI', 'green', letter='M')
    f.chip(392, 783, 186, 50, 'Home', 'mgreen', icon='back')
    X, W, H = [688, 870, 1053, 1236, 1420], 143, 45
    for k, t in enumerate(['Edit Program', 'All G Codes', 'G Codes', 'M Codes', 'Auxiliary']):
        f.chip(X[k], 95, W, H, t)
    for k, t in enumerate(['Switch Coord.', 'Relative Coord.', 'FS Override', 'Time', 'Program Control']):
        f.chip(X[k], 167, W, H, t)
    f.tri(1491, 68, 'up')
    f.chip(1420, 0, W, H, 'Protective Door')
    f.tri(1491, 238, 'down')
    f.chip(1420, 260, W, H, 'M01')
    Y = [425, 507, 582]
    for y, (a, rest) in zip(Y, [('TSM', ['Select Tool', 'Select Offset', 'Relative Coord.', 'Switch Coord.']),
                                ('Workpiece|Positioning', ['Single Axis', 'Cylinder', 'Cuboid']),
                                ('Tool Measure', ['Select Tool', 'Tool Setting', 'Probe Calib.'])]):
        f.chip(688, y, W, H, a, 'lgreen')
        f.tri(862, y + 23, 'right')
        for k, t in enumerate(rest):
            f.chip([888, 1070, 1253, 1436][k], y, W, H, t, 'lgreen')
    for k, t in enumerate(['Clear', 'All G Codes', 'G Codes', 'M Codes', 'Auxiliary']):
        f.chip([690, 872, 1055, 1237, 1420][k], 797, W, H, t, 'lgreen')
    for k, t in enumerate(['Switch Coord.', 'Relative Coord.', 'FS Override', 'Program Control']):
        f.chip([690, 872, 1055, 1237][k], 868, W, H, t, 'lgreen')
    f.tri(1491, 772, 'up')
    f.chip(1420, 703, W, H, 'Protective Door', 'lgreen')
    f.tri(1308, 940, 'down')
    f.chip(1237, 962, W, H, 'Handwheel Trial', 'lgreen')
    f.chip(1418, 962, W, H, 'M01', 'lgreen')
    return f


# ---------------------------------------------------------------- workpiece positioning
def fc3():
    f = Flow(1412, 472)
    f.line([(98, 288), (175, 288)])
    pts = ' '.join(f'{49 + 52 * math.cos(math.radians(a + 30)):.1f},{290 + 52 * math.sin(math.radians(a + 30)):.1f}' for a in range(0, 360, 60))
    f.el.append(f'<polygon points="{pts}" fill="#8cc63f"/><text x="49" y="297" text-anchor="middle" font-size="20" font-weight="600" fill="#fff">JOG</text>')
    f.line([(492, 212), (492, 57), (605, 57)])
    f.bracket(605, 13, 107)
    f.line([(598, 286), (662, 286)], 'lgreen')
    f.line([(510, 360), (510, 383), (662, 383)], 'lgreen')
    f.line([(662, 252), (662, 408)], 'dark', 2.5)
    for y, d in [(258, 'up'), (304, 'down'), (360, 'up'), (402, 'down')]:
        f.tri(662, y, d, 8)
    f.hub(295, 285, 118, 'Привязка|заготовки', 'dgg', [(380, 226, 'dark'), (406, 283, 'green'), (378, 336, 'green')], fs=22)
    f.chip(432, 210, 132, 36, 'Single Axis', 'dark', icon='single')
    f.chip(458, 268, 142, 36, 'Cuboid', 'lgreen', icon='cuboid')
    f.chip(438, 326, 126, 36, 'Cylinder', 'lgreen', icon='cylinder')
    W, H = 96, 32
    for y, ax, rest in [(0, 'X Axis', ['Select Offset', 'Save X1', 'Save X2', 'Set Offset', 'Exit']),
                        (50, 'Y Axis', ['Select Offset', 'Save Y1', 'Save Y2', 'Set Offset', 'Exit']),
                        (95, 'Z Axis', ['Select Offset', 'Save Z', 'Set Offset', 'Exit'])]:
        f.chip(625, y, W, H, ax)
        f.tri(737, y + 16, 'right', 8)
        f.chip(760, y, W, H, 'Tool Positioning')
        f.tri(874, y + 16, 'right', 8)
        for k, t in enumerate(rest):
            f.chip(896 + k * 105, y, W, H, t)
    G = 'lgreen'

    def grid(y0, rows):
        for r, row in enumerate(rows):
            for k, t in enumerate(row):
                f.chip(760 + k * 120, y0 + r * 38, 98, 30, t, G)
    f.chip(618, 213, 92, 32, 'Tool Positioning', G)
    f.tri(738, 229, 'right', 8)
    grid(198, [['Select Offset', 'Save Z', 'Save X1', 'Save X2'], ['Save Y1', 'Save Y2', 'Set Offset', 'Exit']])
    f.chip(618, 315, 92, 32, 'Probe Positioning', G)
    f.tri(738, 331, 'right', 8)
    grid(315, [['Select Offset', 'Start Positioning', 'Exit']])
    f.chip(618, 418, 92, 32, 'Tool Positioning', G)
    f.tri(738, 434, 'right', 8)
    grid(402, [['Select Offset', 'Save Z', 'Save P1', 'Save P2'], ['Save P3', 'Set Offset', 'Exit']])
    return f


# ---------------------------------------------------------------- program editing
def fc4():
    f = Flow(1548, 1445)
    f.line([(530, 802), (530, 570), (655, 570)])
    f.bracket(658, 528, 602)
    f.line([(600, 940), (600, 1092), (665, 1092)], 'lgreen')
    f.bracket(665, 1062, 1122, 'lgreen')
    f.line([(530, 1024), (530, 1388), (665, 1388)], 'lgreen')
    f.line([(455, 1107), (455, 1398), (665, 1398)], 'green')
    f.bracket(665, 1360, 1418, 'lgreen')
    f.hub(186, 890, 186, 'Программы', 'dgg', [(316, 826, 'dark'), (352, 910, 'green'), (312, 990, 'green'), (178, 1066, 'green'), (265, 1066, 'green')], fs=38)
    f.chip(392, 800, 198, 52, 'Local Files', 'dark', icon='localfiles')
    f.chip(432, 888, 213, 52, 'Toolpath Preview', 'lgreen', icon='toolpath')
    f.chip(400, 970, 188, 54, 'USB Drive', 'lgreen', icon='usb_up')
    f.chip(328, 1055, 188, 52, 'SD Card', 'green', icon='sdcard')
    f.chip(233, 1125, 188, 52, 'Load File', 'mgreen', icon='loadfile')
    W, H = 143, 45
    for k, t in enumerate(['Preview', 'Open', 'New', 'Select', 'Rename']):
        f.chip([678, 860, 1037, 1216, 1400][k], 505, W, H, t)
    for k, t in enumerate(['Delete', 'Copy', 'Paste', 'Cut']):
        f.chip([678, 860, 1037, 1216][k], 578, W, H, t)
    f.tri(750, 483, 'up')
    f.chip(678, 418, W, H, 'Close')
    f.chip(678, 362, W, H, 'Edit')
    f.tri(930, 483, 'up')
    f.chip(855, 415, W, H, 'Edit Program')
    f.tri(930, 393, 'up')
    for k, t in enumerate(['Save', 'Copy', 'Cut', 'Paste', 'Close', 'Find/Replace', 'Select']):
        f.chip(858, k * 54.6, W, H, t)
    f.tri(1025, 293, 'right')
    for k, t in enumerate(['Find Content', 'Find Line', 'Replace']):
        f.chip(1050, 217 + k * 55, W, H, t)
    G = 'lgreen'
    f.chip(678, 1040, W, H, 'Start', G)
    f.chip(678, 1097, W, H, 'Single Step', G)
    for k, t in enumerate(['Reset', 'Front View', 'Top View', 'Left View', 'Zoom In', 'Zoom Out']):
        f.chip(860, 681 + k * 54.4, W, H, t, G)
    f.tri(933, 1020, 'up', kind='dark')
    f.chip(860, 1040, W, H, 'View', G)
    f.chip(860, 1097, W, H, 'Override', G)
    f.tri(933, 1162, 'down')
    f.chip(860, 1182, W, H, 'Override +', G)
    f.chip(860, 1237, W, H, 'Override −', G)
    for k, t in enumerate(['Pan X+', 'Pan X−', 'Pan Y+', 'Pan Y−']):
        f.chip(1037, 790 + k * 54.4, W, H, t, G)
    f.tri(1110, 1020, 'up')
    f.chip(1037, 1040, W, H, 'Pan', G)
    f.chip(1037, 1097, W, H, 'Tool Axis Vector', G)
    for k, t in enumerate(['Rotate X+', 'Rotate X−', 'Rotate Y+', 'Rotate Y−', 'Rotate Z+', 'Rotate Z−']):
        f.chip(1216, 681 + k * 54.4, W, H, t, G)
    f.tri(1290, 1017, 'up')
    f.chip(1216, 1040, W, H, 'Rotate', G)
    f.chip(1216, 1097, W, H, 'Close', G)
    for k, t in enumerate(['Preview', 'Open', 'New', 'Select', 'Rename']):
        f.chip([678, 860, 1037, 1216, 1400][k], 1338, W, H, t, G)
    for k, t in enumerate(['Delete', 'Copy', 'Paste', 'Cut']):
        f.chip([678, 860, 1037, 1216][k], 1395, W, H, t, G)
    return f


# ---------------------------------------------------------------- system
def fc5():
    f = Flow(1425, 1181)
    f.line([(570, 347), (570, 22), (870, 22)])
    f.line([(690, 429), (690, 155), (870, 155)])
    f.line([(795, 533), (860, 533)])
    f.bracket(860, 375, 680)
    f.line([(805, 642), (805, 1005), (870, 1005)], 'lgreen')
    f.line([(738, 722), (738, 1085), (870, 1085)], 'lgreen')
    f.line([(570, 882), (570, 1162), (870, 1162)], 'dgreen')
    f.hub(395, 610, 182, 'Система', 'dggggg', [(398, 458, 'dark'), (482, 458, 'dark'), (527, 528, 'dark'), (572, 610, 'green'),
                                              (533, 692, 'green'), (482, 770, 'green'), (395, 770, 'green'), (312, 770, 'green'),
                                              (265, 697, 'dgreen')], fs=40)
    for x, y, w, t, k, ic in [(458, 345, 202, 'Alarm Info', 'dark', 'alarm_info'), (530, 427, 208, 'Alarm History', 'dark', 'alarm_hist'),
                              (598, 507, 197, 'Monitor Data', 'dark', 'monitor'), (645, 588, 188, 'Machine Config', 'lgreen', 'mach_config'),
                              (598, 668, 190, 'HMI Settings', 'lgreen', 'hmi_set'), (530, 748, 188, 'Axis Calib.', 'green', 'axis_calib'),
                              (452, 828, 185, 'Update Center', 'green', 'update'), (245, 828, 185, 'Machine Calib.', 'dgreen', 'mach_calib'),
                              (68, 748, 187, 'Probe Pairing', 'dgreen', 'probe_pair')]:
        f.chip(x, y, w, 52, t, k, icon=ic)
    W, H = 143, 45
    f.chip(878, 0, W, H, 'Clear Alarms')
    f.chip(878, 135, W, H, 'Export')
    for k, t in enumerate(['Digital IO', 'Analog IO', 'Drive', 'Probe', 'Oscilloscope']):
        f.chip(878, [352, 432, 505, 580, 655][k], W, H, t)
    f.tri(1045, 678, 'right')
    for y, t, w in [(352, 'Sampling Setup', 143), (427, 'Start Monitoring', 143), (503, 'Pointer A / Pointer B', 168),
                    (578, 'Pointer Left', 143), (653, 'Pointer Right', 143), (728, 'View', 143)]:
        f.chip(1075 if w == 143 else 1062, y, w, H, t)
    f.tri(1245, 755, 'right')
    for k, t in enumerate(['X Axis', 'Axis Zoom In', 'Axis Zoom Out', 'Axis Left', 'Axis Right', 'Auto Fit', 'Sample Points']):
        f.chip(1272, 427 + k * 75.5, W, H, t)
    f.chip(878, 983, W, H, 'Save', 'lgreen')
    f.chip(1075, 983, W, H, 'Reset', 'lgreen')
    for k, t in enumerate(['Export Log', 'Clear Data', 'Reset Params']):
        f.chip([878, 1075, 1278][k], 1063, W, H, t, 'lgreen')
    for k, t in enumerate(['Online Update', 'USB Update', 'Network Config']):
        f.chip([878, 1075, 1278][k], 1138, W, H, t, 'dgreen')
    return f


if __name__ == '__main__':
    for n, fn in [('fc1', fc1), ('fc2', fc2), ('fc3', fc3), ('fc4', fc4), ('fc5', fc5)]:
        (HERE / f'{n}.svg').write_text(fn().svg())
    print('flowcharts ok')
