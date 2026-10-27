"""Compact per-page text for translation: merges wrapped lines into paragraphs."""
import json, sys
pg = json.load(open('extract/pages.json'))
a, b = int(sys.argv[1]), int(sys.argv[2])
for p in pg:
    if not a <= p['page'] <= b:
        continue
    print(f'=== P{p["page"]}')
    tb = p['tables']
    def in_table(l):
        x0, y0, x1, y1 = l['bbox']
        return any(t['bbox'][0] - 2 <= x0 and y1 <= t['bbox'][3] + 2 and y0 >= t['bbox'][1] - 2 for t in tb)
    items = [(l['bbox'][1], 'L', l) for l in p['lines'] if not in_table(l) and 'Shenzhen Xhorse' not in l['text']
             and not (l['bbox'][1] > 770)]
    items += [(t['bbox'][1], 'T', t) for t in tb]
    items += [(i['rect'][1], 'I', i) for i in p['images'] if not i['smask']]
    items.sort(key=lambda x: x[0])
    buf, prev = '', None
    for y, k, it in items:
        if k == 'L':
            t = it['text'].strip()
            if not t:
                continue
            new = (prev is None or it['bold'] != prev['bold'] or it['bbox'][0] > 70 and abs(it['bbox'][0] - prev['bbox'][0]) > 12
                   or t[0] in '●•' or y - prev['bbox'][1] > 34 or prev['text'].strip()[-1:] in '：:；;。')
            if new:
                if buf: print(buf)
                buf = ('**' if it['bold'] else '') + f'[{it["bbox"][0]:.0f}] ' + t
            else:
                buf += t
            prev = it
        else:
            if buf: print(buf); buf = ''
            if k == 'T':
                for row in it['rows']:
                    cells = [(c or '').replace('\n', ' ') for c in row if c]
                    print('  | ' + ' | '.join(cells))
            else:
                print(f'  [IMG {it["file"]}]')
            prev = None
    if buf: print(buf)
