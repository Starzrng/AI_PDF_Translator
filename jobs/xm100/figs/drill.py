"""Canned-cycle diagrams (G81/G82 simple, G83/G84 peck) for G98 and G99, Russian labels.
Source figure p088 had G98/G99 swapped; here G98 = return to initial plane, G99 = return to R plane."""
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEF = ('<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto">'
       '<path d="M0,1 L10,5 L0,9z" fill="#000"/></marker></defs>')
FONT = 'font-family="PT Sans, Arial"'


def arrow(x1, y1, x2, y2, dash=False, w=1):
    d = ' stroke-dasharray="3 2.5"' if dash else ''
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#000" stroke-width="{w}"{d} marker-end="url(#a)"/>'


def dot(x, y, r=3.4):
    return f'<circle cx="{x}" cy="{y}" r="{r}"/>'


def txt(x, y, s, size=10, anchor='start'):
    return f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}">{s}</text>'


def simple_panel(ox, g98):
    e = [f'<rect x="{ox + 14}" y="10" width="28" height="170" fill="#d9d9d9"/>']
    zx, rx, ax, sx = ox + 28, ox + 72, ox + 120, ox + 172
    y = 58
    e += [txt(zx, 44, 'Z', 11, 'middle'), txt(rx, 44, 'R', 11, 'middle'), txt(ax, 44, 'A', 11, 'middle')]
    e += [arrow(sx - 4, y + 15, ax + 4, y + 1, True), arrow(ax - 4, y, rx + 4, y, True), arrow(rx - 4, y, zx + 4, y, False, 1.2)]
    e += [dot(zx, y), dot(rx, y), dot(ax, y), dot(sx, y + 16), txt(sx + 6, y + 20, 'Начальная', 9.5), txt(sx + 6, y + 31, 'точка', 9.5)]
    y2 = 132
    end = sx if g98 else rx
    e += [dot(zx, y2), arrow(zx + 4, y2, end - 4, y2, True), dot(end, y2)]
    e += [txt(end, y2 + 18, 'Исходная плоскость' if g98 else 'Плоскость R', 10, 'middle' if not g98 else 'end')]
    e += [txt(ox + 220, 170, 'G98' if g98 else 'G99', 17, 'end')]
    return ''.join(e)


def peck_panel(ox, g98):
    e = [f'<rect x="{ox + 10}" y="10" width="78" height="186" fill="#d9d9d9"/>']
    rx, ax, sx = ox + 104, ox + 136, ox + 178
    ds = [ox + 80, ox + 54, ox + 28]          # depth 1..3 (towards the left = deeper)
    y0 = 56
    e += [txt(ds[0], 40, 'Z', 11, 'middle'), txt(rx, 40, 'R', 11, 'middle'), txt(ax, 40, 'A', 11, 'middle')]
    e += [arrow(sx - 4, y0 + 15, ax + 4, y0 + 1, True), dot(sx, y0 + 16), txt(sx + 2, y0 + 30, 'Начальная', 9), txt(sx + 2, y0 + 40, 'точка', 9),
          arrow(ax - 4, y0, rx + 4, y0, True), dot(ax, y0), dot(rx, y0)]
    for x in ds + [rx]:
        e.append(f'<line x1="{x}" y1="{y0 - 4}" x2="{x}" y2="176" stroke="#000" stroke-width="1" stroke-dasharray="1.5 2"/>')
    ys = [y0, y0 + 36, y0 + 74]
    for i, (x, y) in enumerate(zip(ds, ys)):
        if i:
            e.append(arrow(rx, y, x + 4, y, False, 1))
        else:
            e.append(arrow(rx - 4, y, x + 4, y, False, 1.1))
        e.append(dot(x, y))
        e.append(f'<circle cx="{x - 13}" cy="{y + 9}" r="7" fill="none" stroke="#000" stroke-width="0.8"/>' + txt(x - 13, y + 12.5, str(i + 1), 9.5, 'middle'))
        if i < 2:
            e.append(arrow(x, y + 12, rx - 1, y + 12, True, 0.8))
    yr = ys[2] + 16
    end = sx if g98 else rx
    e.append(arrow(ds[2], yr, end - 4, yr, True, 0.9))
    e.append(dot(end, yr))
    for x1, x2 in [(ds[2], ds[1]), (ds[1], ds[0]), (ds[0], rx)]:
        e.append(f'<line x1="{x1 + 1}" y1="186" x2="{x2 - 1}" y2="186" stroke="#000" stroke-width="0.6"/>'
                 + txt((x1 + x2) / 2, 197, 'q', 10, 'middle'))
    e.append(txt(end + (0 if g98 else 4), yr + 18, 'Исходная плоскость' if g98 else 'Плоскость R', 10, 'end' if g98 else 'start'))
    e.append(txt(ox + 236, 196, 'G98' if g98 else 'G99', 17, 'end'))
    return ''.join(e)


def frame(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" {FONT}>{DEF}'
            f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" fill="#fff" stroke="#000" stroke-width="1.5"/>'
            f'<line x1="{w / 2}" y1="1" x2="{w / 2}" y2="{h - 1}" stroke="#000" stroke-width="1.5"/>{body}</svg>')


if __name__ == '__main__':
    (HERE / 'drill_simple.svg').write_text(frame(500, 190, simple_panel(10, True) + simple_panel(260, False)))
    (HERE / 'drill_peck.svg').write_text(frame(500, 210, peck_panel(8, True) + peck_panel(258, False)))
    print('drill ok')
