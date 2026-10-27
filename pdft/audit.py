"""Audit any translated PDF against its source — no job data needed.

    python -m pdft.audit source.pdf translated.pdf [--pages 2-5]

Works for our old jobs, harness jobs and other tools' output alike, so
approaches can be compared on the same numbers:

  ru_pages      pages with Cyrillic text
  en_layer      source-language spans still in the text layer unchanged
                (copy/search returns them even when painted over)
  small         translated spans below 5 pt
  shrunk        translated spans < 85 % of the nearest source span's size
  over_art      translated spans lying on artwork (lines, icons, photos)
  art_changed   pt² of non-text area that differs from the source
                (cover-up boxes over lines, lost graphics)
  overlaps      translated spans of different lines that intersect
"""
import argparse
import re
from pathlib import Path

import pymupdf
from PIL import Image, ImageChops, ImageDraw

from .qa import MIN_PX, ZOOM, _artwork, _differ, _mode, _spans
from .render import parse_pages

CYR = re.compile(r"[А-Яа-яЁё]")
LAT = re.compile(r"[A-Za-z]{2,}")


def _img(page, zoom):
    pix = page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom), alpha=False)
    return Image.frombytes("RGB", (pix.width, pix.height), pix.samples)


def audit(src_path, out_path, pages=None):
    src, out = pymupdf.open(src_path), pymupdf.open(out_path)
    pages = pages or range(1, min(src.page_count, out.page_count) + 1)
    m = dict(pages=0, ru_pages=0, en_layer=0, ru_spans=0, small=0, shrunk=0, over_art=0, art_changed=0.0, overlaps=0)
    worst = {}
    for pg in pages:
        sp, op = src[pg - 1], out[pg - 1]
        s_spans, o_spans = list(_spans(sp)), list(_spans(op))
        ru = [s for s in o_spans if CYR.search(s["text"])]
        m["pages"] += 1
        m["ru_pages"] += bool(ru)
        m["ru_spans"] += len(ru)
        sig = {(round(s["bbox"][0]), round(s["bbox"][1]), s["text"]) for s in s_spans}
        m["en_layer"] += sum(1 for s in o_spans if LAT.search(s["text"]) and not CYR.search(s["text"])
                             and (round(s["bbox"][0]), round(s["bbox"][1]), s["text"]) in sig
                             and len(LAT.findall(s["text"])) >= 2)
        art = _artwork(src_path, pg - 1)
        page_issues = 0
        for s in ru:
            r = pymupdf.Rect(s["bbox"])
            c = r.tl + (r.br - r.tl) * 0.5
            near = min(s_spans, key=lambda t: abs(pymupdf.Rect(t["bbox"]).tl.y - r.tl.y) + 0.3 * abs(pymupdf.Rect(t["bbox"]).tl.x - r.tl.x), default=None)
            if s["size"] < 5:
                m["small"] += 1
            if near and s["size"] < 0.85 * near["size"]:
                m["shrunk"] += 1
                page_issues += 1
            inner = r + (0.5, 0.5, -0.5, -0.5)
            if _differ(art, inner, _mode(art, inner)) > MIN_PX:
                m["over_art"] += 1
                page_issues += 1
        lines = {}
        for s in ru:
            lines.setdefault(round(s["bbox"][1], 1), []).append(pymupdf.Rect(s["bbox"]))
        keys = sorted(lines)
        for i, a in enumerate(keys):
            for b in keys[i + 1:]:
                if any((ra & rb).get_area() > 2 for ra in lines[a] for rb in lines[b] if ra.intersects(rb)):
                    m["overlaps"] += 1
                    page_issues += 1
        # non-text pixels that changed: cover-up boxes, damaged lines
        z = 2.0
        diff = ImageChops.difference(_img(sp, z), _img(op, z)).convert("L").point(lambda v: 255 if v > 40 else 0)
        mask = Image.new("L", diff.size, 255)
        d = ImageDraw.Draw(mask)
        for s in s_spans + o_spans:
            x0, y0, x1, y1 = s["bbox"]
            d.rectangle([(x0 - 1) * z, (y0 - 1) * z, (x1 + 1) * z, (y1 + 1) * z], fill=0)
        changed = ImageChops.multiply(diff, mask).histogram()[255] / (z * z)
        m["art_changed"] += changed
        if page_issues or changed > 20:
            worst[pg] = (page_issues, round(changed))
    m["art_changed"] = round(m["art_changed"])
    m["size_mb"] = round(Path(out_path).stat().st_size / 1e6, 1)
    return m, worst


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source", type=Path)
    ap.add_argument("translated", type=Path)
    ap.add_argument("--pages")
    a = ap.parse_args()
    pages = parse_pages(a.pages, 10_000) if a.pages else None
    m, worst = audit(a.source, a.translated, pages)
    print(" ".join(f"{k}={v}" for k, v in m.items()))
    if worst:
        print("pages with issues (layout issues, changed artwork pt²):",
              ", ".join(f"p{p}: {i}/{c}" for p, (i, c) in sorted(worst.items())))


if __name__ == "__main__":
    main()
