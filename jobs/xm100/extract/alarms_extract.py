"""Pull chapter-5 alarm tables into structured JSON: sections -> entries {code, msg, extra:[(label, text)]}."""
import json, re
pg = json.load(open('extract/pages.json'))
CODE = re.compile(r'^(\d{2}|[A-Z]{2}\d{4,6}([-/]\d+)?)$')
sections, cur = [], None
odd = []
for p in pg:
    if not 114 <= p['page'] <= 160:
        continue
    items = [(l['bbox'][1], 'H', l['text'].strip()) for l in p['lines']
             if l['bold'] and re.match(r'5\.\d+', l['text'].strip())]
    for t in p['tables']:
        for k, r in enumerate(t['rows']):
            items.append((t['bbox'][1] + k * 0.01, 'R', [(c or '').replace('\n', '') .strip() for c in r]))
    items.sort(key=lambda x: x[0])
    for y, k, v in items:
        if k == 'H':
            cur = {'title': v, 'page': p['page'], 'entries': []}
            sections.append(cur)
            continue
        cells = [c for c in v if c]
        if not cells or cells[0] in ('报警编号', '标识编号'):
            continue
        if CODE.match(cells[0]):
            e = {'code': cells[0], 'msg': cells[1] if len(cells) > 1 else '', 'note': cells[2] if len(cells) > 2 else '',
                 'extra': [], 'page': p['page']}
            if cur is None:
                cur = {'title': '5.3', 'page': p['page'], 'entries': []}
                sections.append(cur)
            cur['entries'].append(e)
        elif cells[0] in ('原因', '解决', '原因/解决', '解决方法', '处理'):
            cur['entries'][-1]['extra'].append([cells[0], cells[1] if len(cells) > 1 else ''])
        else:
            odd.append((p['page'], cells))
json.dump(sections, open('extract/alarms.json', 'w'), ensure_ascii=False, indent=1)
for s in sections:
    print(s['page'], s['title'], len(s['entries']))
print('odd rows', len(odd))
for o in odd[:30]:
    print(o)
