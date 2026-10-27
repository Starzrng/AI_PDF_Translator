# -*- coding: utf-8 -*-
"""Layout-preserving EN->RU translation of CreatBot D1000 Pro HS manual.

Run from anywhere: .venv/bin/python jobs/d1000-pro-hs/build.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))

import pymupdf  # noqa: E402
from pdft.overlay import Overlay, hexcol, load_blocks, parse_key  # noqa: E402
from translations import TR, SPEC, MACROS, PARTS, TOC, COVER  # noqa: E402

OUT = HERE / "out" / "D1000 pro HS-user manual-RU.pdf"

ov = Overlay(HERE / "source.pdf", sample_step=2, bg_pad=1.0)
doc = ov.doc
blocks = load_blocks(HERE / "blocks.json")
fill_rect = ov.fill_rect


def put_html(pno, rect, inner, size, color="#000000", align="left", lh=1.30):
    ov.put_html(pno, rect, inner, size, color, align, lh)


def put_line(pno, rect, text, size, color=(0, 0, 0), align="left", autofit=True, valign="mid"):
    """Single-line text with optional autofit + vertical centring."""
    fs = ov.fit_size(text, rect.width - 2, size) if autofit else size
    if valign == "mid":
        y0 = rect.y0 + (rect.height - fs) / 2 - fs * 0.12
    else:
        y0 = rect.y0
    ov.put_textbox(pno, pymupdf.Rect(rect.x0, max(rect.y0, y0), rect.x1, rect.y1 + 6), text, fs, color, align)


GRAY = (0.97, 0.98, 0.98)

# ----------------------------------------------------------------------------
# 1) GENERIC BLOCKS
# ----------------------------------------------------------------------------
for key, e in TR.items():
    pg, bi = parse_key(key)
    o = blocks[(pg, bi)]
    r = pymupdf.Rect(o["bbox"])
    r.x0 += e.get("dx0", 0); r.y0 += e.get("dy0", 0)
    r.x1 += e.get("dx1", 0); r.y1 += e.get("dy1", 0)
    # single-line headings/captions: give them the full column width so RU
    # doesn't wrap inside the (often narrow) original English box
    if "<br>" not in e["html"] and "dx1" not in e and "dx0" not in e:
        if e.get("align", "left") == "center":
            r.x0, r.x1 = 90.0, 505.0
        else:
            r.x1 = max(r.x1, 505.0)
    fill_rect(pg-1, pymupdf.Rect(o["bbox"]).round() + (-1, -1, 1, 1))
    size = e.get("size", o["sz"])
    color = e.get("color", hexcol(o["col"]))
    put_html(pg-1, r, e["html"], size, color, e.get("align", "left"), e.get("lh", 1.30))

# ----------------------------------------------------------------------------
# 2) COVER
# ----------------------------------------------------------------------------
fill_rect(0, pymupdf.Rect(108, 594, 488, 690))
put_html(0, pymupdf.Rect(120, 598, 476, 690), COVER, 23, "#000000", "center", 1.22)

# ----------------------------------------------------------------------------
# 3) SPEC TABLE  (page 8 -> index 7)
# ----------------------------------------------------------------------------
PNO = 7
LX0, LDIV, RX1 = 90.0, 241.7, 513.0
for row in SPEC:
    y0, y1, kind = row["y"]
    if kind == "h":  # full-width gray header
        rr = pymupdf.Rect(LX0+0.8, y0+0.8, RX1-0.8, y1-0.8)
        fill_rect(PNO, rr, GRAY)
        put_html(PNO, pymupdf.Rect(LX0, y0, RX1, y1+1), f'<b>{row["l"]}</b>', 11.5, "#1c1f23", "center")
    else:
        lr = pymupdf.Rect(LX0+0.8, y0+0.8, LDIV-0.8, y1-0.8)
        vr = pymupdf.Rect(LDIV+0.8, y0+0.8, RX1-0.8, y1-0.8)
        fill_rect(PNO, lr); fill_rect(PNO, vr)
        # label centred in left col, value centred in right col
        nlines = row.get("ll", 1)
        lsz = row.get("ls", 10.4)
        put_html(PNO, pymupdf.Rect(LX0, y0+ (0 if nlines>1 else 1.2), LDIV, y1+1), row["l"], lsz, "#1c1f23", "center", 1.15)
        if row.get("v"):
            vsz = row.get("vs", 10.4)
            put_html(PNO, pymupdf.Rect(LDIV, y0+ (0 if row.get('vl',1)>1 else 1.2), RX1, y1+1), row["v"], vsz, "#000000", "center", 1.15)

# ----------------------------------------------------------------------------
# 4) MACROS TABLE  (pages 15,16)
# ----------------------------------------------------------------------------
# columns: Name [88-210], Type [210-345], Usage [345-510]
def macro_row(pno, y0, y1, name, typ, use, header=False):
    page = doc[pno]
    fill_rect(pno, pymupdf.Rect(88.6+0.8, y0+0.8, 510.7-0.8, y1-0.8))
    cN = pymupdf.Rect(92, y0, 209, y1)
    cT = pymupdf.Rect(212, y0, 344, y1)
    cU = pymupdf.Rect(348, y0, 509, y1)
    if header:
        for c, t in ((cN, name), (cT, typ), (cU, use)):
            put_html(pno, pymupdf.Rect(c.x0, y0+1, c.x1, y1+1), f'<b>{t}</b>', 10.4, "#000", "center")
    else:
        put_line(pno, cN, name, 9.6, align="left")
        put_line(pno, cT, typ, 9.6, align="left")
        put_line(pno, cU, use, 9.6, align="left")

for m in MACROS:
    macro_row(m["pg"]-1, m["y"][0], m["y"][1], m["n"], m["t"], m["u"], m.get("h", False))

# ----------------------------------------------------------------------------
# 5) PART-NAME TABLES (pages 5,6,7)
# ----------------------------------------------------------------------------
# columns x: 84.6 | 297.6 | 510.7 ; name area starts after number circle
for grp in PARTS:
    pno = grp["pg"] - 1
    for cell in grp["cells"]:
        col, y0, y1, text = cell  # col 0 left, 1 right
        if col == 0:
            nx0, nx1 = 110, 296
        else:
            nx0, nx1 = 322, 509
        rr = pymupdf.Rect(nx0, y0+0.8, nx1, y1-0.8)
        fill_rect(pno, rr)
        put_line(pno, pymupdf.Rect(nx0, y0, nx1, y1), text, 9.0, align="left")

# ----------------------------------------------------------------------------
# 6) TABLE OF CONTENTS (page 4 -> index 3)
# ----------------------------------------------------------------------------
PNO = 3
# clear entire TOC region
fill_rect(PNO, pymupdf.Rect(108, 130, 510, 678))
page = doc[PNO]
page.insert_font(fontname="ar", fontfile=ov.font_file)
ty = 133.0
ROWH = 15.6
RIGHT = 507.0
for title, pageno, lvl in TOC:
    x0 = 111 if lvl == 0 else 132
    fs = ov.fit_size(title, RIGHT - x0 - 28, 9.6, 7.5)
    tl = ov.mfont.text_length(title, fs)
    num = str(pageno)
    numw = ov.mfont.text_length(num, fs)
    dotw = ov.mfont.text_length(".", fs)
    baseline = ty + fs * 0.80
    page.insert_text((x0, baseline), title, fontname="ar", fontsize=fs, color=(0, 0, 0))
    page.insert_text((RIGHT - numw, baseline), num, fontname="ar", fontsize=fs, color=(0, 0, 0))
    dot_start = x0 + tl + 3
    dot_end = RIGHT - numw - 3
    ndots = max(0, int((dot_end - dot_start) / dotw))
    if ndots:
        page.insert_text((dot_start, baseline), "." * ndots, fontname="ar", fontsize=fs, color=(0, 0, 0))
    ty += ROWH

ov.save(OUT)
