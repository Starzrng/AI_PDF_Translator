"""Render PDF pages to PNG for visual review.

    python -m pdft.render file.pdf [pages] [--dpi 110] [--out tmp/render]

pages: "5", "3-7" or "1,4,9" (1-based); default all. PNGs land in tmp/
(gitignored), named <pdf stem>_p<N>.png.
"""
import argparse
from pathlib import Path

import pymupdf


def parse_pages(spec, count):
    if not spec:
        return list(range(1, count + 1))
    pages = []
    for part in spec.split(","):
        lo, _, hi = part.partition("-")
        pages.extend(range(int(lo), int(hi or lo) + 1))
    return pages


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf", type=Path)
    ap.add_argument("pages", nargs="?")
    ap.add_argument("--dpi", type=int, default=110)
    ap.add_argument("--out", type=Path, default=Path("tmp/render"))
    args = ap.parse_args()
    doc = pymupdf.open(args.pdf)
    args.out.mkdir(parents=True, exist_ok=True)
    for n in parse_pages(args.pages, doc.page_count):
        path = args.out / f"{args.pdf.stem}_p{n}.png"
        doc[n - 1].get_pixmap(dpi=args.dpi).save(path)
        print(path)


if __name__ == "__main__":
    main()
