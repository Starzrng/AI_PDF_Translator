"""Pixel regression check between two PDFs.

    python -m pdft.diff old.pdf new.pdf [dpi]

Renders both page by page and prints pages whose pixels differ. Exit code 1
on any difference, so a refactor that must not change output is provable.
"""
import sys

import pymupdf
from PIL import Image, ImageChops


def page_image(doc, i, dpi):
    pix = doc[i].get_pixmap(dpi=dpi, alpha=False)
    return Image.frombytes("RGB", (pix.width, pix.height), pix.samples)


def main():
    a, b = pymupdf.open(sys.argv[1]), pymupdf.open(sys.argv[2])
    dpi = int(sys.argv[3]) if len(sys.argv) > 3 else 72
    print(f"pages: {a.page_count} vs {b.page_count}")
    worst = 0.0 if a.page_count == b.page_count else 100.0
    for i in range(min(a.page_count, b.page_count)):
        ia, ib = page_image(a, i, dpi), page_image(b, i, dpi)
        if ia.size != ib.size:
            print(f"p{i + 1}: size {ia.size} vs {ib.size}")
            worst = 100.0
            continue
        mask = ImageChops.difference(ia, ib).convert("L").point(lambda v: 255 if v > 24 else 0)
        n = mask.histogram()[255]
        pct = 100 * n / (ia.width * ia.height)
        worst = max(worst, pct)
        if n:
            print(f"p{i + 1}: {n} px differ ({pct:.3f}%)")
    print(f"max diff: {worst:.3f}%")
    sys.exit(1 if worst else 0)


if __name__ == "__main__":
    main()
