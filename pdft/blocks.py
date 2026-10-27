"""Dump the text-block inventory of a source PDF.

    python -m pdft.blocks jobs/<job>/source.pdf

Writes blocks.json (input for Overlay jobs, keys "P{page}b{block}") and
blocks.txt (human/agent-readable listing) next to the source PDF.
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path
from statistics import mode

import pymupdf


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def heavy(span):
    return any(w in span["font"] for w in ("Bold", "Black", "Medium"))


def markup(spans, dcol):
    """Block text with inline emphasis as html, so translators can carry it over.

    Bold runs are marked only when the block mixes weights; colour only where it
    differs from the block's dominant colour.
    """
    mixed = len({heavy(s) for s in spans if s["text"].strip()}) > 1
    out = []
    for s in spans:
        t = s["text"]
        if mixed and heavy(s) and t.strip():
            t = f"<b>{t}</b>"
        if s["color"] != dcol and t.strip():
            t = f'<span style="color:#{s["color"] & 0xFFFFFF:06x}">{t}</span>'
        out.append(t)
    return norm(" ".join(out)).replace("</b> <b>", " ")


def parts(words, bbox, size):
    """Split a one-line block where words sit far apart (table cells, two callouts).

    -> [{"bbox", "t"}, ...] with 2+ items, or None.
    """
    x0, y0, x1, y1 = bbox
    ws = sorted((w for w in words if x0 - 1 <= (w[0] + w[2]) / 2 <= x1 + 1 and y0 - 1 <= (w[1] + w[3]) / 2 <= y1 + 1),
                key=lambda w: w[0])
    groups = []
    for w in ws:
        if groups and w[0] - groups[-1][-1][2] <= 2.0 * size:
            groups[-1].append(w)
        else:
            groups.append([w])
    if len(groups) < 2:
        return None
    return [{"bbox": (round(g[0][0], 1), round(min(w[1] for w in g), 1), round(g[-1][2], 1), round(max(w[3] for w in g), 1)),
             "t": " ".join(w[4] for w in g)} for g in groups]


def dump(src):
    doc = pymupdf.open(src)
    out = []
    for pno in range(doc.page_count):
        words = doc[pno].get_text("words")
        blocks = [b for b in doc[pno].get_text("dict")["blocks"] if b["type"] == 0]
        for bi, b in enumerate(blocks):
            colors, txts, sizes, fonts = [], [], [], []
            bold = False
            spans = [s for line in b["lines"] for s in line["spans"]]
            for line in b["lines"]:
                txts.append("".join(s["text"] for s in line["spans"]))
                for s in line["spans"]:
                    sizes.append(round(s["size"], 1)); colors.append(s["color"]); fonts.append(s["font"])
                    if heavy(s):
                        bold = True
            text = norm(" ".join(txts))
            if not text:
                continue
            try:
                dsize = mode(sizes)
            except Exception:
                dsize = sizes[0]
            try:
                dcol = mode(colors)
            except Exception:
                dcol = colors[0]
            o = {"pg": pno + 1, "bi": bi, "bbox": tuple(round(x, 1) for x in b["bbox"]),
                 "sz": dsize, "col": dcol, "bold": bold,
                 "font": Counter(fonts).most_common(1)[0][0], "t": text}
            marked = markup(spans, dcol)
            if marked != text:
                o["h"] = marked             # source emphasis: <b>, <span style="color:...">
            if max(l["bbox"][1] for l in b["lines"]) - min(l["bbox"][1] for l in b["lines"]) < 0.5 * dsize:  # one visual row
                p = parts(words, b["bbox"], dsize)
                if p:
                    o["parts"] = p          # addressed as P{pg}b{bi}.1, .2, ...
            out.append(o)
    return out


def main():
    src = Path(sys.argv[1])
    out = dump(src)
    (src.parent / "blocks.json").write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
    with open(src.parent / "blocks.txt", "w", encoding="utf-8") as f:
        for o in out:
            f.write(f'P{o["pg"]:>2} b{o["bi"]:>2} sz{o["sz"]} col{o["col"]} {"B" if o["bold"] else " "} '
                    f'{o["bbox"]} {o["font"]}\n     {o["t"]}\n')
    print("blocks:", len(out))


if __name__ == "__main__":
    main()
