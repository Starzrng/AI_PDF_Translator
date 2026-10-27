"""Every redrawn HMI screen / fragment of the manual, keyed by name.
SRC maps a screen to the original raster it replaces (for side-by-side QA)."""
from kit import *

SCREENS, SRC = {}, {}


def reg(name, src=None):
    def deco(fn):
        SCREENS[name] = fn
        SRC[name] = src
        return fn
    return deco


AUTO_CODE = [(28, 'N25 X24.568 Y-24.567'), (29, 'N26 X-24.567'), (30, 'N27 Y24.567'), (31, 'N28 X24.566'),
             (32, 'N29 X22.979 Y22.98'), (33, 'N30 X22.981 Y-22.98')]


@reg('auto_classic', 'p026_x620.png')
def auto_classic():
    return screen(top('AUTO', 'Auto', 0), coords(), tfs(), program(lines=AUTO_CODE, sel=5),
                  msgbar('File loaded successfully'), side(SIDE_AUTO, 0), bottom(BOT_AUTO))


@reg('auto_graphic', 'p027_x89.png')
def auto_graphic():
    g54 = ''.join(f'<div class="crow" style="top:{i * 57}px;height:57px"><span class="ax" style="color:#d4d4d4;font-size:29px;top:9px">{a}</span>'
                  f'<span class="cv mono g" style="left:0;width:244px;top:11px">{v}</span></div>'
                  for i, (a, v) in enumerate([('X', '12.540'), ('Y', '12.541'), ('Z', '-1.960'), ('A', '0.000'), ('C', '0.000')]))
    mach = ''.join(f'<div class="crow" style="top:{i * 58}px;height:58px"><span class="ax" style="color:#d4d4d4;font-size:29px;top:9px">{a}</span>'
                   f'<span class="cv mono" style="left:0;width:248px;top:11px;color:#a8d26d">{v1}</span>'
                   f'<span class="cv mono" style="left:0;width:454px;top:11px;color:#a8d26d">{v2}</span></div>'
                   for i, (a, v1, v2) in enumerate([('X', '-52.418', '-0.715'), ('Y', '-96.418', '-0.715'), ('Z', '-98.960', '-0.000'),
                                                    ('A', '0.000', '-0.000'), ('C', '0.000', '0.000')]))
    tfs_row = (at(0, 290, '', 'width:100%;height:1px;background:#3a3b40')
               + at(16, 302, '<span class="ax" style="position:static;color:#d4d4d4;font-size:29px">T</span>')
               + at(0, 302, '<span class="mono blue" style="font-size:29px">#2</span>', 'width:150px;text-align:right')
               + at(165, 296, '', 'width:1px;height:48px;background:#45474b')
               + at(180, 302, '<span class="ax" style="position:static;color:#d4d4d4;font-size:29px">F</span>')
               + at(0, 302, '<span class="mono g" style="font-size:29px">1000</span>', 'width:302px;text-align:right')
               + at(316, 296, '', 'width:1px;height:48px;background:#45474b')
               + at(330, 302, '<span class="ax" style="position:static;color:#d4d4d4;font-size:29px">S</span>')
               + at(0, 302, '<span class="mono g" style="font-size:29px">10000</span>', 'width:470px;text-align:right'))
    tool_tbl = ''.join(f'<div class="crow" style="top:{i * 56}px;height:56px"><span class="ax" style="color:#d4d4d4;font-size:28px;top:8px">{a}</span>'
                       f'<span class="cv mono {c}" style="left:0;width:244px;top:10px">{v}</span></div>'
                       for i, (a, v, c) in enumerate([('T', '#2', 'blue'), ('D', '0.000', 'g'), ('H', '-70.000', 'g')]))
    timebox = (at(18, 34, '<span style="color:#8cc63f;font-size:20px">▶</span>')
               + at(56, 30, '<span class="mono" style="font-size:22px;color:#a8d26d">[164/14247]</span>')
               + at(56, 62, '<span class="mono" style="font-size:29px;color:#d0d0d0">1-(2)-D3.175.NC</span>')
               + at(0, 44, '<span class="mono g" style="font-size:34px">1%</span>', 'width:484px;text-align:right')
               + at(18, 122, ico('clock', 22, 22, '#cfcfcf') + '<span class="mono" style="font-size:21px;color:#cfcfcf;margin-left:14px">00:03:40</span>', 'display:flex;align-items:center')
               + at(330, 122, ico('clock', 22, 22, '#cfcfcf') + '<span class="mono" style="font-size:21px;color:#cfcfcf;margin-left:14px">05:17:49</span>', 'display:flex;align-items:center')
               + at(0, 110, '', 'width:100%;height:1px;background:#3a3b40')
               + box('abs', 14, 166, 472, 52, '<i style="display:block;width:3px;height:100%;background:#8cc63f"></i>', 'background:#2c2e33'))
    over = (at(0, 70, gauge(150, 150, 100, 0, 120, '#6aad2e', 'Feed Rate'), 'width:300px;height:300px')
            + at(30, 440, '', 'width:240px;height:1px;background:#4a4a4a')
            + at(0, 430, gauge(150, 150, 100, 50, 120, '#3c6fe0', 'Spindle Speed'), 'width:300px;height:300px'))
    return screen(top('AUTO', 'Auto', 0),
                  panel(3, 64, 292, 352, 'G54', box('inner', 16, 46, 260, 290, g54)),
                  panel(3, 422, 292, 376, 'Current Tool:',
                        at(40, 80, img('endmill.png', 'width:210px')) + at(0, 150, 'Neck End Mill', 'width:290px;text-align:center;font-size:17px;color:#cfcfcf')
                        + box('inner', 16, 190, 260, 170, tool_tbl)),
                  panel(300, 64, 535, 432, 'Machining', box('inner', 16, 46, 502, 370, mach + tfs_row)),
                  panel(300, 502, 535, 296, 'Machining Time', box('inner', 16, 42, 502, 230, timebox)),
                  panel(840, 64, 298, 734, 'Override', over),
                  side([('classic', 'Classic View'), ('graphic', 'Graphic View'), ('guide', 'Guide View')], 1))


@reg('jog_guide', 'p028_x95.png')
def jog_guide():
    steps = ['Home machine axes, empty the tool magazine', 'Select the G-code file to machine', 'Install the workpiece',
             'Load additional tools as the job requires', 'Workpiece positioning', 'Ready — start machining']
    st = ''.join(at(80, 228 + i * 53, f'<span style="display:inline-flex;width:26px;height:26px;border-radius:50%;background:#5b5b5b;color:#cfcfcf;'
                                      f'align-items:center;justify-content:center;font-size:16px;margin-right:16px">{i + 1}</span>'
                                      f'<span style="font-size:18px;color:#d6d6d6">{s}</span>', 'display:flex;align-items:center')
                 + (at(92, 256 + i * 53, '', 'width:1px;height:22px;background:#6a6a6a') if i < 5 else '')
                 for i, s in enumerate(steps))
    body = (at(470, 172, img('guide_bg.png', 'width:540px;opacity:.95'))
            + at(22, 18, ico('guide', 30, 30, '#5a5a5a') + '<span style="font-size:21px;color:#d0d0d0;margin-left:14px">Machining Guide</span>', 'display:flex;align-items:center')
            + at(22, 68, '', 'width:1095px;height:1px;background:#5a5a5a')
            + at(46, 116, '<span style="color:#7ec242;font-size:18px;line-height:1.6">• Welcome to the Machining Guide! In a few simple steps you can easily machine a workpiece.<br>'
                          '&nbsp;&nbsp;The steps you are about to take:</span>', 'width:900px')
            + st
            + at(66, 568, '<span style="font-size:17.5px;color:#d0d0d0">Follow the prompts. If you have any questions, use <span style="color:#7ec242">“Help”</span> for details at any time.</span>')
            + at(22, 655, '', 'width:1095px;height:1px;background:#5a5a5a')
            + box('abs', 942, 672, 160, 48, 'Start', 'background:#5c9829;border:2px solid #86c94e;color:#fff;font-size:21px;display:flex;align-items:center;justify-content:center'))
    return screen(top('JOG', '', 0), box('panel', 3, 64, 1135, 734, body, 'background:#3a3a3a'),
                  side([('classic', 'Classic View'), ('graphic', 'Graphic View'), ('guide', 'Guide View')], 2))


@reg('jog_tsm', 'p031_x132.png')
def jog_tsm():
    form = (field(14, 'Select Tool', '#2', lw=170) + field(66, 'Spindle Speed', lw=170)
            + field(118, 'Spindle M Code', 'M03', dropdown=True, lw=170) + field(170, 'Select Offset', lw=170))
    return screen(top('JOG', 'Handwheel', 0), coords(COORDS_JOG), tfs(F='0', S='0'),
                  lower('TSM', form, icon=('tsm_t', '#3d7df2')),
                  msgbar('Please select the step distance', right='Handwheel'),
                  side(SIDE_JOG, 3), bottom(BOT_JOG))


@reg('jog_workpos', 'p032_x150.png')
def jog_workpos():
    tiles = ''.join(box('tile', 40 + i * 176, 34, 158, 158, img(f'../icons/{ic}.png', 'height:52px') + f'<span>{t}</span>')
                    for i, (ic, t) in enumerate([('tile_single', 'Single Axis'), ('tile_cuboid', 'Cuboid'), ('tile_cylinder', 'Cylinder')]))
    return screen(top('JOG', 'Handwheel', 0), coords(COORDS_JOG), tfs(F='0', S='0'),
                  lower('Workpiece Positioning', tiles),
                  msgbar('Please select the positioning type', right='Handwheel'),
                  side(SIDE_JOG, 4),
                  bottom([('single', 'Single Axis'), ('cuboid', 'Cuboid'), ('cylinder', 'Cylinder')]))


@reg('jog_toolmeasure', 'p034_x179.png')
def jog_toolmeasure():
    form = (field(12, 'Tool No. T', '#2', sm=True, lw=150) + field(58, 'Tool Length H', '-70.000', sm=True, lw=150)
            + field(104, 'Rad. Comp. RS', '0.000', sm=True, lw=150))
    return screen(top('JOG', 'Handwheel', 0), coords(COORDS_JOG), tfs(F='0', S='0'),
                  lower('Tool Measure', form), msgbar('', right='Handwheel'),
                  side(SIDE_JOG, 5), bottom([('seltool', 'Select Tool'), ('toolset', 'Tool Setting'), ('probecal', 'Probe Calib.')]))


@reg('mdi', 'p035_x189.png')
def mdi():
    lines = ''.join(at(14, 10 + i * 38, f'<span style="font-size:19px;color:#bdbdbd;display:inline-block;width:34px">{i + 1}</span>'
                                        f'<span style="font-size:24px;color:#d8d8d8">{c}</span>') for i, c in enumerate(['G01 X40 F500', '', '']))
    W = [('X', '40.000', '0.000'), ('Y', '32.239', '0.000'), ('Z', '167.000', '0.000'), ('A', '0.000', '0.000'), ('C', '0.000', '0.000')]
    return screen(top('MDI', 'MDI', 0), coords(W, 'Work Coord.', 'G54'), tfs(F='0', S='0'),
                  lower('MDI', lines, inner_style='border:2px solid #8cc63f'),
                  msgbar('Switched to the work coordinate system!'), side(SIDE_MDI, 0), bottom(BOT_AUTO))


# ---------------------------------------------------------------- fragments
@reg('frag_prompt', 'p025_x77.png')
def frag_prompt():
    return screen(at(0, 0, '<span style="font-size:13px">●</span><span>Homing is available only in Manual mode — switch to Manual mode</span>',
                     'width:100%;height:100%;display:flex;align-items:center;gap:12px;padding-left:12px;font-size:17px;font-weight:700;color:#ff9b21'),
                  w=640, h=34, bg="#252627")


@reg('frag_alarm', 'p025_x78.png')
def frag_alarm():
    return screen(at(0, 0, 'NC50038: Illegal character [Line: 7]',
                     'width:100%;height:100%;display:flex;align-items:center;padding-left:10px;font-size:17px;font-weight:700;color:#ff3b30'),
                  w=320, h=34, bg='#262222')


@reg('frag_fbar', 'p054_x380.png')
def frag_fbar():
    return screen(box('tfs-l', 0, 0, 60, 63, '<b>F</b><small>Feed<br>Rate</small>'),
                  at(60, 13, '<span class="mono g" style="font-size:30px">0</span>', 'width:150px;text-align:center'),
                  at(222, 20, '<span class="mono" style="font-size:16px;color:#6f6f6f">mmpm</span>'),
                  box('abs', 302, 6, 1, 50, '', 'background:#43464b'),
                  at(320, 6, '<span class="mono" style="font-size:16px;color:#cfcfcf">90%</span>', 'width:190px;text-align:right'),
                  f'<div class="bar" style="left:322px;top:34px;width:190px"><i style="width:76%"></i></div>',
                  w=520, h=63, bg='#24272b')


@reg('frag_ruby', 'p035_x185.png')
def frag_ruby():
    f = (field(52, 'Tool No. T', '#8', sm=True, lw=150, x=12) + field(98, 'Tool Length H', '-84.471', sm=True, lw=150, x=12)
         + field(144, 'Rad. Comp. RS', '0.000', sm=True, lw=150, x=12)
         + field(190, '<b style="color:#e8e8e8">Ruby Radius</b>', '<b style="color:#fff">0.75</b>', sm=True, lw=150, x=12)
         + box('abs', 6, 181, 290, 52, '', 'border:2px solid #e02020'))
    return screen(at(12, 8, 'Tool Measure', 'font-size:18px;color:#c9c9c9'), box('abs', 0, 36, 380, 1, '', 'background:#555'),
                  f, w=380, h=244, bg='#2f3034')


if __name__ == '__main__':
    print(list(SCREENS))


# ================================================================ chapter 1 / 3 page screens
TOOLS = [('Spindle', '8', 'probe', 'Probe', '-75.0000', '0.0000'),
         ('1', '1', 'endmill', 'End Mill', '-45.0000', '0.0000'),
         ('2', '2', 'taper_ball', 'Tapered Ball Mill', '-39.9853', '0.0000'),
         ('3', '3', 'taper_ball2', 'Tapered Ball Mill', '0.0000', '0.0000'),
         ('4', '4', 'ball', 'Ball End Mill', '0.0000', '0.0000'),
         ('5', '5', 'reamer', 'Reamer', '9.0000', '0.0000'),
         ('6', '6', 'bullnose', 'Bull Nose Mill', '0.0000', '0.0000')]
SIDE_TOOLS = [('toollist', 'Tool List'), ('seloffset', 'Offsets'), None, None, None, None, ('control', 'Control Panel')]
BOT_TOOLS = ['^', 'v', ('details', 'Details'), None, None, ('toolchange', 'Tool Change'),
             ('spindle_rel', 'Spindle Release'), ('mag_out', 'Magazine Out')]


def tools_page(sel=0, mode=('JOG', 'Handwheel'), msg=''):
    hd = 'font-size:16.5px;color:#a9a9a9;font-weight:700'
    head = (at(40, 14, 'Slot', hd) + at(134, 14, 'Tool No.', hd) + at(400, 14, 'Tool Type', hd)
            + at(0, 14, 'Tool Length (H)', hd + ';width:752px;text-align:right')
            + at(0, 14, 'Rad. Comp. (RS)', hd + ';width:888px;text-align:right') + at(948, 14, 'Loaded', hd))
    rows = []
    for i, (slot, no, pic, typ, h, rs) in enumerate(TOOLS):
        s = i == sel
        bg = 'background:#4773e5;' if s else ''
        num = '#fff' if s else '#8cc63f'
        val = '#fff' if s else '#5d6168'
        rows.append(box('abs', 0, i * 53, 1096, 52,
                        at(0, 12 if slot == 'Spindle' else 11, slot, f'width:84px;text-align:center;font-size:{20 if slot == "Spindle" else 23}px;color:{"#fff" if s else "#888"};font-weight:700')
                        + at(0, 11, no, f'width:300px;text-align:center;font-size:23px;color:{num};font-weight:700')
                        + at(262, 8, img(f'tool_{pic}.png', 'height:36px'))
                        + at(420, 15, typ, f'font-size:17px;color:{"#fff" if s else "#9a9a9a"}')
                        + at(0, 11, h, f'width:730px;text-align:right;font-size:24px;color:{val}', 'abs mono')
                        + at(0, 11, rs, f'width:866px;text-align:right;font-size:24px;color:{val}', 'abs mono')
                        + at(966, 11, '✓', 'font-size:22px;color:#8cc63f'),
                        bg + 'border-bottom:1px solid #3a3d42'))
    inner = box('inner', 18, 50, 1100, 540, box('abs', 2, 2, 1096, 536, ''.join(rows)))
    return screen(top(mode[0], mode[1], 1), box('panel', 3, 64, 1135, 604, head + inner),
                  msgbar(msg, right='Handwheel', right2=('1X', True)), side_any(SIDE_TOOLS, 0), bottom_any(BOT_TOOLS))


@reg('tools_list', 'p036_x195.png')
def tools_list():
    return tools_page()


FILES_A48 = [('folder', '.', '', '', ''), ('folder', 'A48', '', 'Folder', '2024-12-10 17:15:48'),
             ('folder', 'NewFolder1', '', 'Folder', '2024-10-26 17:38:14'),
             ('NC', '1(2).NC', '0 B', 'NC file', '2024-10-18 10:03:09'),
             ('TAP', '1-(2)-d3.175(2).tap', '204.0 KB', 'TAP file', '2024-10-24 15:56:45'),
             ('TAP', '1-(2)-d3.175.tap', '204.0 KB', 'TAP file', '2023-05-18 11:02:45'),
             ('NC', '1-T1-D4(1)(2).NC', '188.0 KB', 'NC file', '2024-11-04 19:59:44'),
             ('NC', '1-T1-D4.NC', '113.0 KB', 'NC file', '2023-05-18 09:40:59'),
             ('NC', '1.NC', '0 B', 'NC file', '2024-10-17 14:54:03')]
SIDE_PROG = [('localfiles', 'Local Files'), ('usb', 'USB Drive'), ('sdcard', 'SD Card'), ('progedit', 'Edit Program'),
             ('loadfile', 'Load File'), None, None]
BOT_PROG = ['^', 'v', ('preview', 'Preview'), ('new', 'New'), ('open', 'Open'), ('select', 'Select'), None, ('next', 'Next Page')]


def files_page(rows=FILES_A48, sel=1, path='Local NC Files &gt; A48', mode=('JOG', 'Handwheel'), side=SIDE_PROG,
               side_on=0, bottom=BOT_PROG, red=7, right='', msg='', big=True):
    hd = 'font-size:16.5px;color:#8f8f8f;font-weight:700'
    fs = 22 if big else 19
    head = (at(18, 10, ico('localfiles', 20, 18, '#777') + f'<span style="margin-left:8px">{path}</span>',
               'display:flex;align-items:center;font-size:16px;color:#7d7d7d')
            + at(70, 44, 'Name', hd) + at(0, 44, 'Size', hd + ';width:782px;text-align:right')
            + at(818, 44, 'Type', hd) + at(0, 44, 'Modified', hd + ';width:1100px;text-align:right'))
    rr = []
    for i, (k, name, size, typ, date) in enumerate(rows):
        s = i == sel
        icon = folder_svg(30) if k == 'folder' else file_svg(k, 24)
        c = '#fff' if s else '#e0e0e0'
        tri_ = '<span style="position:absolute;left:12px;top:19px;border-top:6px solid transparent;border-bottom:6px solid transparent;border-left:8px solid #9aa"></span>' if (s or (k == 'folder' and name not in ('.',))) and big else ''
        rr.append(box('abs', 0, i * 60, 1080, 59,
                      tri_ + at(36, 15, icon) + at(84, 14, name, f'font-size:{fs}px;color:{c};font-weight:{700 if s else 600}')
                      + at(0, 18, size, f'width:746px;text-align:right;font-size:17px;color:{c}')
                      + at(782, 18, typ, f'font-size:17px;color:{c}')
                      + at(0, 18, date, f'width:1064px;text-align:right;font-size:17px;color:{c}'),
                      ('background:#4773e5;' if s else '') + 'border-bottom:1px solid #33363b'))
    inner = box('inner', 18, 72, 1100, 520, box('abs', 4, 4, 1080, 512, ''.join(rr))
                + box('abs', 1086, 4, 10, 120, '', 'background:#4a4b50;border-radius:3px'), 'overflow:hidden')
    return screen(top(mode[0], mode[1], 2), box('panel', 3, 64, 1135, 604, head + inner),
                  msgbar(msg, right=right or None), side_any(side, side_on), bottom_any(bottom, red=red))


@reg('prog_files', 'p038_x227.png')
def prog_files():
    return files_page()


def radio(on):
    if on:
        return '<span style="display:inline-block;width:18px;height:18px;border-radius:50%;border:4px solid #8cc63f;background:#2b2e33;margin-right:10px;vertical-align:-3px"></span>'
    return '<span style="display:inline-block;width:18px;height:18px;border-radius:50%;background:#8a8a8a;margin-right:10px;vertical-align:-3px"></span>'


SIDE_SYS_HMI = [('mach_calib', 'Machine Calib.'), ('axis_calib', 'Axis Calib.'), ('probe_pair', 'Probe Pairing'),
                ('update', 'Update Center'), None, None, ('prev', 'Previous Page')]
BOT_SYS_HMI = [('export_log', 'Export Log'), ('clear_data', 'Clear Data'), ('reset_params', 'Reset Params')]


def sys_hmi_page(mode=('JOG', 'Handwheel')):
    lab = 'font-size:17px;color:#a8a8a8'
    val = 'font-size:18px;color:#d8d8d8'

    def sec(y, icon, title):
        return box('abs', 22, y, 1056, 36, at(14, 8, ico(icon, 16, 16, '#888') + f'<span style="margin-left:12px">{title}</span>',
                                                'display:flex;align-items:center;font-size:17.5px;color:#d0d0d0;font-weight:700'),
                   'background:#2d3137')
    b = (sec(14, 'aux', 'About Device')
         + at(56, 62, 'Serial Number:', lab) + at(56, 96, 'Software Version:', lab) + at(250, 95, 'V1.0.0', val)
         + at(56, 130, 'Firmware Version:', lab) + at(250, 129, 'V1.0.0', val)
         + sec(168, 'tab_system', 'Basic Settings')
         + at(56, 216, 'Language', lab) + at(250, 215, radio(False) + 'Chinese (Simplified)', val) + at(520, 215, radio(True) + 'English', val)
         + at(56, 250, 'Units', lab) + at(250, 249, radio(True) + 'mm', val) + at(520, 249, radio(False) + 'inch', val)
         + at(56, 284, 'Display Precision', lab) + at(250, 283, radio(True) + '0.0001', val) + at(520, 283, radio(False) + '0.001', val)
         + sec(322, 'tab_system', 'Preferences')
         + at(56, 374, 'Magazine Slots', lab) + box('fin', 250, 364, 300, 38, '6', 'position:absolute')
         + at(56, 420, 'Brightness', lab) + box('fin', 250, 410, 300, 38, 'High<span class="chv"></span>', 'position:absolute')
         + at(56, 466, 'Time', lab) + box('fin', 250, 456, 300, 38, '2024-12-31 15:20:19', 'position:absolute')
         + at(56, 510, 'Startup Guide <span style="display:inline-block;width:18px;height:18px;border-radius:50%;background:#bbb;color:#333;font-size:13px;text-align:center;line-height:18px">?</span>', lab)
         + box('abs', 250, 506, 52, 28, '<i style="position:absolute;right:3px;top:3px;width:22px;height:22px;border-radius:50%;background:#fff"></i>',
               'background:#6aaa3a;border-radius:14px'))
    return screen(top(mode[0], mode[1], 3), box('panel', 3, 64, 1135, 604, box('inner', 18, 16, 1100, 572, b)),
                  msgbar(''), side_any(SIDE_SYS_HMI, None, red=6), bottom_any(BOT_SYS_HMI))


@reg('sys_hmi', 'p043_x305.png')
def sys_hmi():
    return sys_hmi_page()


@reg('boot', 'p014_x37.png')
def boot():
    return screen(f'<img src="{uri(HIMG / "boot_bg.png")}" style="position:absolute;left:0;top:0;width:1280px;height:800px">',
                  at(420, 650, 'Initializing machine configuration...', 'font-size:17px;color:#e0e0e0;font-weight:600'))


@reg('jog_tsm2', 'p014_x38.png')
def jog_tsm2():
    form = (field(14, 'Select Tool', '#2', lw=170) + field(66, 'Spindle Speed', '500', lw=170)
            + field(118, 'Spindle M Code', 'M03', dropdown=True, lw=170) + field(170, 'Select Offset', 'G54', lw=170))
    c = [('X', '-97.245', '0.000'), ('Y', '-49.704', '0.000'), ('Z', '0.000', '0.000'), ('A', '0.000', '0.000'), ('C', '0.000', '0.000')]
    return screen(top('JOG', 'Handwheel', 0), coords(c), tfs(F='0', S='0'),
                  lower('TSM', form, icon=('tsm_t', '#3d7df2')), msgbar('', right='Handwheel'),
                  side(SIDE_JOG, 3), bottom(BOT_JOG + [('auxaxis', 'Aux Axis')]))


@reg('keyboard', 'p020_x56.png')
def keyboard():
    K = 'position:absolute;display:flex;align-items:center;justify-content:center;background:linear-gradient(#4b4b4b,#3f3f3f);border:1px solid #5a5a5a;color:#f0f0f0;font-family:Barlow;font-weight:700'
    rows = ['ABCDEF', 'GHIJKL', 'MNOPQR', 'STUVWX']
    h = [at(10, 10, 'Full Keyboard', 'font-size:15px;color:#cfcfcf;font-weight:700'),
         box('abs', 312, 6, 30, 26, '✕', 'background:#d9382f;color:#fff;font-size:17px;display:flex;align-items:center;justify-content:center')]
    kw, kh, x0, y0, gx, gy = 54, 39, 2, 43, 58, 43
    for r, s in enumerate(rows):
        for c, ch in enumerate(s):
            h.append(f'<div style="{K};left:{x0 + c * gx}px;top:{y0 + r * gy}px;width:{kw}px;height:{kh}px;font-size:24px">{ch}</div>')

    def key(c, r, t, w=1, hh=1, bg=None, fs=24):
        st = f'background:{bg};border-color:{bg};' if bg else ''
        return (f'<div style="{K};{st}left:{x0 + c * gx}px;top:{y0 + r * gy}px;width:{kw + (w - 1) * gx}px;'
                f'height:{kh + (hh - 1) * gy}px;font-size:{fs}px">{t}</div>')
    for c, t in enumerate(['7', '8', '9', 'Y', 'Z']):
        h.append(key(c, 4, t))
    h.append(key(5, 4, '⌫', bg='#d9382f'))
    for c, t in enumerate(['4', '5', '6']):
        h.append(key(c, 5, t))
    h += [key(3, 5, '␣', hh=2, bg='#3f6ff0', fs=26), key(4, 5, 'A/a', fs=15), key(5, 5, 'Shift', bg='#3f6ff0', fs=15)]
    for c, t in enumerate(['1', '2', '3']):
        h.append(key(c, 6, t))
    h += [key(4, 6, '↑'), key(5, 6, 'Enter', bg='#5c9829', fs=15)]
    for c, t in enumerate(['−', '0', '.', '←', '↓', '→']):
        h.append(key(c, 7, t))
    return screen(*h, w=349, h=388, bg='#2f2f2f')


# ================================================================ chapter 1 annotated figures
ERR_MSG = ('<span style="display:inline-flex;align-items:center;gap:6px;border:1.5px solid #e0302a;border-radius:3px;padding:1px 6px;color:#ff3b30">'
           '<span class="dot red" style="width:13px;height:13px"></span>Error</span>'
           '<span style="color:#ff3b30;margin-left:10px;font-weight:700">NC50006: Please reopen the file</span>')


@reg('ann_main', 'p016_x44.png')
def ann_main():
    z = [('X', '0.000', '0.000'), ('Y', '0.000', '0.000'), ('Z', '0.000', '0.000'), ('A', '0.000', '0.000'), ('C', '0.000', '0.000')]
    code = [(1, '%'), (2, 'G17 G21 G40 G49 G80 G90 G94'), (3, 'G91 G28 Z0'), (4, 'G91 G28 X0 Y0'), (5, 'G90 G53 G0 A0 C0'), (6, 'T5 M6')]
    scr = screen(top('AUTO', 'Auto', 0, dot='red', msg=ERR_MSG), coords(z),
                 tfs(T='#8', D='2', H='-75.000', F='0', S='0', fpct=0, spct=80, tool='Probe', pic='tool_probe.png'),
                 program('Local NC Files &gt; 5_1-(5)-Q1.nc', '1/109288', code, 0),
                 msgbar('When an error alarm occurs, reset before switching to Manual mode'),
                 side(SIDE_AUTO, 0), bottom_any(BOT_AUTO, red=7))
    fr = [(2, 2, 805, 57, 'green'), (808, 2, 470, 57, 'orange'), (2, 64, 568, 312, 'blue'), (575, 64, 563, 312, 'blue'),
          (2, 380, 1136, 290, 'blue'), (2, 672, 1137, 43, 'dgreen'), (2, 717, 1138, 81, 'purple'),
          (1142, 62, 136, 185, 'purple'), (1142, 250, 136, 548, 'purple')]
    bd = [(1, 404, -36, 'green', (404, 2)), (2, 1040, -36, 'orange', (1040, 2)), (3, -62, 180, 'blue', (2, 180)),
          (4, -62, 252, 'blue', (575, 252)), (5, -62, 520, 'blue', (2, 520)), (6, -62, 693, 'dgreen', (2, 693)),
          (7, -62, 757, 'purple', (2, 757)), (8, 1342, 150, 'purple', (1278, 150)), (9, 1342, 470, 'purple', (1278, 470))]
    return annotate(scr, fr, bd)


def _ann_std(scr):
    fr = [(2, 2, 790, 57, 'green'), (794, 2, 346, 57, 'orange'), (1142, 2, 136, 57, 'orange'),
          (1142, 62, 136, 736, 'purple'), (2, 64, 1137, 604, 'blue'), (2, 672, 1137, 43, 'dgreen'), (2, 717, 1138, 81, 'purple')]
    bd = [(1, 396, -36, 'green', (396, 2)), (2, 1140, -36, 'orange', (1140, 2)), (3, 1342, 110, 'purple', (1278, 110)),
          (4, -62, 757, 'purple', (2, 757)), (5, -62, 330, 'blue', (2, 330)), (6, -62, 693, 'dgreen', (2, 693))]
    return annotate(scr, fr, bd)


@reg('ann_tools', 'p017_x47.png')
def ann_tools():
    return _ann_std(tools_page())


FILES_P18 = [('folder', 'test', '', 'Folder', '2024-01-13 04:16:38'), ('folder', 'testFile', '', 'Folder', '2023-11-18 17:28:17'),
             ('NC', '1-192976.132.NC', '119 KB', 'NC file', '2023-10-27 05:27:47'),
             ('NC', '1-T83917.NC', '126 KB', 'NC file', '2023-08-15 01:26:02'),
             ('NGC', '2-875T86.NGC', '820 KB', 'NGC file', '2023-08-07 11:47:20'),
             ('MPF', '3-28-T86.MPF', '240 KB', 'MPF file', '2023-06-24 21:57:45'),
             ('TXT', '3-8-T86.TXT', '72 KB', 'TXT file', '2023-05-16 15:57:41'),
             ('NC', '4-875T-86.NC', '2 KB', 'NC file', '2023-04-23 21:39:31'),
             ('TAP', '5-1221-T186.TAP', '12 KB', 'TAP file', '2023-03-10 15:42:41')]


@reg('ann_prog', 'p018_x50.png')
def ann_prog():
    sd = [('localfiles', 'Local Files'), None, None, ('progedit', 'Edit Program'), ('loadfile', 'Load File'),
          ('toolpath', 'Toolpath|Preview'), None]
    scr = files_page(FILES_P18, sel=3, path='Local NC Files &gt; Test &gt; 1-T1-D4.NC', mode=('AUTO', 'Single Block'),
                     side=sd, side_on=None, right='Single Block')
    return _ann_std(scr)


@reg('ann_sys', 'p019_x53.png')
def ann_sys():
    return _ann_std(sys_hmi_page())


@reg('panel_photo', 'p015_x41.png')
def panel_photo():
    patches = [(3, 198, 50, 232), (408, 16, 672, 46), (658, 104, 748, 134), (586, 157, 708, 188), (661, 201, 778, 230),
               (586, 249, 708, 280), (606, 296, 708, 325), (328, 374, 428, 402), (398, 416, 502, 445), (513, 416, 642, 445)]
    ox = 80
    lab = 'font-family:PT Sans;font-weight:700;font-size:21px;color:#f2f2f2;white-space:nowrap;line-height:1'
    labels = [(46, 202, 'Маховик', 'right'), (415, 21, 'Выбор главного меню (четыре меню интерфейса)', None),
              (665, 108, 'Кнопка аварийной остановки', None), (593, 162, 'Переключение режима обработки', None),
              (668, 206, 'Коррекция подачи', None), (593, 254, 'Коррекция шпинделя', None),
              (613, 300, 'Управление осями', None), (378, 380, 'Управление I/O', 'center'),
              (440, 420, 'Сброс (Reset)', 'right'), (548, 420, 'Пуск/пауза программы', None)]
    h = [f'<img src="{uri(ROOT / "extract" / "img" / "p015_x41.png")}" style="position:absolute;left:{ox}px;top:0;width:783px;height:445px">']
    for x0, y0, x1, y1 in patches:
        h.append(box('abs', ox + x0, y0, x1 - x0, y1 - y0, '', 'background:#393939'))
    for x, y, t, al in labels:
        if al == 'right':
            h.append(at(ox + x - 300, y, t, lab + ';width:300px;text-align:right'))  # right-aligned to x
        elif al == 'center':
            h.append(at(ox + x - 150, y, t, lab + ';width:300px;text-align:center'))
        else:
            h.append(at(ox + x, y, t, lab))
    return screen(*h, w=1120, h=452, bg='#393939')


# ================================================================ chapter 3.1.3 / 3.2–3.4
@reg('frag_mdi', 'p036_x194.png')
def frag_mdi():
    return screen(at(18, 10, 'MDI', 'font-size:20px;color:#c9c9c9;font-weight:700'),
                  box('inner', 16, 40, 380, 230, at(10, 8, '1', 'font-size:22px;color:#bdbdbd')
                      + box('abs', 40, 8, 340, 32, '', 'background:#4773e5'), 'border:2px solid #8cc63f'),
                  box('abs', 0, 292, 390, 42, '', 'background:#252627;border-top:1px solid #3a3a3a'),
                  w=390, h=334, bg='#373737')


@reg('prog_usb', 'p041_x286.png')
def prog_usb():
    sd = [('localfiles', 'Local Files'), ('usb', 'USB Drive'), ('sdcard', 'SD Card'), ('progedit', 'Edit Program'), ('loadfile', 'Load File'), None, None]
    return files_page(path='USB Drive &gt; A48', side=sd, side_on=1)


@reg('prog_sd', 'p041_x287.png')
def prog_sd():
    sd = [('localfiles', 'Local Files'), ('usb', 'USB Drive'), ('sdcard', 'SD Card'), ('progedit', 'Edit Program'), ('loadfile', 'Load File'), None, None]
    return files_page(path='SD Card &gt; A48', side=sd, side_on=2)


@reg('toolpath', 'p039_x245.png')
def toolpath():
    sd = [('localfiles', 'Local Files'), ('usb', 'USB Drive'), ('sdcard', 'SD Card'), ('progedit', 'Edit Program'),
          ('loadfile', 'Load File'), ('toolpath', 'Toolpath|Preview'), None]

    def chip(x, t, on=False):
        st = 'background:#5c9829;border:1px solid #86c94e;color:#fff' if on else 'background:#1d1e20;border:1px solid #333;color:#ddd'
        return box('abs', x, 108, 130, 30, f'<span style="font-size:9px;margin-right:6px">●</span>{t}',
                   st + ';display:flex;align-items:center;justify-content:center;font-size:13.5px;font-weight:700;white-space:nowrap')
    coord = ''
    for i, (a, v, u) in enumerate([('X', '68.69', 'mm'), ('Y', '108.93', 'mm'), ('Z', '63.4358', 'mm'), ('A', '0', 'deg'), ('C', '0', 'deg')]):
        x = 25 + i * 219
        coord += box('abs', x, 596, 217, 30, at(12, 3, a, 'font-size:19px;color:#c8302b;font-family:Barlow')
                     + at(0, 3, v, 'width:150px;text-align:right;font-size:19px;color:#8cc63f;font-weight:700')
                     + at(160, 5, u, 'font-size:16px;color:#5d6168'), 'background:#2b2e33')
    info = box('abs', 25, 628, 1093, 34, at(14, 5, 'N6717 G90 G53 G00 A0.0 C0.0', 'font-size:18px;color:#cfcfcf')
               + at(560, 7, 'Override: <b style="color:#ddd;margin-left:8px">50</b>', 'font-size:16px;color:#9a9a9a')
               + at(705, 7, 'Parsed: <b style="color:#ddd;margin-left:8px">6688</b>', 'font-size:16px;color:#9a9a9a')
               + at(880, 7, 'Max Lines:', 'font-size:16px;color:#9a9a9a')
               + at(0, 7, '<b style="color:#ddd">30000</b>', 'width:1085px;text-align:right;font-size:16px'), 'background:#2b2e33')
    body = (box('panel', 3, 64, 1135, 604, at(18, 12, ico('localfiles', 20, 18, '#777') + '<span style="margin-left:8px">Local NC Files &gt; 1-T1-D4(1).NC</span>',
                                             'display:flex;align-items:center;font-size:16px;color:#7d7d7d'))
            + chip(704, 'Finished', True) + chip(842, 'Tool Axis Vector') + chip(980, 'Single Step')
            + f'<img src="{uri(HIMG / "toolpath_view.png")}" style="position:absolute;left:25px;top:148px;width:1093px;height:447px">'
            + at(1020, 154, '⟳ 80%', 'font-size:20px;color:#e8e8e8;font-weight:700') + coord + info)
    bot = [('pan_xp', 'Pan Right'), ('pan_xm', 'Pan Left'), ('pan_yp', 'Pan Up'), ('pan_ym', 'Pan Down'), None, None, None, ('back', 'Back')]
    return screen(top('JOG', 'Handwheel', 2), body, msgbar(''), side_any(sd, 5), bottom_any(bot))


SIDE_SYS = [('alarm_info', 'Alarm Info'), ('alarm_hist', 'Alarm History'), ('monitor', 'Monitor Data'),
            ('update', 'Update Center'), None, None, ('next', 'Next Page')]
BOT_MON = [('dio', 'Digital IO'), ('aio', 'Analog IO'), ('drive', 'Drive'), ('probe', 'Probe'), ('scope', 'Oscilloscope')]


def led(on=True, color=None):
    c = color or ('#3fbf3f' if on else '#bdbdbd')
    return f'<span style="display:inline-block;width:18px;height:18px;border-radius:50%;background:radial-gradient(circle at 35% 35%,#fff8 0,{c} 55%)"></span>'


@reg('sys_dio', 'p042_x290.png')
def sys_dio():
    rows = [('Magazine In', 'DI', 1), ('Magazine Out', 'DI', 0), ('Spindle Release', 'DI', 0), ('Spindle Clamp', 'DI', 1)] + \
           [(f'Tool Slot {k}', 'DI', 1) for k in range(1, 7)]
    hd = 'font-size:16.5px;color:#a9a9a9;font-weight:700'
    rr = ''.join(box('abs', 0, i * 52, 1076, 51, at(16, 14, n, 'font-size:17px;color:#cfcfcf') + at(486, 14, t, 'font-size:17px;color:#cfcfcf')
                     + at(924, 16, led(v)), 'border-bottom:1px solid #3a3d42') for i, (n, t, v) in enumerate(rows))
    body = (at(18, 12, ico('tab_system', 16, 16, '#888') + '<span style="margin-left:10px">Monitor Data</span>', 'display:flex;align-items:center;font-size:16px;color:#9a9a9a')
            + at(36, 46, 'Signal Name', hd) + at(504, 46, 'Signal Type', hd) + at(890, 46, 'Signal State', hd)
            + box('inner', 18, 76, 1100, 516, rr, 'overflow:hidden'))
    return screen(top('MDI', 'MDI', 3), box('panel', 3, 64, 1135, 604, body), msgbar(''),
                  side_any(SIDE_SYS, 2), bottom_any(BOT_MON, active=0))


def probe_page(paired):
    st = [('Pairing Status', 'Paired' if paired else 'Not Paired'), ('Connection Status', 'Connected' if paired else 'Not Connected'),
          ('Probe Firmware', 'V1.0.0' if paired else '--'), ('Probe Serial No.', 'MS14920309' if paired else '--'),
          ('Receiver Firmware', 'V1.0.0' if paired else '--'), ('Receiver Serial No.', 'MS13381132' if paired else '--'),
          ('Battery Level', '100%' if paired else '--'), ('Probe Signal (DI)', led(False))]
    hd = 'font-size:16.5px;color:#a9a9a9;font-weight:700'
    rr = ''.join(box('abs', 8, i * 52, 788, 51, at(8, 14, n, 'font-size:17.5px;color:#cfcfcf') + at(626, 14, v, 'font-size:18px;color:#cfcfcf;font-weight:700'),
                     'border-bottom:1px solid #3a3d42') for i, (n, v) in enumerate(st))
    left = box('panel', 3, 64, 836, 604, at(18, 12, ico('tab_system', 16, 16, '#888') + '<span style="margin-left:10px">Probe Data</span>',
                                          'display:flex;align-items:center;font-size:16px;color:#9a9a9a')
               + at(36, 54, 'Parameter', hd) + at(658, 54, 'Status', hd) + box('inner', 18, 84, 802, 506, rr))
    stat = ('<span style="border:2px solid #7ec242;border-radius:14px;padding:2px 16px;color:#8cc63f">Connected</span>' if paired
            else '<span style="border:2px solid #aaa;border-radius:14px;padding:2px 16px;color:#cfcfcf">Not Connected</span>')
    batt = ('<div style="margin-top:12px;display:flex;align-items:center;justify-content:center;gap:10px;color:#cfcfcf;font-size:19px">'
            '<span style="display:inline-block;width:36px;height:18px;border:2px solid #8cc63f;padding:2px;box-sizing:border-box">'
            '<i style="display:block;height:100%;background:#8cc63f"></i></span>100%</div>' if paired else '')
    right = box('panel', 843, 64, 295, 604, at(18, 54, 'Probe Status', hd)
                + box('inner', 18, 84, 258, 506, at(8, 52, img('probe_big.png', 'width:240px'))
                      + box('abs', 26, 368, 206, 1, '', 'background:#4a4d52')
                      + at(0, 400, stat, 'width:258px;text-align:center;font-size:18px;font-weight:700') + at(0, 430, batt, 'width:258px')))
    return screen(top('JOG', 'Handwheel' if not paired else '', 3), left, right, msgbar(''),
                  side_any(SIDE_SYS, 2, red=6), bottom_any(BOT_MON, active=3))


@reg('sys_probe', 'p047_x338.png')
def sys_probe():
    return probe_page(False)


@reg('sys_probe_ok', 'p047_x339.png')
def sys_probe_ok():
    return probe_page(True)


def scope_plot(w=1132, h=448, x0=34, xs=(320, 540), view=False):
    """sine trace with grid, axis labels and A/B cursor"""
    import math as _m
    gx = lambda v: x0 + (v - 314) / (536 - 314) * (w - x0 - 8)
    gy = lambda v: 210 - v * 80
    el = [f'<rect width="{w}" height="{h}" fill="#000"/>']
    for v in range(xs[0], xs[1] + 1, 20):
        el.append(f'<line x1="{gx(v):.1f}" y1="20" x2="{gx(v):.1f}" y2="{h - 34}" stroke="#2a2a2a" stroke-dasharray="2 4"/>')
        el.append(f'<text x="{gx(v):.1f}" y="{h - 12}" fill="#cfcfcf" font-size="15" text-anchor="middle" font-family="Inter" font-weight="600">{v}</text>')
    for v in (-2, -1, 0, 1, 2):
        el.append(f'<line x1="{x0}" y1="{gy(v)}" x2="{w}" y2="{gy(v)}" stroke="#2a2a2a" stroke-dasharray="2 4"/>')
        el.append(f'<text x="{x0 - 8}" y="{gy(v) + 5}" fill="#cfcfcf" font-size="15" text-anchor="end" font-family="Inter" font-weight="600">{v}</text>')
    el.append(f'<line x1="{x0}" y1="10" x2="{x0}" y2="{h - 34}" stroke="#e8a317" stroke-width="1.5"/>')
    pts = []
    t = 314.0
    while t <= 538:
        pts.append(f'{gx(t):.1f},{gy(_m.sin((t - 314) / 7.85 * 2 * _m.pi) * 0.97):.1f}')
        t += 0.5
    el.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="#f4a71a" stroke-width="2.2"/>')
    cx = gx(369)
    el.append(f'<line x1="{cx:.1f}" y1="18" x2="{cx:.1f}" y2="{h - 34}" stroke="#f2e600" stroke-width="2"/>')
    el.append(f'<text x="{cx:.1f}" y="14" fill="#f2e600" font-size="14" text-anchor="middle" font-family="Inter" font-weight="700">A/B</text>')
    return f'<svg width="{w}" height="{h}" style="position:absolute;left:0;top:0">{"".join(el)}</svg>'


def scope_table(y=512):
    cols = ['Signal', 'Unit', 'A', 'B', 'ΔT', 'Max', 'Min', 'Mean', 'Std. Dev.']
    cw = [155, 122, 122, 122, 122, 122, 122, 122, 122]
    rows = [('Time', '#e0e0e0', ['ms', '369', '369', '0', '--', '--', '--', '--']),
            ('Filtered Mach. Coord. X', '#62b330', ['', '-131', '-131', '0', '-131', '-131', '-131', '0']),
            ('Filtered Mach. Coord. Y', '#f4a71a', ['', '-0.876084', '-0.876084', '0', '-0.876084', '-0.876084', '-0.876084', '0']),
            ('Filtered Mach. Coord. Z', '#3b82f6', ['', '0.812543', '0.812543', '0', '0.812543', '0.812543', '0.812543', '0']),
            ('Filtered Mach. Coord. A', '#e040c0', ['', '-1', '-1', '0', '-1', '-1', '-1', '0'])]
    h = []
    x = 0
    for c, w in zip(cols, cw):
        h.append(box('abs', x, 0, w - 1, 24, c, 'background:#5a5a5a;color:#eee;font-size:13.5px;font-weight:700;display:flex;align-items:center;justify-content:center'))
        x += w
    for r, (name, col, vals) in enumerate(rows):
        x = 0
        for k, w in enumerate(cw):
            t = name if k == 0 else vals[k - 1]
            c = col if k == 0 else '#fff'
            fs = 11.5 if k == 0 and r else 15
            h.append(box('abs', x, 25 + r * 26, w - 1, 25, t, f'background:#666;color:{c};font-size:{fs}px;font-weight:700;display:flex;align-items:center;justify-content:center;white-space:nowrap;overflow:hidden'))
            x += w
    return box('abs', 6, y, 1132, 160, ''.join(h))


@reg('sys_scope', 'p048_x345.png')
def sys_scope():
    bot = [('samp_set', 'Sampling Setup'), ('mon_start', 'Start Monitoring'), ('ptr_a', 'Pointer A'), ('ptr_left', 'Pointer Left'),
           ('ptr_right', 'Pointer Right'), ('view3d', 'View'), None, ('exit', 'Exit')]
    return screen(top('JOG', 'Handwheel', 3), box('abs', 6, 64, 1132, 448, scope_plot()), scope_table(),
                  msgbar(''), side_any(SIDE_SYS, 2, red=6), bottom_any(bot, red=7))


@reg('sys_scope_view', 'p049_x349.png')
def sys_scope_view():
    bot = [('x_axis', 'X Axis'), ('ax_zin', 'Axis Zoom In'), ('ax_zout', 'Axis Zoom Out'), ('ax_left', 'Axis Left'),
           ('ax_right', 'Axis Right'), ('autofit', 'Auto Fit'), ('samp_pts', 'Sample Points'), ('back', 'Back')]
    return screen(top('JOG', 'Handwheel', 3), box('abs', 6, 64, 1132, 448, scope_plot()), scope_table(),
                  msgbar(''), side_any(SIDE_SYS, 2, red=6), bottom_any(bot))


@reg('frag_sampling', 'p048_x346.png')
def frag_sampling():
    ax = ['X', 'Y', 'Z', 'A', 'C', 'U', 'V']
    chk = lambda on: (f'<span style="display:inline-flex;width:18px;height:18px;background:#111;border-radius:3px;align-items:center;justify-content:center;'
                      f'color:#9ad04a;font-size:17px;font-weight:900">{"✓" if on else ""}</span>')
    h = [box('abs', 6, 6, 690, 30, at(14, 4, '◌', 'color:#888;font-size:16px') + at(36, 4, 'Sampling Setup', 'font-size:16px;color:#e6e6e6;font-weight:700'), 'background:#4a4a4a'),
         at(6, 46, 'Signal Selection (up to 4 signals)', 'font-size:14.5px;color:#bdbdbd;font-weight:600'),
         box('abs', 6, 72, 690, 466 - 72 - 10, '', 'background:#5d5d5d;border:1px solid #777')]
    for k, a in enumerate(ax):
        x = 96 + k * 86
        h.append(box('abs', x, 74, 84, 18, a, 'background:#6a6a6a;color:#fff;font-size:13px;font-weight:700;display:flex;align-items:center;justify-content:center'))
        h.append(at(x + 33, 140, chk(k < 4)))
    h.append(at(8, 134, 'Filtered Mach.<br>Coord.', 'font-size:12.5px;color:#fff;font-weight:700;width:86px;line-height:1.2'))
    h.append(box('abs', 6, 175, 690, 1, '', 'background:#777'))
    h.append(at(6, 200, 'Sampling Period', 'font-size:14.5px;color:#bdbdbd'))
    h.append(box('fin', 132, 192, 220, 32, '1<span class="chv"></span>', 'position:absolute;height:32px;font-size:15px'))
    h.append(at(362, 199, 'ms', 'font-size:15px;color:#cfcfcf'))
    return screen(*h, w=702, h=238, bg='#3a3a3a')


@reg('frag_wifi', 'p051_x360.png')
def frag_wifi():
    wifi = '<svg width="18" height="14" viewBox="0 0 18 14"><path d="M1,5 a11,11 0 0 1 16,0 M4,8 a7,7 0 0 1 10,0 M7,11 a3,3 0 0 1 4,0" fill="none" stroke="#ddd" stroke-width="2"/></svg>'
    lock = '<svg width="12" height="14" viewBox="0 0 12 14"><rect x="1" y="6" width="10" height="8" rx="1" fill="#ddd"/><path d="M3,6 v-2 a3,3 0 0 1 6,0 v2" fill="none" stroke="#ddd" stroke-width="1.8"/></svg>'
    h = [at(14, 6, 'Select Network <span style="color:#8cc63f">◌</span>', 'font-size:12.5px;color:#cfcfcf'),
         at(404, 6, 'Signal', 'font-size:12.5px;color:#cfcfcf'), at(450, 6, 'Status', 'font-size:12.5px;color:#cfcfcf'),
         box('abs', 4, 24, 538, 26, at(12, 4, 'HUAWEI_B316_4900', 'font-size:14px;color:#8cc63f') + at(392, 5, lock) + at(418, 5, wifi)
             + at(448, 5, 'Connected', 'font-size:12.5px;color:#8cc63f') + at(520, 2, '✓', 'font-size:16px;color:#8cc63f'), 'background:#2a2d31'),
         box('abs', 4, 52, 538, 24, at(12, 4, 'OnePlus 10 Pro', 'font-size:14px;color:#cfcfcf') + at(392, 5, lock) + at(418, 5, wifi)
             + at(448, 5, 'Not connected', 'font-size:12px;color:#cfcfcf'), 'background:#232528')]
    return screen(*h, w=556, h=76, bg='#1e2023')


@reg('probe_pair', 'p052_x374.png')
def probe_pair():
    G = '#7ec242'
    num = lambda n: f'<span style="display:inline-flex;width:24px;height:24px;border-radius:50%;background:{G};color:#fff;align-items:center;justify-content:center;font-size:16px;font-weight:800;margin-right:10px;flex:none">{n}</span>'
    tag = lambda t: f'<span style="border:2px solid {G};border-radius:14px;padding:1px 12px;color:{G};font-size:16px;font-weight:700;background:#1e2a16">{t}</span>'
    dots = lambda cs, bar=None, note='': (''.join(f'<span style="display:inline-block;width:18px;height:18px;border-radius:50%;background:{c};margin-right:5px"></span>' for c in cs)
                                         + (f'<span style="display:inline-block;width:40px;height:16px;background:{bar};border:1px solid #fff;margin-right:8px;vertical-align:1px"></span>' if bar else '')
                                         + f'<span style="color:#e0e0e0;font-size:16px;font-weight:700;vertical-align:3px">{note}</span>')
    p1 = box('abs', 24, 22, 392, 492,
             at(30, 24, num(1) + '<span>Remove the probe battery, wait 5 s and reinsert it to put the probe in battery mode</span>',
                'display:flex;align-items:flex-start;font-size:16px;color:#e8e8e8;font-weight:700;line-height:1.35;width:360px')
             + at(100, 82, img('pair_1.png', 'width:280px'))
             + at(240, 325, '<span style="color:#7ec242;font-size:14px;font-weight:700;line-height:1.25">Remove battery,<br>reinsert after 5 s</span>')
             + at(0, 404, tag('Battery Mode'), 'width:392px;text-align:center')
             + at(0, 448, dots(['#3fbf3f'] * 3, note='(for 5 s)'), 'width:392px;text-align:center'), 'background:#2c3036;border:1px solid #444')
    p2 = box('abs', 430, 22, 660, 492,
             at(30, 34, num(2) + '<span>In battery mode, press and quickly release the stylus to enter pairing mode</span>',
                'display:flex;align-items:center;font-size:16px;color:#e8e8e8;font-weight:700;width:620px')
             + at(60, 82, img('pair_2.png', 'width:220px')) + at(390, 82, img('pair_3.png', 'width:220px'))
             + box('abs', 329, 76, 1, 360, '', 'background:#3e434a')
             + at(0, 404, tag('Pairing Mode'), 'width:340px;text-align:center')
             + at(330, 404, tag('Paired'), 'width:330px;text-align:center')
             + at(0, 448, dots(['#3b82f6'] * 2, '#d0201b', '(for 8 s)'), 'width:340px;text-align:center')
             + at(330, 448, dots(['#3b82f6'] * 2, '#3fbf3f'), 'width:330px;text-align:center'), 'background:#2c3036;border:1px solid #444')
    legend = at(0, 20, 'Legend: <span style="display:inline-block;width:16px;height:16px;border-radius:50%;background:#3fbf3f;margin:0 4px 0 10px;vertical-align:-2px"></span>Short flash'
                       '<span style="display:inline-block;width:30px;height:14px;background:#3fbf3f;margin:0 4px 0 14px;vertical-align:-1px"></span>Long flash',
                'width:1110px;text-align:right;font-size:16px;color:#e0e0e0;font-weight:700')
    body = box('panel', 3, 64, 1135, 604, at(20, 18, 'Probe Pairing', 'font-size:16px;color:#9a9a9a') + legend
               + box('abs', 12, 56, 1110, 536, p1 + p2, 'background:#20242a;border:1px solid #333'))
    sd = [('mach_config', 'Machine Config'), ('hmi_set', 'HMI Settings'), ('axis_calib', 'Axis Calib.'), ('probe_pair', 'Probe Pairing'), None, None, None]
    msg = ('<div class="msgbar" style="color:#ff9b21"><span style="display:inline-flex;width:20px;height:20px;border-radius:50%;background:#ff9b21;color:#252627;'
           'align-items:center;justify-content:center;font-size:15px;font-weight:900">!</span><span>Press “Pair” to start pairing a new probe</span></div>'
           + box('mbox', 953, 675, 88, 38, '') + box('mbox on', 1045, 675, 93, 38, 'Single Block'))
    return screen(top('JOG', 'Handwheel', 3), body, msg, side_any(sd, 3), bottom_any([('pair', 'Pair')]))


@reg('frag_sbar', 'p108_x499.png')
def frag_sbar():
    return screen(box('tfs-l', 0, 0, 60, 63, '<b>S</b><small>Spindle<br>Speed</small>'),
                  at(60, 13, '<span class="mono g" style="font-size:30px">0</span>', 'width:150px;text-align:center'),
                  at(222, 20, '<span class="mono" style="font-size:16px;color:#6f6f6f">rpm</span>'),
                  box('abs', 302, 6, 1, 50, '', 'background:#43464b'),
                  at(320, 6, '<span class="mono" style="font-size:16px;color:#cfcfcf">80%</span>', 'width:190px;text-align:right'),
                  f'<div class="bar" style="left:322px;top:34px;width:190px"><i style="width:68%"></i></div>',
                  w=520, h=63, bg='#24272b')


@reg('alarm_area', 'p112_x508.png')
def alarm_area():
    err = ('<span style="display:inline-flex;align-items:center;gap:6px;border:1.5px solid #e0302a;border-radius:3px;padding:1px 6px;color:#ff3b30">'
           '<span class="dot red" style="width:13px;height:13px"></span>Error</span>'
           '<span style="color:#ff3b30;margin-left:10px;font-weight:700;font-size:16px">SW00001: Press Reset to clear the error state</span>')
    c = [('X', '-32.245', '0.000'), ('Y', '-18.254', '0.000'), ('Z', '100.000', '0.000'), ('A', '0.000', '0.000'), ('C', '0.000', '0.000')]
    code = [(1, '%'), (2, ' (Program name= CAVITY_MILL_4'), (3, ' (Tool name= D4)'), (4, 'N1 G40 G17 G94 G90 G80 G49'),
            (5, 'N2 G21'), (6, 'N3 G91 G28 Z0.0')]
    prog = program('Local NC Files &gt; 1-T1-D4.NC', '1/3596', code, 5, w=568)
    prog = prog.replace('width:1076px', 'width:510px').replace('left:1078px', 'left:512px').replace('left:1081px', 'left:515px') \
               .replace('width:1100px;height:230px', 'width:534px;height:230px')
    timep = box('panel', 575, 380, 563, 290, '<div class="ph">Machining Time</div>' + box('inner', 16, 44, 530, 230,
                at(18, 30, '<span style="color:#8cc63f;font-size:20px">▶</span>')
                + at(56, 26, '<span class="mono" style="font-size:22px;color:#a8d26d">[1/6693]</span>')
                + at(56, 58, '<span class="mono" style="font-size:29px;color:#d0d0d0">1-T1-D4(1).NC</span>')
                + at(0, 42, '<span class="mono g" style="font-size:34px">0%</span>', 'width:500px;text-align:right')
                + at(0, 110, '', 'width:100%;height:1px;background:#3a3b40')
                + at(18, 122, ico('clock', 22, 22, '#cfcfcf') + '<span class="mono" style="font-size:21px;color:#cfcfcf;margin-left:14px">00:00:08</span>', 'display:flex;align-items:center')
                + at(330, 122, ico('clock', 22, 22, '#cfcfcf') + '<span class="mono" style="font-size:21px;color:#cfcfcf;margin-left:14px">00:00:00</span>', 'display:flex;align-items:center')
                + box('abs', 14, 166, 500, 52, '', 'background:#2c2e33')))
    bot = [('time', 'Time'), ('progctl', 'Program Control'), ('auxaxis', 'Aux Axis'), None, None, None, None, ('back', 'Previous Page')]
    frames = (box('abs', 212, 4, 581, 54, '', 'border:3px solid #e0201b')
              + box('abs', 3, 671, 950, 44, '', 'border:3px solid #e0201b'))
    return screen(top('AUTO', 'Auto', 0, dot='red', msg=err), coords(c, 'Work Coord.', 'G54'),
                  tfs(T='#1', D='4', H='-50.000', F='0', S='0', spct=74, tool='End Mill'), prog, timep,
                  msgbar('When an error alarm occurs, reset before switching to MDI mode'),
                  side(SIDE_AUTO, 0), bottom_any(bot, active=0), frames)
