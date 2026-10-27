"""Dump source PDF structure: text lines with style, tables, images per page.

Outputs:
  pages.json  — machine-readable inventory
  pages.txt   — human-readable dump used while authoring content/*.html
  img/        — every content image (alpha kept) named p{page}_x{xref}.png
"""
import fitz, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', 'source.pdf')
CHROME_XREFS = {38871, 610, 611}          # watermark + 2 header logos
CJK = re.compile(r'[一-鿿]')


def color_hex(c):
    return '#%06x' % c


def main():
    doc = fitz.open(SRC)
    os.makedirs(os.path.join(HERE, 'img'), exist_ok=True)
    out, txt = [], []
    saved = set()
    for pno, page in enumerate(doc, 1):
        pg = {'page': pno, 'lines': [], 'tables': [], 'images': []}
        d = page.get_text('dict')
        for b in d['blocks']:
            if b['type'] != 0:
                continue
            for l in b['lines']:
                spans = [s for s in l['spans'] if s['text'].strip()]
                if not spans:
                    continue
                text = ''.join(s['text'] for s in l['spans']).strip()
                s0 = max(spans, key=lambda s: len(s['text']))
                pg['lines'].append({
                    'bbox': [round(v, 1) for v in l['bbox']],
                    'size': round(s0['size'], 1),
                    'bold': 'Bold' in s0['font'] or bool(s0['flags'] & 16),
                    'color': color_hex(s0['color']),
                    'font': s0['font'],
                    'text': text,
                })
        for t in page.find_tables().tables:
            pg['tables'].append({'bbox': [round(v, 1) for v in t.bbox],
                                 'rows': t.extract()})
        for im in page.get_images(full=True):
            x = im[0]
            if x in CHROME_XREFS:
                continue
            rects = page.get_image_rects(x)
            fn = f'p{pno:03d}_x{x}.png'
            if x not in saved:
                pix = fitz.Pixmap(doc, x)
                if im[1]:                       # soft mask -> keep alpha
                    pix = fitz.Pixmap(pix, fitz.Pixmap(doc, im[1]))
                if pix.colorspace and pix.colorspace.n > 3:
                    pix = fitz.Pixmap(fitz.csRGB, pix)
                pix.save(os.path.join(HERE, 'img', fn))
                saved.add(x)
            for r in rects:
                pg['images'].append({'xref': x, 'smask': im[1], 'w': im[2], 'h': im[3],
                                     'rect': [round(v, 1) for v in r], 'file': fn})
        out.append(pg)

        txt.append(f'\n===== PAGE {pno} =====')
        items = [(l['bbox'][1], l['bbox'][0], 'L', l) for l in pg['lines']]
        items += [(i['rect'][1], i['rect'][0], 'I', i) for i in pg['images']]
        items += [(t['bbox'][1] - 0.5, t['bbox'][0], 'T', t) for t in pg['tables']]
        for y, x, k, it in sorted(items, key=lambda a: (round(a[0]), a[1])):
            if k == 'L':
                fl = ('B' if it['bold'] else ' ') + f"{it['size']:4.1f}"
                col = '' if it['color'] == '#000000' else ' ' + it['color']
                txt.append(f"  y{y:5.0f} x{x:4.0f} {fl}{col}| {it['text']}")
            elif k == 'I':
                r = it['rect']
                txt.append(f"  y{y:5.0f} x{x:4.0f} [IMG {it['file']} {r[2]-r[0]:.0f}x{r[3]-r[1]:.0f}pt"
                           f"{' smask' if it['smask'] else ''}]")
            else:
                txt.append(f"  y{y:5.0f} x{x:4.0f} [TABLE {len(it['rows'])}r]")
                for row in it['rows']:
                    txt.append('      | ' + ' | '.join((c or '').replace('\n', '⏎') for c in row))
    json.dump(out, open(os.path.join(HERE, 'pages.json'), 'w'), ensure_ascii=False, indent=0)
    open(os.path.join(HERE, 'pages.txt'), 'w').write('\n'.join(txt))
    print('pages', len(out), 'images saved', len(saved))


if __name__ == '__main__':
    main()
