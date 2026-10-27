"""Group line-level text blocks into paragraph segments.

Some PDFs store every visual line as its own block. Translating line by line
breaks sentences, so consecutive blocks of one column with the same size and
colour and a line-sized gap become one segment: the translation is keyed on
the first block and the rest are listed in `merge`.
"""
import re

LETTERS = re.compile(r"[A-Za-zÀ-ɏЀ-ӿ一-鿿]")


def has_letters(text):
    return bool(LETTERS.search(text))


def key(o):
    return f'P{o["pg"]}b{o["bi"]}'


def _continues(seg_last, seg_x0, o):
    if o["pg"] != seg_last["pg"] or o["sz"] != seg_last["sz"] or o["col"] != seg_last["col"]:
        return False
    centred = abs((o["bbox"][0] + o["bbox"][2]) - (seg_last["bbox"][0] + seg_last["bbox"][2])) <= 5.0
    if abs(o["bbox"][0] - seg_x0) > 2.0 and not centred:   # same left edge, or centred lines
        return False
    gap = o["bbox"][1] - seg_last["bbox"][3]
    return -0.25 * o["sz"] <= gap <= 0.6 * o["sz"]   # line boxes may overlap slightly


def _units(blocks):
    """Blocks, with multi-part blocks (blocks.parts) replaced by their parts."""
    for o in blocks:
        if "parts" not in o:
            yield o
            continue
        for i, p in enumerate(o["parts"], 1):
            yield dict(o, bbox=p["bbox"], t=p["t"], h=p["t"], bi=f'{o["bi"]}.{i}')


def segment(blocks):
    """blocks: list from blocks.json -> list of segments (dicts) in reading order."""
    segs = []
    by_page = {}
    for o in _units(blocks):
        by_page.setdefault(o["pg"], []).append(o)
    for pg in sorted(by_page):
        open_segs = []
        for o in sorted(by_page[pg], key=lambda o: (o["bbox"][1], o["bbox"][0])):
            if not has_letters(o["t"]):
                continue
            for s in open_segs:
                if _continues(s["blocks"][-1], s["x0"], o):
                    s["blocks"].append(o)
                    break
            else:
                s = {"blocks": [o], "x0": o["bbox"][0]}
                open_segs.append(s)
        for s in open_segs:
            bs = s["blocks"]
            segs.append({
                "key": key(bs[0]),
                "merge": [key(b) for b in bs[1:]],
                "pg": pg,
                "bbox": (min(b["bbox"][0] for b in bs), min(b["bbox"][1] for b in bs),
                         max(b["bbox"][2] for b in bs), max(b["bbox"][3] for b in bs)),
                "sz": bs[0]["sz"],
                "bold": any(b["bold"] for b in bs),
                "font": bs[0].get("font", ""),
                "text": " ".join(b["t"] for b in bs),
                "h": " ".join(b.get("h", b["t"]) for b in bs),
            })
    segs.sort(key=lambda s: (s["pg"], s["bbox"][1], s["bbox"][0]))
    return segs
