"""Building blocks for the redrawn XMachine HMI (1280×800 canvas, English UI)."""
from pathlib import Path
import base64, math

ROOT = Path(__file__).resolve().parent.parent
ICONS = ROOT / 'assets' / 'icons'
HIMG = ROOT / 'assets' / 'hmi_img'


def uri(p):
    return Path(p).as_uri()


_DATA = {}


def data_uri(p):
    """CSS masks need same-origin images; file:// is opaque, so inline icons as data URIs."""
    p = Path(p)
    if p not in _DATA:
        _DATA[p] = 'data:image/png;base64,' + base64.b64encode(p.read_bytes()).decode()
    return _DATA[p]


def ico(name, w=None, h=None, color=None, extra=''):
    st = f'--i:url({data_uri(ICONS / (name + ".png"))});'
    if w: st += f'width:{w}px;'
    if h: st += f'height:{h}px;'
    if color: st += f'color:{color};'
    return f'<span class="ico" style="{st}{extra}"></span>'


def img(name, style=''):
    return f'<img src="{uri(HIMG / name)}" style="{style}">'


def box(cls, x, y, w, h, inner='', style=''):
    return f'<div class="{cls}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;{style}">{inner}</div>'


def at(x, y, inner, style='', cls='abs'):
    return f'<div class="{cls}" style="left:{x}px;top:{y}px;{style}">{inner}</div>'


def screen(*parts, w=1280, h=800, bg=None):
    st = f'width:{w}px;height:{h}px;' + (f'background:{bg};' if bg else '')
    return f'<div class="hmi" style="{st}">' + ''.join(parts) + '</div>'


# ---------------------------------------------------------------- chrome
TABS = [('tab_machining', 'Machining'), ('tab_tools', 'Tools'), ('tab_program', 'Program'), ('tab_system', 'System')]
MODE_DOT = {'AUTO': 'green', 'JOG': 'orange', 'MDI': 'orange'}


def top(mode='AUTO', sub='Auto', tab=0, dot=None, msg=''):
    dot = dot or MODE_DOT.get(mode, 'green')
    h = ['<div class="top">',
         f'<div class="mode"><span class="dot {dot}"></span><span class="m {mode.lower()}">{mode}</span>'
         f'<span class="chev">›</span><span class="sub" style="{"font-size:15px" if len(sub) > 10 else ""}">{sub}</span><span class="dd"></span></div>',
         f'<div class="msgf">{msg}</div>']
    for i, (ic, t) in enumerate(TABS):
        x = 1143 if i == 3 else 795 + i * 116
        cls = 'tab' + (' on' if i == tab else '') + (' sys' if i == 3 else '')
        h.append(f'<div class="{cls}" style="left:{x}px">{ico(ic)}<span>{t}</span></div>')
    h.append('</div>')
    return ''.join(h)


SB_Y = [63, 156, 249, 342, 435, 528, 621]


def _label(t):
    if '|' in t:
        a, b = t.split('|')
        return f'<span class="lbl2">{a}<br>{b}</span>'
    return f'<span>{t}</span>'


def side(items, active=None, help=True):
    """items: up to 7 of (icon, label) | None."""
    h = []
    for i, y in enumerate(SB_Y):
        it = items[i] if i < len(items) else None
        if it is None:
            h.append(f'<div class="sbtn empty" style="top:{y}px"></div>')
        else:
            on = ' on' if active == i else ''
            h.append(f'<div class="sbtn{on}" style="top:{y}px">{ico(it[0])}{_label(it[1])}</div>')
    if help:
        h.append(f'<div class="sbtn" style="top:717px;height:81px">{ico("help")}<span>Help</span></div>')
    return ''.join(h)


def bottom(items, active=None):
    h = []
    for i in range(8):
        x = 3 + i * 143
        it = items[i] if i < len(items) else None
        if it is None:
            h.append(f'<div class="bbtn empty" style="left:{x}px"></div>')
        else:
            on = ' on' if active == i else ''
            h.append(f'<div class="bbtn{on}" style="left:{x}px">{ico(it[0])}{_label(it[1])}</div>')
    return ''.join(h)


def msgbar(text='', err=False, right=None, right2=None):
    cls = 'msgbar err' if err else 'msgbar'
    t = f'<span style="font-size:15px">●</span><span>{text}</span>' if text else ''
    h = f'<div class="{cls}">{t}</div>'
    h += box('mbox' + (' on' if right2 and right2[1] else ''), 953, 675, 88, 38, right2[0] if right2 else '')
    h += box('mbox' + (' on' if right else ''), 1045, 675, 93, 38, right or '')
    return h


def panel(x, y, w, h, title='', inner='', head_extra=''):
    t = f'<div class="ph">{title}</div>' if title else ''
    return box('panel', x, y, w, h, t + head_extra + inner)


# ---------------------------------------------------------------- standard blocks
SIDE_AUTO = [('classic', 'Classic View'), ('graphic', 'Graphic View'), ('guide', 'Guide View'),
             ('edit', 'Edit Program'), None, None, ('control', 'Control Panel')]
SIDE_JOG = [('classic', 'Classic View'), ('graphic', 'Graphic View'), ('guide', 'Guide View'),
            ('tsm', 'TSM'), ('workpos', 'Workpiece|Positioning'), ('toolmeasure', 'Tool Measure'),
            ('control', 'Control Panel')]
SIDE_MDI = [('classic', 'Classic View'), ('graphic', 'Graphic View'), ('guide', 'Guide View'),
            ('clear', 'Clear'), None, None, ('control', 'Control Panel')]
BOT_AUTO = [('allg', 'All G Codes'), ('g', 'G Codes'), ('m', 'M Codes'), ('aux', 'Auxiliary'),
            ('switch', 'Switch Coord.'), ('relative', 'Relative Coord.'), ('fs', 'FS Override'), ('next', 'Next Page')]
BOT_JOG = [('seltool', 'Select Tool'), ('seloffset', 'Select Offset'), ('g', 'G Codes'), ('m', 'M Codes'),
           ('switch', 'Switch Coord.'), ('relative', 'Relative Coord.')]

COORDS_DEMO = [('X', '-42.020', '0.001'), ('Y', '-106.020', '-25.960'), ('Z', '-97.980', '-0.000'),
               ('A', '0.000', '-0.000'), ('C', '0.000', '0.000')]
COORDS_JOG = [('X', '-86.392', '0.000'), ('Y', '-117.782', '0.000'), ('Z', '-99.940', '0.000'),
              ('A', '0.000', '0.000'), ('C', '0.000', '0.000')]


def coords(rows=COORDS_DEMO, kind='Machine Coord.', g='G53', x=3, y=64, w=568, h=312):
    head = (f'<div class="ph">{kind}<span class="badge">{g}</span></div>'
            + at(0, 12, 'Position', 'width:282px;text-align:right;font-size:17.5px;color:#c9c9c9;font-weight:700')
            + at(0, 12, 'Distance to Go', 'width:478px;text-align:right;font-size:17.5px;color:#c9c9c9;font-weight:700')
            + at(492, 12, 'Unit', 'font-size:17.5px;color:#c9c9c9;font-weight:700'))
    rr = []
    for i, (ax, pos, rem) in enumerate(rows):
        unit = 'deg' if ax in 'ABC' else 'mm'
        rr.append(f'<div class="crow" style="top:{i * 50}px"><span class="ax">{ax}</span>'
                  f'<span class="cv mono g" style="left:0;width:262px">{pos}</span>'
                  f'<span class="cv mono" style="left:0;width:452px;color:#e2e2e2">{rem}</span>'
                  f'<span class="cu">{unit}</span></div>')
    inner = box('inner', 20, 44, 528, 254, ''.join(rr))
    return box('panel', x, y, w, h, head + inner)


def tfs(T='#2', D='0', H='-70.000', RS='0.000', F='999', S='10000', fpct=100, spct=100, tool='Neck End Mill',
        x=575, y=64, w=563, h=312, pic='endmill.png'):
    lbl = 'font-size:14.5px;color:#b9b9b9;font-weight:700'
    unit = 'font-family:IBM Plex Mono;font-size:11px;color:#6a6a6a;font-weight:500;margin-left:6px'
    trow = (box('tfs-l', 0, 0, 56, 126, '<b>T</b><small>Tool<br>Info</small>')
            + at(84, 34, f'<span class="mono g" style="font-size:21px">{T}</span>'
                         f'<span style="color:#666;margin:0 8px;font-size:20px;font-weight:400">|</span>'
                         f'<span class="mono" style="font-size:21px;color:#ddd">{D}</span><span style="{unit}">mm</span>')
            + at(66, 66, f'<div class="toolpic">{img(pic, "position:absolute;left:30px;top:0;height:22px;width:128px;object-fit:cover;object-position:left")}'
                         f'<span class="tl">{tool}</span></div>')
            + box('abs', 236, 28, 1, 76, '', 'background:#4a4a4a')
            + box('abs', 382, 28, 1, 76, '', 'background:#4a4a4a')
            + at(246, 34, f'<span style="{lbl}">Tool Length H</span><span style="{unit}">mm</span>')
            + at(246, 62, f'<span class="mono g" style="font-size:25px">{H}</span>')
            + at(392, 34, f'<span style="{lbl}">Rad. Comp. RS</span><span style="{unit}">mm</span>')
            + at(392, 62, f'<span class="mono g" style="font-size:25px">{RS}</span>')
            + box('abs', 56, 126, 474, 1, '', 'background:#43464b'))

    def row(top, letter, small, val, u, pct):
        return (box('tfs-l', 0, top, 56, 62, f'<b>{letter}</b><small>{small}</small>')
                + at(56, top + 14, f'<span class="mono g" style="font-size:30px">{val}</span>',
                     'width:150px;text-align:center')
                + at(222, top + 22, f'<span class="mono" style="font-size:15px;color:#6f6f6f">{u}</span>')
                + box('abs', 300, top + 6, 1, 50, '', 'background:#43464b')
                + at(320, top + 8, f'<span class="mono" style="font-size:16px;color:#cfcfcf">{pct}%</span>',
                     'width:185px;text-align:right')
                + f'<div class="bar" style="left:322px;top:{top + 36}px;width:185px"><i style="width:{min(pct, 100) * 0.85}%"></i></div>')
    inner = box('inner', 16, 44, 530, 254, trow + row(127, 'F', 'Feed<br>Rate', F, 'mmpm', fpct)
                + box('abs', 56, 189, 474, 1, '', 'background:#43464b')
                + row(190, 'S', 'Spindle<br>Speed', S, 'rpm', spct), 'overflow:hidden')
    return box('panel', x, y, w, h, '<div class="ph">Status</div>' + inner)


def program(path='Local NC Files &gt; xiao &gt; 1-(2)-D3.175.NC', counter='33/14246', lines=None, sel=None,
            x=3, y=380, w=1135, h=290):
    """lines: (number, code) rows of the program window"""
    lines = lines or []
    head = (f'<div class="ph" style="color:#8a8a8a;font-weight:600">{ico("prog_g", 22, 20, "#3d7df2")}{path}</div>'
            + at(0, 12, counter, f'width:{w - 32}px;text-align:right;font-size:17.5px;color:#8a8a8a'))
    rows = []
    for i, (n, c) in enumerate(lines):
        cls = 'code sel' if sel == i else 'code'
        rows.append(f'<div class="{cls}" style="top:{i * 38}px;width:1076px"><span class="n mono">{n}</span>'
                    f'<span class="c mono">{c}</span></div>')
    scroll = (box('abs', 1078, 0, 20, 228, '', 'background:#2b2c30;border-left:1px solid #3a3a3a')
              + box('abs', 1081, 4, 14, 42, '', 'background:#4a4b50;border-radius:2px'))
    return box('panel', x, y, w, h, head + box('inner', 18, 46, 1100, 230, ''.join(rows) + scroll, 'overflow:hidden'))


def lower(title, inner_html, icon=None, x=3, y=380, w=1135, h=290, inner_style=''):
    t = (ico(icon[0], 22, 22, icon[1]) if icon else '') + title
    return box('panel', x, y, w, h, f'<div class="ph">{t}</div>' + box('inner', 18, 44, 1100, 232, inner_html, inner_style))


def field(y, label, value='', w=None, dropdown=False, sm=False, x=14, lw=160):
    cls = 'fin sm' if sm else 'fin'
    st = f'width:{w}px' if w else ''
    dd = '<span class="chv"></span>' if dropdown else ''
    return (f'<div class="frow" style="top:{y}px;left:{x}px"><span class="fl" style="width:{lw}px">{label}</span>'
            f'<div class="{cls}" style="{st}">{value}{dd}</div></div>')


def gauge(cx, cy, pct, lo, hi, color, label, r=96):
    """Speedometer-style override gauge drawn in SVG."""
    a0, a1 = 225, -45                      # degrees, CCW from +x
    frac = (pct - lo) / (hi - lo)

    def pt(a, rr):
        return cx + rr * math.cos(math.radians(a)), cy - rr * math.sin(math.radians(a))

    def arc(rr, f0, f1):
        s, e = a0 - (a0 - a1) * f0, a0 - (a0 - a1) * f1
        (x0, y0), (x1, y1) = pt(s, rr), pt(e, rr)
        large = 1 if (s - e) > 180 else 0
        return f'M{x0:.1f},{y0:.1f} A{rr},{rr} 0 {large} 1 {x1:.1f},{y1:.1f}'
    ticks = []
    for k in range(41):
        a = a0 - (a0 - a1) * k / 40
        (x0, y0), (x1, y1) = pt(a, r + 12), pt(a, r + 22 if k % 5 == 0 else r + 18)
        ticks.append(f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="#bdbdbd" stroke-width="1.6"/>')
    (lx, ly), (hx, hy) = pt(a0 - 6, r - 6), pt(a1 + 6, r - 6)
    svg = (f'<svg width="300" height="300" viewBox="0 0 300 300" style="position:absolute;left:0;top:0">'
           f'<path d="{arc(r - 14, 0, 1)}" stroke="#1d1d1d" stroke-width="26" fill="none" stroke-linecap="round"/>'
           f'<path d="{arc(r - 14, 0, frac)}" stroke="{color}" stroke-width="22" fill="none" stroke-linecap="round"/>'
           + ''.join(ticks)
           + f'<text x="{cx}" y="{cy + 13}" text-anchor="middle" font-family="Inter" font-weight="600" font-size="38" fill="#c8c8c8">{pct}%</text>'
           f'<text x="{lx:.0f}" y="{ly + 20:.0f}" text-anchor="middle" font-family="IBM Plex Mono" font-size="15" fill="#cfcfcf" transform="rotate(45 {lx:.0f} {ly + 20:.0f})">{lo}</text>'
           f'<text x="{hx:.0f}" y="{hy + 20:.0f}" text-anchor="middle" font-family="IBM Plex Mono" font-size="15" fill="#cfcfcf" transform="rotate(-45 {hx:.0f} {hy + 20:.0f})">{hi}</text>'
           f'</svg>')
    return svg + at(0, cy + 108, label, 'width:300px;text-align:center;font-size:17px;color:#cfcfcf')


# ---------------------------------------------------------------- doc buttons
def hbtn(icon, label, on=False):
    b = (f'<div class="hbtn{" on" if on else ""}">'
         f'<span class="ico" style="--i:url({data_uri(ICONS / (icon + ".png"))})"></span>{_label(label)}</div>')
    return f'<div class="hbtn-wrap">{b}<div class="refl">{b}</div></div>'


# ---------------------------------------------------------------- annotated screens (ch.1)
ANN = {'green': '#7cc142', 'orange': '#f5a020', 'blue': '#3b82f6', 'dgreen': '#1f9d3a', 'purple': '#9b4dca'}


def annotate(scr, frames, badges, pad=(120, 70), bg='#2b2b2b'):
    """Put a 1280×800 screen on a dark canvas and draw coloured frames + numbered badges.
    frames: (x, y, w, h, colour) in screen coords; badges: (n, bx, by, colour, (lx, ly) | None) —
    badge centre in screen coords (may lie outside), optional leader-line end point."""
    px, py = pad
    W, H = 1280 + 2 * px, 800 + 2 * py
    svg = [f'<svg width="{W}" height="{H}" style="position:absolute;left:0;top:0">']
    for x, y, w, h, c in frames:
        svg.append(f'<rect x="{x + px}" y="{y + py}" width="{w}" height="{h}" fill="none" stroke="{ANN[c]}" stroke-width="5"/>')
    for n, bx, by, c, lead in badges:
        if lead:
            svg.append(f'<line x1="{bx + px}" y1="{by + py}" x2="{lead[0] + px}" y2="{lead[1] + py}" stroke="{ANN[c]}" stroke-width="4"/>')
    for n, bx, by, c, lead in badges:
        svg.append(f'<circle cx="{bx + px}" cy="{by + py}" r="22" fill="{ANN[c]}"/>'
                   f'<text x="{bx + px}" y="{by + py + 10}" text-anchor="middle" font-family="Inter" font-weight="700" font-size="28" fill="#fff">{n}</text>')
    svg.append('</svg>')
    inner = scr.replace('class="hmi" style="', 'class="hmi" style="position:absolute;left:%dpx;top:%dpx;' % (px, py), 1)
    return f'<div class="hmi" style="width:{W}px;height:{H}px;background:{bg}">{inner}{"".join(svg)}</div>'


# ---------------------------------------------------------------- tables / files
def folder_svg(w=30):
    return (f'<svg width="{w}" height="{w * 0.8:.0f}" viewBox="0 0 30 24"><path d="M1,4 a2,2 0 0 1 2,-2 h8 l3,3 h13 a2,2 0 0 1 2,2 v14 a2,2 0 0 1 -2,2 h-24 a2,2 0 0 1 -2,-2z" fill="#f0a020"/>'
            f'<rect x="1" y="8" width="28" height="15" rx="2" fill="#ffb62e"/></svg>')


FILE_COL = {'NC': '#2f6bff', 'TAP': '#22a03a', 'NGC': '#e0952a', 'MPF': '#d0342c', 'TXT': '#7a7a7a'}


def file_svg(kind='NC', w=26):
    c = FILE_COL.get(kind, '#2f6bff')
    return (f'<svg width="{w}" height="{w * 1.15:.0f}" viewBox="0 0 26 30"><path d="M3,1 h14 l7,7 v20 a1,1 0 0 1 -1,1 h-19 a1,1 0 0 1 -1,-1 v-26 a1,1 0 0 1 1,-1z" fill="#f2f4f8"/>'
            f'<path d="M17,1 v7 h7z" fill="#c9d3e6"/><text x="4" y="27" font-family="Inter" font-weight="800" font-size="8" fill="{c}">{kind}</text></svg>')


def tri(up=True):
    b = 'border-bottom:18px solid #e6e6e6' if up else 'border-top:18px solid #e6e6e6'
    return f'<span style="width:0;height:0;border-left:13px solid transparent;border-right:13px solid transparent;{b}"></span>'


def bottom_any(items, active=None, red=None):
    """bottom bar where an item may be ('^'|'v') arrow, (icon,label), None."""
    h = []
    for i in range(8):
        x = 3 + i * 143
        it = items[i] if i < len(items) else None
        st = 'background:linear-gradient(#d84a43,#c23b35);border-color:#e0605a;' if red == i else ''
        if it is None:
            h.append(f'<div class="bbtn empty" style="left:{x}px"></div>')
        elif it in ('^', 'v'):
            h.append(f'<div class="bbtn" style="left:{x}px">{tri(it == "^")}</div>')
        else:
            on = ' on' if active == i else ''
            h.append(f'<div class="bbtn{on}" style="left:{x}px;{st}">{ico(it[0])}{_label(it[1])}</div>')
    return ''.join(h)


def side_any(items, active=None, red=None, help=True):
    h = []
    for i, y in enumerate(SB_Y):
        it = items[i] if i < len(items) else None
        st = 'background:linear-gradient(#d84a43,#c23b35);border-color:#e0605a;' if red == i else ''
        if it is None:
            h.append(f'<div class="sbtn empty" style="top:{y}px"></div>')
        else:
            on = ' on' if active == i else ''
            h.append(f'<div class="sbtn{on}" style="top:{y}px;{st}">{ico(it[0])}{_label(it[1])}</div>')
    if help:
        h.append(f'<div class="sbtn" style="top:717px;height:81px">{ico("help")}<span>Help</span></div>')
    return ''.join(h)
