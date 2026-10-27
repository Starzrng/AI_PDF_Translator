"""Automatic checks on a built overlay job — the agent's feedback signal.

ERROR  todo       segment on a checked page still has html=TODO
ERROR  leftover   source-font text with letters still on the page (not in KEEP)
ERROR  moved      source text that is not where the source has it (redaction damage)
ERROR  lost       source text outside every entry box vanished (redaction too wide)
ERROR  style      translation breaks docs/glossary/style-rules.json
WARN   shrunk     text scaled below 90 % to fit (layout too tight)
WARN   fill-art   a painted box covers original artwork (paint=True entries)
WARN   text-art   new text lands on original artwork (lines, icons, photos)
WARN   overlap    texts of two different entries intersect

Artwork checks compare against the source rendered with all text removed, so
they see exactly the lines, fills and images a translation could collide with.
"""
import json
import re
from collections import Counter
from pathlib import Path

import pymupdf

from .overlay import block_bbox, parse_key
from .segments import has_letters, segment

ROOT = Path(__file__).resolve().parents[1]
ZOOM = 3.0
TOL = 60          # summed RGB distance that counts as "different colour"
MIN_PX = 30       # differing pixels (at ZOOM) before an artwork warning fires


def _pix(page):
    return page.get_pixmap(matrix=pymupdf.Matrix(ZOOM, ZOOM), alpha=False)


def _artwork(src_path, pno):
    """Source page rendered without any text."""
    doc = pymupdf.open(src_path)
    page = doc[pno]
    page.clean_contents(sanitize=True)
    page.add_redact_annot(page.rect, fill=False)
    page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE, graphics=pymupdf.PDF_REDACT_LINE_ART_NONE,
                          text=pymupdf.PDF_REDACT_TEXT_REMOVE)
    return _pix(page)


def _region(pix, rect, step=1):
    s, n, st = pix.samples, pix.n, pix.stride
    for y in range(max(0, int(rect.y0 * ZOOM)), min(pix.height, int(rect.y1 * ZOOM)), step):
        for x in range(max(0, int(rect.x0 * ZOOM)), min(pix.width, int(rect.x1 * ZOOM)), step):
            o = y * st + x * n
            yield s[o], s[o + 1], s[o + 2]


def _differ(pix, rect, ref):
    return sum(1 for p in _region(pix, rect)
               if abs(p[0] - ref[0]) + abs(p[1] - ref[1]) + abs(p[2] - ref[2]) > TOL)


def _mode(pix, rect):
    c = Counter(_region(pix, rect, 2))
    return c.most_common(1)[0][0] if c else (255, 255, 255)


def _spans(page):
    for b in page.get_text("dict")["blocks"]:
        if b["type"] == 0:
            for line in b["lines"]:
                for s in line["spans"]:
                    if s["text"].strip():
                        yield s


def _ours(span):
    return "arial" in span["font"].lower()


def _center(bbox):
    r = pymupdf.Rect(bbox)
    return r.tl + (r.br - r.tl) * 0.5


def _sig(s):
    return round(s["bbox"][0]), round(s["bbox"][1]), s["text"]


def check(job, log, pages=None):
    mod = job.translations()
    keep = set(getattr(mod, "KEEP", ()))
    pages = set(pages or range(1, pymupdf.open(job.source).page_count + 1))
    rules = json.loads((ROOT / "docs/glossary/style-rules.json").read_text(encoding="utf-8"))
    issues = []

    def add(level, kind, pg, key, msg):
        issues.append(dict(level=level, kind=kind, pg=pg, key=key, msg=msg))

    for k, e in mod.TR.items():
        pg = parse_key(k)[0]
        if pg not in pages:
            continue
        if e.get("html") is None:
            if k not in keep:
                add("ERROR", "todo", pg, k, "not translated yet")
            continue
        plain = re.sub(r"<[^>]+>", "", e["html"])
        for rule in rules:
            if re.search(rule["pattern"], plain, re.I):
                add("ERROR", "style", pg, k, f'«{rule["pattern"]}» → {rule["use"]}')

    src, out = pymupdf.open(job.source), pymupdf.open(job.output)
    segs = segment(list(job.blocks.values()))
    for pg in sorted(pages):
        pno = pg - 1
        page_log = [en for en in log if en["pg"] == pg]
        boxes = [pymupdf.Rect(en["fill"]) for en in page_log if en["fill"]]
        keep_rects = [pymupdf.Rect(block_bbox(job.blocks, k)) for k in keep if parse_key(k)[0] == pg]
        src_spans = list(_spans(src[pno]))
        out_spans = list(_spans(out[pno]))
        src_sigs = {_sig(s) for s in src_spans}
        out_sigs = {_sig(s) for s in out_spans if not _ours(s)}

        # text bookkeeping: leftover / moved / lost
        reported = set()
        for s in out_spans:
            if _ours(s):
                continue
            if _sig(s) not in src_sigs:
                add("ERROR", "moved", pg, "?", f'source text displaced to {tuple(round(v) for v in s["bbox"])}: "{s["text"].strip()[:40]}"')
                continue
            c = _center(s["bbox"])
            if not has_letters(s["text"]) or any(c in r for r in keep_rects):
                continue
            seg = next((g for g in segs if g["pg"] == pg and c in pymupdf.Rect(g["bbox"]) + (-1, -1, 1, 1)), None)
            key = seg["key"] if seg else "?"
            if key not in reported:
                reported.add(key)
                add("ERROR", "leftover", pg, key, f'source text left: "{s["text"].strip()[:60]}"')
        for s in src_spans:
            if _sig(s) not in out_sigs and not any(_center(s["bbox"]) in b for b in boxes):
                add("ERROR", "lost", pg, "?", f'source text removed outside any entry box: "{s["text"].strip()[:40]}"')

        # layout
        for en in page_log:
            if en["scale"] < 0.9:
                add("WARN", "shrunk", pg, en["key"], f'text at {en["scale"]:.0%} size' + (f'; {en["note"]}' if en["note"] else "; no free space to grow"))

        # artwork collisions
        art = _artwork(job.source, pno)
        for en in page_log:
            if en["fill"] and en.get("paint"):
                n = _differ(art, pymupdf.Rect(en["fill"]), [round(c * 255) for c in en["fillcolor"]])
                if n > MIN_PX:
                    add("WARN", "fill-art", pg, en["key"], f"painted box hides {n} px of artwork; restrict it with fr=")
        owner = {}
        for s in out_spans:
            if not _ours(s):
                continue
            c = _center(s["bbox"])
            en = next((x for x in page_log if c in pymupdf.Rect(x["rect"]) + (-0.5, -0.5, 0.5, 0.5)), None)
            owner.setdefault(en["key"] if en else "?", []).append(pymupdf.Rect(s["bbox"]))
        for k, rects in owner.items():
            for r in rects:
                inner = r + (0.5, 0.5, -0.5, -0.5)
                n = _differ(art, inner, _mode(art, inner))
                if n > MIN_PX:
                    add("WARN", "text-art", pg, k, f"text over artwork ({n} px) at {tuple(round(v) for v in r)}")
                    break
        keys = list(owner)
        for i, a in enumerate(keys):
            for b in keys[i + 1:]:
                if any((ra & rb).get_area() > 2 for ra in owner[a] for rb in owner[b] if ra.intersects(rb)):
                    add("WARN", "overlap", pg, f"{a} × {b}", "texts intersect")
    return issues


def report(job, issues, pages=None):
    path = job.output.parent / "qa.json"
    path.write_text(json.dumps(issues, ensure_ascii=False, indent=1), encoding="utf-8")
    err = sum(i["level"] == "ERROR" for i in issues)
    print(f"QA {job.id}: {err} errors, {len(issues) - err} warnings → {path.relative_to(ROOT)}")
    for i in sorted(issues, key=lambda i: (i["pg"], i["level"] != "ERROR", i["kind"])):
        print(f'  p{i["pg"]:<3}{i["level"]:<6}{i["kind"]:<9}{i["key"]:<12}{i["msg"]}')
    return err
