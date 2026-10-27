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


def dump(src):
    doc = pymupdf.open(src)
    out = []
    for pno in range(doc.page_count):
        blocks = [b for b in doc[pno].get_text("dict")["blocks"] if b["type"] == 0]
        for bi, b in enumerate(blocks):
            colors, txts, sizes, fonts = [], [], [], []
            bold = False
            for line in b["lines"]:
                txts.append("".join(s["text"] for s in line["spans"]))
                for s in line["spans"]:
                    sizes.append(round(s["size"], 1)); colors.append(s["color"]); fonts.append(s["font"])
                    if any(w in s["font"] for w in ("Bold", "Black", "Medium")):
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
            out.append({"pg": pno + 1, "bi": bi, "bbox": tuple(round(x, 1) for x in b["bbox"]),
                        "sz": dsize, "col": dcol, "bold": bold,
                        "font": Counter(fonts).most_common(1)[0][0], "t": text})
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
