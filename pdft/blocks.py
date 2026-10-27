"""Dump the text-block inventory of a source PDF.

    python -m pdft.blocks jobs/<job>/source.pdf [--force]

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
    """Bold-looking weight. Medium (500) is closer to Arial Regular than to Bold."""
    return any(w in span["font"] for w in ("Bold", "Black", "Heavy"))


def markup(spans, dcol, dsize):
    """Block text with inline emphasis as html, so translators can carry it over.

    Bold runs are marked only when the block mixes weights; colour and size only
    where they differ from the block's dominant colour and size.
    """
    mixed = len({heavy(s) for s in spans if s["text"].strip()}) > 1
    out = []
    for s in spans:
        t = s["text"]
        if mixed and heavy(s) and t.strip():
            t = f"<b>{t}</b>"
        if s["color"] != dcol and t.strip():
            t = f'<span style="color:#{s["color"] & 0xFFFFFF:06x}">{t}</span>'
        if abs(s["size"] - dsize) > 0.4 and t.strip():
            t = f'<span style="font-size:{round(s["size"], 1)}px">{t}</span>'
        out.append(t)
    return norm(" ".join(out)).replace("</b> <b>", " ")


def parts(words, bbox, size):
    """Split a one-line block where words sit far apart (table cells, two callouts).

    -> [{"bbox", "t"}, ...] with 2+ items, or None.
    """
    x0, y0, x1, y1 = bbox
    ws = sorted((w for w in words if x0 - 1 <= (w[0] + w[2]) / 2 <= x1 + 1 and y0 - 1 <= (w[1] + w[3]) / 2 <= y1 + 1),
                key=lambda w: w[0])
    gaps = sorted(b[0] - a[2] for a, b in zip(ws, ws[1:]))
    # a normal word space; capped, because one-word cells have only cell gaps
    word_gap = min(gaps[len(gaps) // 2], 0.35 * size) if gaps else 0
    split = max(0.8 * size, 3 * word_gap)    # well beyond a normal word space
    groups = []
    for w in ws:
        if groups and w[0] - groups[-1][-1][2] <= split:
            groups[-1].append(w)
        else:
            groups.append([w])
    if len(groups) < 2:
        return None
    return [{"bbox": (round(g[0][0], 1), round(min(w[1] for w in g), 1), round(g[-1][2], 1), round(max(w[3] for w in g), 1)),
             "t": " ".join(w[4] for w in g)} for g in groups]


def columns(block):
    """Split a multi-row block whose lines sit in separate columns (a label and
    a value cell fused into one block). -> parts like parts(), or None."""
    groups = []
    for line in sorted(block["lines"], key=lambda l: l["bbox"][0]):
        x0, _, x1, _ = line["bbox"]
        for g in groups:
            if x0 <= g["x1"] + 2 and x1 >= g["x0"] - 2:
                g["lines"].append(line); g["x0"] = min(g["x0"], x0); g["x1"] = max(g["x1"], x1)
                break
        else:
            groups.append({"x0": x0, "x1": x1, "lines": [line]})
    if len(groups) < 2:
        return None
    out = []
    for g in sorted(groups, key=lambda g: g["x0"]):
        ls = sorted(g["lines"], key=lambda l: l["bbox"][1])
        out.append({"bbox": (round(min(l["bbox"][0] for l in ls), 1), round(min(l["bbox"][1] for l in ls), 1),
                             round(max(l["bbox"][2] for l in ls), 1), round(max(l["bbox"][3] for l in ls), 1)),
                    "t": norm(" ".join("".join(s["text"] for s in l["spans"]) for l in ls)),
                    "nl": len({round(l["bbox"][1]) for l in ls})})
    return out


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
            o["bl"] = round(spans[0]["origin"][1], 2)                # first baseline, pt
            tops = sorted({round(line["bbox"][1], 1) for line in b["lines"]})
            steps = [y2 - y1 for y1, y2 in zip(tops, tops[1:]) if y2 - y1 > 0.5 * dsize]
            if steps:
                o["lp"] = round(sorted(steps)[len(steps) // 2], 2)   # line pitch, pt
                o["nl"] = len(steps) + 1                              # visual lines
            marked = markup(spans, dcol, dsize)
            if marked != text:
                o["h"] = marked             # source emphasis: <b>, <span style="color:...">
            if max(l["bbox"][1] for l in b["lines"]) - min(l["bbox"][1] for l in b["lines"]) < 0.5 * dsize:  # one visual row
                p = parts(words, b["bbox"], dsize)
            else:
                p = columns(b)
            if p:
                o["parts"] = p              # addressed as P{pg}b{bi}.1, .2, ...
            out.append(o)
    return out


def main():
    src = Path(sys.argv[1])
    if (src.parent / "blocks.json").exists() and "--force" not in sys.argv:
        sys.exit(f"{src.parent / 'blocks.json'} exists. Translation keys are block indices, so "
                 "rewriting it can break the job (see AGENTS.md); pass --force to overwrite.")
    out = dump(src)
    (src.parent / "blocks.json").write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
    with open(src.parent / "blocks.txt", "w", encoding="utf-8") as f:
        for o in out:
            f.write(f'P{o["pg"]:>2} b{o["bi"]:>2} sz{o["sz"]} col{o["col"]} {"B" if o["bold"] else " "} '
                    f'{o["bbox"]} {o["font"]}\n     {o["t"]}\n')
    print("blocks:", len(out))


if __name__ == "__main__":
    main()
