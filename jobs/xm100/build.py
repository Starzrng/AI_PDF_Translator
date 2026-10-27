"""Build the Russian XM-100 manual.

content/*.html (sorted)  ->  build/index.html  ->  Chromium PDF  ->  stamped final PDF

Content conventions:
  <h1 class="ch">   chapter (outline level 1, page break before)
  <h2>/<h3>/<h4>    outline levels 2..4 (ids + TOC entries generated here)
  <h5>              bold sub-item heading, not in TOC
  <!--TOC-->        where the generated table of contents goes
Images are referenced relative to xm100/ (e.g. assets/scr/classic.png).
"""
import fitz, html, os, re, sys
from playwright.sync_api import sync_playwright

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hmi'))
from screens import SCREENS  # noqa: E402
from kit import hbtn  # noqa: E402

ROOT = os.path.dirname(os.path.abspath(__file__))
B = os.path.join(ROOT, 'build')
OUT = os.path.join(ROOT, 'XM-100_manual_RU.pdf')
SRC = os.path.join(ROOT, 'source.pdf')
HEAD_RE = re.compile(r'<h([1-4])([^>]*)>(.*?)</h\1>', re.S)


def load_content(only=None):
    files = sorted(f for f in os.listdir(os.path.join(ROOT, 'content')) if f.endswith('.html'))
    if only:
        files = [f for f in files if any(f.startswith(o) for o in only)]
    return '\n'.join(open(os.path.join(ROOT, 'content', f)).read() for f in files)


def number_headings(body):
    """Give every h1-h4 an id; return (body, entries[(level, id, text)])."""
    entries = []

    def sub(m):
        lvl, attrs, inner = int(m.group(1)), m.group(2), m.group(3)
        hid = f'h{len(entries) + 1}'
        attrs = re.sub(r'\sid="[^"]*"', '', attrs)
        text = re.sub(r'<[^>]+>', '', inner).strip()
        if 'notoc' not in attrs:
            entries.append((lvl, hid, text))
        else:
            hid = f'n{len(entries)}_{abs(hash(text)) % 99999}'
        return f'<h{lvl} id="{hid}"{attrs}>{inner}</h{lvl}>'
    return HEAD_RE.sub(sub, body), entries


XHMI = re.compile(r'<x-hmi\s+n="([^"]+)"(?:\s+w="([\d.]+)")?\s*/>')
XFIG = re.compile(r'<x-fig\s+n="([^"]+)"(?:\s+w="([\d.]+)")?\s*/>')
XBTN = re.compile(r'<x-btn\s+i="([^"]+)"\s+l="([^"]+)"(\s+on)?\s*/>')


def expand_widgets(body):
    """<x-hmi n=".." w="pt"/> -> vector HMI screen; <x-btn i=".." l=".."/> -> button with reflection."""
    def scr(m):
        h = SCREENS[m.group(1)]()
        w_px, h_px = (int(v) for v in re.search(r'width:(\d+)px;height:(\d+)px', h).groups())
        w_pt = float(m.group(2) or 425)
        z = w_pt * 96 / 72 / w_px
        return (f'<div class="hmi-fig" style="width:{w_pt}pt;height:{w_pt * h_px / w_px:.2f}pt">'
                f'<div style="zoom:{z:.5f}">{h}</div></div>')
    body = XHMI.sub(scr, body)
    body = XBTN.sub(lambda m: hbtn(m.group(1), m.group(2), bool(m.group(3))), body)

    def fig(m):
        svg = open(os.path.join(ROOT, 'figs', m.group(1) + '.svg')).read()
        pre = re.sub(r'\W', '', m.group(1)) + '-'
        svg = re.sub(r'id="([^"]+)"', lambda k: f'id="{pre}{k.group(1)}"', svg)
        svg = re.sub(r'url\(#([^)]+)\)', lambda k: f'url(#{pre}{k.group(1)})', svg)
        vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', svg).group(1).split()]
        w = float(m.group(2) or vb[2])
        return svg.replace('<svg ', f'<svg width="{w}pt" height="{w * vb[3] / vb[2]:.2f}pt" style="display:block;margin:0 auto" ', 1)
    body = XFIG.sub(fig, body)
    return XALM.sub(lambda m: alarm_table(m.group(1)), body)


XALM = re.compile(r'<x-alarms\s+d="([^"]+)"\s*/>')


LABEL = {'原因': 'Причина', '解决': 'Решение', '原因/解决': 'Причина / решение'}


def alarm_table(sec):
    """Chapter-5 table for section '5.N' from extract/alarms.json + data/alarms_tr.py."""
    import json
    sys.path.insert(0, os.path.join(ROOT, 'data'))
    import alarms_tr
    secs = json.load(open(os.path.join(ROOT, 'extract', 'alarms.json')))
    msgs = json.load(open(os.path.join(ROOT, 'extract', 'alarm_msgs.json')))
    extra = json.load(open(os.path.join(ROOT, 'extract', 'alarm_extra.json')))
    mi = {m: k for k, m in enumerate(msgs)}
    xi = {m: k for k, m in enumerate(extra)}
    s = next(x for x in secs if x['title'].split()[0] == sec)
    out = ['<table class="tb alarm"><colgroup><col style="width:66pt"><col></colgroup>'
           '<thead><tr><th>Код</th><th>Сообщение на экране (EN) / перевод</th></tr></thead>']
    for e in s['entries']:
        en, ru = alarms_tr.MSG[mi[e['msg']]]
        out.append(f'<tbody class="alarm"><tr class="acode"><td>{e["code"]}</td><td><span class="en">{en}</span>'
                   f'<span class="ru">{ru}</span></td></tr>')
        for lab, txt in e['extra']:
            ru_x = alarms_tr.EXTRA[xi[txt]] if txt in xi else txt
            out.append(f'<tr><td>{LABEL.get(lab, lab)}</td><td>{ru_x or "—"}</td></tr>')
        out.append('</tbody>')
    out.append('</table>')
    return ''.join(out)


def toc_html(entries, pages=None):
    rows = []
    for lvl, hid, text in entries:
        pg = pages.get(hid, '') if pages else '000'
        rows.append(f'<div class="e l{lvl}"><a href="#{hid}"><span class="tx">{text}</span>'
                    f'<span class="dots"></span><span class="pg">{pg}</span></a></div>')
    return '<section class="toc"><h1 class="notoc">Содержание</h1>\n' + '\n'.join(rows) + '\n</section>'


def render(body, entries, pages, pdf_path):
    doc = ('<!doctype html><html lang="ru"><head><meta charset="utf-8">'
           '<link rel="stylesheet" href="../style.css"><link rel="stylesheet" href="../hmi/kit.css"></head><body>\n'
           + body.replace('<!--TOC-->', toc_html(entries, pages)) + '\n</body></html>')
    hp = os.path.join(B, 'index.html')
    open(hp, 'w').write(doc)
    with sync_playwright() as p:
        br = p.chromium.launch()
        pg = br.new_page()
        pg.goto('file://' + hp)
        pg.wait_for_load_state('networkidle')
        pg.pdf(path=pdf_path, prefer_css_page_size=True, print_background=True)
        br.close()


def link_targets(pdf_path, entries):
    """Map heading id -> (body page index, y from top) via the named destinations Chromium writes."""
    d = fitz.open(pdf_path)
    names = d.resolve_names()
    out = {}
    for _, hid, _ in entries:
        if hid in names:
            n = names[hid]
            out[hid] = (n['page'], d[n['page']].rect.height - n['to'][1])
    return out


def named_to_goto(doc, targets):
    """Replace Chromium's named-destination links with explicit GoTo links (survive insert_pdf)."""
    for page in doc:
        for ln in page.get_links():
            if ln.get('kind') == fitz.LINK_NAMED and ln.get('nameddest') in targets:
                pno, y = targets[ln['nameddest']]
                page.delete_link(ln)
                page.insert_link({'kind': fitz.LINK_GOTO, 'from': ln['from'], 'page': pno,
                                  'to': fitz.Point(0, max(y - 12, 0)), 'zoom': 0})


def chrome_template():
    """Original page 3 with all body text removed -> watermark + header logos + rule + company line."""
    src = fitz.open(SRC)
    t = fitz.open()
    t.insert_pdf(src, from_page=2, to_page=2)
    pg = t[0]
    pg.add_redact_annot(fitz.Rect(0, 70, 595, 842))
    pg.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE,
                        graphics=fitz.PDF_REDACT_LINE_ART_REMOVE_IF_TOUCHED)
    return t


def assemble(body_pdf, entries, targets, cover=None, back=None):
    body = fitz.open(body_pdf)
    tpl = chrome_template()
    arial = '/System/Library/Fonts/Supplemental/Arial.ttf'
    font = fitz.Font(fontfile=arial)
    named_to_goto(body, targets)
    for i, page in enumerate(body):
        page.show_pdf_page(page.rect, tpl, 0, overlay=False)
        num = str(i + 1)
        w = font.text_length(num, 9)
        page.insert_text((page.rect.width / 2 - w / 2, 786), num, fontsize=9, fontname='arial', fontfile=arial)
    out = fitz.open()
    if cover:
        out.insert_pdf(fitz.open(cover))
    off = len(out)
    out.insert_pdf(body)
    if back:
        out.insert_pdf(fitz.open(back))
    toc = []
    for lvl, hid, text in entries:
        if hid in targets:
            pno, y = targets[hid]
            toc.append([lvl, html.unescape(text), pno + 1 + off, {'kind': fitz.LINK_GOTO, 'page': pno + off,
                                                                   'to': fitz.Point(0, max(y - 12, 0))}])
    # PyMuPDF wants levels without jumps
    fixed, prev = [], 0
    for e in toc:
        e[0] = min(e[0], prev + 1)
        prev = e[0]
        fixed.append(e)
    out.set_toc(fixed)
    out.subset_fonts()
    out.save(OUT, garbage=4, deflate=True, clean=True)
    print('saved', OUT, len(out), 'pages')


def main():
    only = sys.argv[1:] or None
    os.makedirs(B, exist_ok=True)
    body, entries = number_headings(expand_widgets(load_content(only)))
    p1 = os.path.join(B, 'pass1.pdf')
    render(body, entries, None, p1)
    targets = link_targets(p1, entries)
    pages = {hid: str(pno + 1) for hid, (pno, _) in targets.items()}
    p2 = os.path.join(B, 'body.pdf')
    render(body, entries, pages, p2)
    targets2 = link_targets(p2, entries)
    if {h: v[0] for h, v in targets2.items()} != {h: v[0] for h, v in targets.items()}:
        print('WARNING: pagination changed between passes')
    cover = os.path.join(ROOT, 'assets', 'cover.pdf')
    back = os.path.join(ROOT, 'assets', 'back.pdf')
    assemble(p2, entries, targets2,
             cover if os.path.exists(cover) else None,
             back if os.path.exists(back) else None)


if __name__ == '__main__':
    main()
