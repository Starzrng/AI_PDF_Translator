# -*- coding: utf-8 -*-
"""Layout-preserving EN->RU translation of Creality Sermoon P1 scanner manual.

Run from anywhere: .venv/bin/python jobs/sermoon-p1/build.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))

import pymupdf  # noqa: E402
from pdft.overlay import Overlay, hex2rgb, hexcol, load_blocks, parse_key  # noqa: E402
from translations import TR, OPS  # noqa: E402

OUT = HERE / "out" / "sermoon_p1_scanner_RU.pdf"

ov = Overlay(HERE / "source.pdf", sample_step=1, bg_pad=0.8)
doc = ov.doc
blocks = load_blocks(HERE / "blocks.json")
fill_rect = ov.fill_rect


def put_html(pno, rect, inner, size, color="#231f20", align="left", lh=1.25):
    ov.put_html(pno, rect, inner, size, color, align, lh)


def put_line(pno, rect, text, size, color="#231f20", align="center"):
    """Single-line autofit for cramped diagram callouts."""
    fs = ov.fit_size(text, rect.width - 1, size, mins=2.4, step=0.15)
    y0 = rect.y0 + (rect.height - fs) / 2 - fs * 0.10
    r = pymupdf.Rect(rect.x0, max(rect.y0 - 1, y0), rect.x1, rect.y1 + 4)
    ov.put_textbox(pno, r, text, fs, (0, 0, 0) if color == "#231f20" else hex2rgb(color), align)


# ---- generic blocks (resolve rect from blocks.json) ----
for key, e in TR.items():
    pg, bi = parse_key(key)
    o = blocks[(pg, bi)]
    base = pymupdf.Rect(o["bbox"])
    r = pymupdf.Rect(base)
    r.x0 += e.get("dx0", 0); r.y0 += e.get("dy0", 0); r.x1 += e.get("dx1", 0); r.y1 += e.get("dy1", 0)
    if "x0" in e: r.x0 = e["x0"]
    if "x1" in e: r.x1 = e["x1"]
    if "y0" in e: r.y0 = e["y0"]
    if "y1" in e: r.y1 = e["y1"]
    if "fr" in e:                       # explicit fill rect (table cells: keep off gridlines)
        fill_rect(pg-1, pymupdf.Rect(e["fr"]))
    else:
        pad = e.get("bgpad", 0.8)
        fill_rect(pg-1, base + (-pad, -pad, pad, pad))
    size = e.get("size", o["sz"])
    color = e.get("color", hexcol(o["col"]))
    put_html(pg-1, r, e["html"], size, color, e.get("align", "left"), e.get("lh", 1.25))

# ---- explicit ops (splits, spec cells, callouts, footer) ----
# two-pass: fill all first (so overlapping callout boxes don't erase neighbours' text)
for op in OPS:
    if op.get("fill", True):
        r0 = pymupdf.Rect(op["rect"])
        # table cells -> inset so the fill never paints over the gridlines; others -> small expand
        delta = (1.4, 1.2, -1.4, -1.2) if op.get("inset") else (-0.6, -0.6, 0.6, 0.6)
        fill_rect(op["pg"]-1, r0 + delta, op.get("fillcolor"))
for op in OPS:
    pg = op["pg"]; r = pymupdf.Rect(op["rect"])
    if op.get("autofit"):
        put_line(pg-1, r, op["html"], op.get("size", 4.0), op.get("color", "#231f20"), op.get("align", "center"))
    else:
        put_html(pg-1, r, op["html"], op.get("size", 6.0), op.get("color", "#231f20"),
                 op.get("align", "left"), op.get("lh", 1.2))

# ---- unify font: re-render any text NOT already replaced (kept numbers) in Arial ----
# build coverage map of regions we already redacted/rewrote
covered = {}
for key in TR:
    pg, bi = parse_key(key)
    covered.setdefault(pg, []).append(pymupdf.Rect(blocks[(pg, bi)]["bbox"]))
for op in OPS:
    covered.setdefault(op["pg"], []).append(pymupdf.Rect(op["rect"]))

def _is_covered(pg, bbox):
    cx, cy = (bbox[0]+bbox[2])/2, (bbox[1]+bbox[3])/2
    for r in covered.get(pg, []):
        if r.x0-0.5 <= cx <= r.x1+0.5 and r.y0-0.5 <= cy <= r.y1+0.5:
            return True
    return False

leftover = []  # (pno, span bbox, text, size, color)
# only the spec tables (pages 18,19) — elsewhere any leftover is intentional
# (e.g. page-3 circled numbers ①..⑨, which Arial cannot render)
for pno in (17, 18):
    for b in doc[pno].get_text("dict")["blocks"]:
        if b["type"] != 0:
            continue
        for l in b["lines"]:
            for s in l["spans"]:
                if not s["text"].strip():
                    continue
                if _is_covered(pno+1, s["bbox"]):
                    continue
                leftover.append((pno, s["bbox"], s["text"], round(s["size"], 1), s["color"]))

print("re-rendering %d kept spans in Arial:" % len(leftover))
for pno in {l[0] for l in leftover}:
    doc[pno].insert_font(fontname="ar", fontfile=ov.font_file)
# two-pass: fill all, then text all
for pno, bb, txt, sz, col in leftover:
    fill_rect(pno, pymupdf.Rect(bb) + (-0.6, -0.4, 0.6, 0.4))
for pno, bb, txt, sz, col in leftover:
    r = pymupdf.Rect(bb[0]-8, bb[1]-0.6, bb[2]+8, bb[3]+3)
    doc[pno].insert_textbox(r, txt, fontname="ar", fontsize=sz,
                            color=hex2rgb(hexcol(col)), align=1)

ov.save(OUT)
