"""Data-driven overlay job: job.json + blocks.json + translations.py -> out/*.pdf.

translations.py defines
  TR   {"P{page}b{block}": dict(html=..., merge=[...], size, color, align, lh,
                                dx0/dy0/dx1/dy1, x0/x1/y0/y1, fr, fillcolor, bgpad, grow,
                                bold, paint)}
       html=None (TODO) leaves the segment untranslated.
  OPS  [dict(pg, rect, html, size, color, align, lh, inset, fill, fillcolor)] explicit boxes
  KEEP {"P{page}b{block}", ...} source text that stays as is on purpose.

Build order: remove the source text under each entry's box (redaction keeps
images and vector art, so nothing is painted over the artwork), optionally
paint the box (paint=True: text baked into vector outlines, or a job that
needs the old cover-up), then place the text. With grow (default on) a segment whose translation would
be shrunk first takes clean background below it (or to the right for one-line
labels) instead of shrinking.
"""
import json
from pathlib import Path

import pymupdf

from .overlay import Overlay, block_bbox, hexcol, load_blocks, parse_key
from .tm import load_translations

FIT = 0.995           # insert_htmlbox scale treated as "fits without shrinking"
FOOTER = 22.0         # pt kept free at the page bottom (page numbers)


class Job:
    def __init__(self, job_dir):
        self.dir = Path(job_dir).resolve()
        self.id = self.dir.name
        self.cfg = json.loads((self.dir / "job.json").read_text(encoding="utf-8"))
        self.source = self.dir / self.cfg.get("source", "source.pdf")
        self.output = self.dir / self.cfg["output"]
        self.blocks = load_blocks(self.dir / "blocks.json")

    def translations(self):
        return load_translations(self.dir)


def _source_lh(job, keys, size):
    """Line height the source uses for this segment (pitch / size), if it has 2+ lines."""
    pitches = [job.blocks[parse_key(k)]["lp"] for k in keys if "lp" in job.blocks[parse_key(k)]]
    for a, b in zip(keys, keys[1:]):           # step between merged blocks, per line of the first
        step = (block_bbox(job.blocks, b)[1] - block_bbox(job.blocks, a)[1]) / job.blocks[parse_key(a)].get("nl", 1)
        if step > 0.5 * size:
            pitches.append(step)
    if not pitches:
        return None
    lh = sorted(pitches)[len(pitches) // 2] / size
    return round(lh, 2) if 1.0 <= lh <= 3.0 else None


def _entries(job, mod, pages):
    oc = job.cfg.get("overlay", {})
    out = []
    for k, e in mod.TR.items():
        pg, bi = parse_key(k)
        if e.get("html") is None or (pages and pg not in pages):
            continue
        keys = [k] + list(e.get("merge", []))
        base = pymupdf.Rect(block_bbox(job.blocks, k))
        for m in keys[1:]:
            base |= pymupdf.Rect(block_bbox(job.blocks, m))
        o = job.blocks[(pg, bi)]
        size = e.get("size", o["sz"])
        lh = e.get("lh") or _source_lh(job, keys, size) or oc.get("lh", 1.25)
        r = pymupdf.Rect(base)
        need = size * lh * 1.15 + 0.4           # htmlbox needs ~15 % over the line height
        if r.height < need:                     # one-line box: room for one line at full size
            d = (need - r.height) / 2
            r.y0 -= d; r.y1 += d
        r.x0 += e.get("dx0", 0); r.y0 += e.get("dy0", 0); r.x1 += e.get("dx1", 0); r.y1 += e.get("dy1", 0)
        for side in ("x0", "y0", "x1", "y1"):
            if side in e:
                setattr(r, side, e[side])
        pad = e.get("bgpad", oc.get("bg_pad", 0.8))
        html = e["html"]
        units = [job.blocks[parse_key(x)] for x in keys]
        align = e.get("align")
        if align is None and len(keys) > 1:     # lines centred on each other -> centred text
            bbs = [block_bbox(job.blocks, x) for x in keys]
            if max(b[0] for b in bbs) - min(b[0] for b in bbs) > 2 and \
                    max(b[0] + b[2] for b in bbs) - min(b[0] + b[2] for b in bbs) <= 5:
                align = "center"
        if e.get("bold", all(u["bold"] and "<b>" not in u.get("h", "") for u in units)) and not html.startswith("<b>"):
            html = f"<b>{html}</b>"           # weight follows the source block
        out.append(dict(
            key=k, keys=keys, pno=pg - 1, rect=r,
            fill=pymupdf.Rect(e["fr"]) if "fr" in e else base + (-pad, -pad, pad, pad),
            fillcolor=e.get("fillcolor"), paint=e.get("paint", oc.get("paint", False)), html=html, size=size,
            color=e.get("color", hexcol(o["col"])), align=align,
            lh=lh, grow=e.get("grow", oc.get("grow", True))))
    for i, op in enumerate(getattr(mod, "OPS", [])):
        if pages and op["pg"] not in pages:
            continue
        r = pymupdf.Rect(op["rect"])
        delta = (1.4, 1.2, -1.4, -1.2) if op.get("inset") else (-0.6, -0.6, 0.6, 0.6)
        out.append(dict(
            key=f'OP{i}@P{op["pg"]}', keys=[], pno=op["pg"] - 1, rect=r,
            fill=(r + delta) if op.get("fill", True) else None, fillcolor=op.get("fillcolor"),
            paint=op.get("paint", oc.get("paint", False)),
            html=op["html"], size=op.get("size", 6.0), color=op.get("color", "#231f20"),
            align=op.get("align"), lh=op.get("lh", 1.2), grow=op.get("grow", False)))
    return out


def _grown(r, direction, g):
    r = pymupdf.Rect(r)
    if direction == "right":
        r.x1 += g
    elif direction == "left":
        r.x0 -= g
    elif direction == "sides":
        r.x0 -= g; r.x1 += g
    elif direction == "vsides":
        r.y0 -= g; r.y1 += g
    else:
        r.y1 += g
    return r


def _solve(ov, en, page_h):
    """Choose text box and alignment so the translation fits at full size.

    Alignment (unless set): centred on the page or in its cell/frame -> center;
    a one-line label whose right end touches a leader line -> right; else left. Growth follows
    the anchor: right-aligned labels grow left, centred ones to both sides and
    then up and down (wrapping to two lines), left ones right then down;
    paragraphs grow down, then sideways (centred ones sideways first). Only clean background is
    taken. -> (rect, align, scale, note)
    """
    pno, probe = en["pno"], en["fill"] or en["rect"]
    one_line = en["rect"].height < 2.2 * en["size"]
    free = lambda d, area=probe: ov.free_space(pno, area, d) - 1.0
    align = en["align"]
    if align is None:
        page_cx = ov.doc[pno].rect.width / 2
        fl, fr = (free("left"), free("right")) if one_line else (99, 99)
        if fr < 3 <= fl:
            align = "right"                    # leader line at the label's right end
        elif fl < 3 <= fr:
            align = "left"
        elif one_line and abs((en["rect"].x0 + en["rect"].x1) / 2 - page_cx) < 4:
            align = "center"
        elif one_line and fl + fr < 200 and abs(fl - fr) < max(2.0, 0.08 * (fl + fr)):
            align = "center"                   # centred in a table cell or frame
        else:
            align = "left"
    r = pymupdf.Rect(en["rect"])
    measure = lambda rr: ov.measure(rr, en["html"], en["size"], en["color"], align, en["lh"])[1]
    scale = measure(r)
    if scale >= FIT or not en["grow"]:
        return r, align, scale, None
    if not one_line:                           # paragraphs: down first, then sideways
        order = {"right": ("down", "left"), "center": ("sides", "down")}.get(align, ("down", "right"))
    else:
        order = {"right": ("left",), "center": ("sides", "vsides")}.get(align, ("right", "down"))
    note = None
    for direction in order:
        area = probe | r                       # after one growth, scan beside the grown box
        room = {"sides": lambda: min(free("left", area), free("right", area)),
                "vsides": lambda: min(free("up", area), free("down", area))}.get(direction, lambda: free(direction, area))()
        if direction == "down":
            room = min(room, page_h - FOOTER - r.y1)
        # paragraphs stay inside the text column; one-line labels may use half the margin
        lo_x, hi_x = en["column"]
        if one_line:
            lo_x, hi_x = lo_x / 2, hi_x + (ov.doc[pno].rect.width - hi_x) / 2
        if direction in ("right", "sides"):
            room = min(room, hi_x - r.x1)
        if direction in ("left", "sides"):
            room = min(room, r.x0 - lo_x)
        if room <= 0.5:
            continue
        if measure(_grown(r, direction, room)) < FIT:
            r = _grown(r, direction, room)
            scale = measure(r)
            note = f"grew {direction} {room:.1f}pt (all free space), still shrunk"
            continue
        lo, hi = 0.0, room                     # smallest growth that fits
        for _ in range(12):
            mid = (lo + hi) / 2
            if measure(_grown(r, direction, mid)) >= FIT:
                hi = mid
            else:
                lo = mid
        r = _grown(r, direction, hi)
        scale = measure(r)
        note = f"grew {direction} {hi:.1f}pt"
        break
    return r, align, scale, note


def build(job, pages=None):
    """Build job.output; returns the per-entry layout log used by qa."""
    oc = job.cfg.get("overlay", {})
    ov = Overlay(job.source, sample_step=oc.get("sample_step", 1), bg_pad=oc.get("bg_pad", 0.8))
    entries = _entries(job, job.translations(), pages)
    column = {}                                # text column: page margins mirrored
    for o in job.blocks.values():
        column[o["pg"] - 1] = min(column.get(o["pg"] - 1, 1e9), o["bbox"][0])
    for en in entries:                         # 1. sample on the untouched source
        w = ov.doc[en["pno"]].rect.width
        m = min(column.get(en["pno"], 36), en["rect"].x0)
        en["column"] = (m, w - m)
        if en["fill"] is not None and en["fillcolor"] is None:
            en["fillcolor"] = ov.bg_color(en["pno"], en["fill"])
        en["solved"] = _solve(ov, en, ov.doc[en["pno"]].rect.height)
    for pno in sorted({en["pno"] for en in entries}):  # 2. remove source text, paint fills
        page = ov.doc[pno]
        fills = [en for en in entries if en["pno"] == pno and en["fill"] is not None]
        # Normalise the content stream first: with relative text positioning
        # (Td/TL chains) MuPDF's redaction otherwise shifts the text that follows
        # a removed block (seen on sermoon-p1s p20: whole rows moved 92 pt up).
        page.clean_contents(sanitize=True)
        for en in fills:
            page.add_redact_annot(en["fill"], fill=False)
        page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE,
                              graphics=pymupdf.PDF_REDACT_LINE_ART_NONE,
                              text=pymupdf.PDF_REDACT_TEXT_REMOVE)
        for en in fills:
            if en["paint"]:
                ov.fill_rect(pno, en["fill"], en["fillcolor"])
    log = []
    for en in entries:                         # 3. text
        rect, align, _, note = en["solved"]
        spare, scale = ov.put_html(en["pno"], rect, en["html"], en["size"], en["color"], align, en["lh"])
        log.append(dict(key=en["key"], keys=en["keys"], pg=en["pno"] + 1, rect=tuple(rect),
                        fill=tuple(en["fill"]) if en["fill"] is not None else None,
                        fillcolor=en["fillcolor"], paint=en["paint"], scale=round(scale, 3), note=note))
    job.output.parent.mkdir(parents=True, exist_ok=True)
    ov.save(job.output)
    return log
