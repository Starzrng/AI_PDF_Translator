"""In-place overlay primitives (PyMuPDF).

A job opens its source PDF through `Overlay`, paints over each source text
block with the sampled background colour and writes the translation on top,
so artwork, tables and page furniture stay untouched. See
docs/overlay-technique.md for the gotchas these helpers encode.
"""
import html as htmlmod
import json
import re
import unicodedata
from collections import Counter

import pymupdf

from .fonts import font_path

ALIGN = {"left": 0, "center": 1, "right": 2, "justify": 3}

CSS = ("@font-face{font-family:ar;src:url(arial.ttf);}"
       "@font-face{font-family:ar;font-weight:bold;src:url(arialb.ttf);}"
       "*{font-family:ar;margin:0;padding:0;}")


def hexcol(i):
    return "#%06x" % (i & 0xFFFFFF)


def hex2rgb(h):
    h = h.lstrip("#")
    return (int(h[0:2], 16) / 255, int(h[2:4], 16) / 255, int(h[4:6], 16) / 255)


def plain(html):
    """Visible text of a translation's html."""
    return htmlmod.unescape(re.sub(r"<br\s*/?>", " ", re.sub(r"<(?!br)[^>]+>", "", html)))


def squash(text):
    """Text without any whitespace: compares content regardless of line breaks.

    MuPDF extracts a drawn "-" as a soft hyphen (U+00AD) and ";" as U+037E;
    NFKC and the hyphen map undo that.
    """
    text = unicodedata.normalize("NFKC", text.replace("\xad", "-"))
    return re.sub(r"\s+", "", text)


def parse_key(key):
    """'P12b3' -> (12, 3): 1-based page, block index from blocks.json.

    A part suffix ('P3b10.2', see blocks.parts) is ignored here; use block_bbox.
    """
    return int(key[1:key.index("b")]), int(key[key.index("b") + 1:].split(".")[0])


def block_bbox(blocks, key):
    """bbox of a block key, or of one of its parts ('P3b10.2')."""
    o = blocks[parse_key(key)]
    if "." in key:
        return o["parts"][int(key.split(".")[1]) - 1]["bbox"]
    return o["bbox"]


def load_blocks(path):
    """blocks.json (written by `python -m pdft.blocks`) keyed by (page, block)."""
    with open(path, encoding="utf-8") as f:
        return {(o["pg"], o["bi"]): o for o in json.load(f)}


class Overlay:
    """Source document plus fonts and background sampling.

    sample_step -- pixel stride when sampling the background colour
    bg_pad      -- how far (pt) beyond the rect the background is sampled
    """

    def __init__(self, src, *, zoom=3.0, sample_step=1, bg_pad=1.0):
        self.doc = pymupdf.open(src)
        self.font_file = font_path("regular")
        self.arch = pymupdf.Archive()
        self.arch.add(self.font_file, "arial.ttf")
        self.arch.add(font_path("bold"), "arialb.ttf")
        self.mfont = pymupdf.Font(fontfile=self.font_file)
        self.zoom = zoom
        self.sample_step = sample_step
        self.bg_pad = bg_pad
        self._pix = {}

    def pixmap(self, pno):
        if pno not in self._pix:
            self._pix[pno] = self.doc[pno].get_pixmap(matrix=pymupdf.Matrix(self.zoom, self.zoom))
        return self._pix[pno]

    def bg_color(self, pno, rect, pad=None):
        """Most frequent colour under rect (+pad), from the untouched source render."""
        pad = self.bg_pad if pad is None else pad
        z, step = self.zoom, self.sample_step
        pix = self.pixmap(pno)
        x0 = max(0, int((rect.x0 - pad) * z)); y0 = max(0, int((rect.y0 - pad) * z))
        x1 = min(pix.width, int((rect.x1 + pad) * z)); y1 = min(pix.height, int((rect.y1 + pad) * z))
        s, n, st = pix.samples, pix.n, pix.stride
        c = Counter()
        for yy in range(y0, y1, step):
            base = yy * st
            for xx in range(x0, x1, step):
                o = base + xx * n
                c[(s[o], s[o + 1], s[o + 2])] += 1
        if not c:
            return (1, 1, 1)
        r, g, b = c.most_common(1)[0][0]
        return (r / 255, g / 255, b / 255)

    def fill_rect(self, pno, rect, color=None):
        if color is None:
            color = self.bg_color(pno, rect)
        self.doc[pno].draw_rect(rect, color=None, fill=color)

    @staticmethod
    def _html(inner, size, color, align, lh):
        return (f'<div style="font-size:{size}px;color:{color};text-align:{align};'
                f'line-height:{lh};font-family:ar;">{inner}</div>')

    def put_html(self, pno, rect, inner, size, color="#000000", align="left", lh=1.30):
        """Rich text (<b>, <br>, justify) in the embedded Arial via insert_htmlbox.

        Returns (spare_height, scale); scale < 1 means the text was shrunk to fit.
        """
        return self.doc[pno].insert_htmlbox(rect, self._html(inner, size, color, align, lh),
                                            archive=self.arch, css=CSS)

    def measure(self, rect, inner, size, color="#000000", align="left", lh=1.30):
        """(spare_height, scale) that put_html would give, without touching the document.

        insert_htmlbox can drop the tail of a text that does not fit and still
        report scale 1.0; such a box is reported here as scale 0.
        """
        if not hasattr(self, "_scratch"):
            self._scratch = pymupdf.open()
        page = self._scratch.new_page(width=self.doc[0].rect.width, height=self.doc[0].rect.height)
        spare, scale = page.insert_htmlbox(rect, self._html(inner, size, color, align, lh), archive=self.arch, css=CSS)
        complete = squash(page.get_text()) == squash(plain(inner))
        self._scratch.delete_page(0)
        return (spare, scale if complete else 0.0)

    def free_space(self, pno, rect, direction="down", tol=30):
        """Points of clean background next to rect on the untouched source render.

        Scans rows below (or columns right/left of) rect until a pixel differs from the
        background colour: other text, lines, images, page furniture.
        """
        pix, z = self.pixmap(pno), self.zoom
        bg = [round(c * 255) for c in self.bg_color(pno, rect)]
        s, n, st = pix.samples, pix.n, pix.stride

        def clean(x, y):
            o = y * st + x * n
            return abs(s[o] - bg[0]) + abs(s[o + 1] - bg[1]) + abs(s[o + 2] - bg[2]) <= tol

        x0, y0 = max(0, int(rect.x0 * z)), max(0, int(rect.y0 * z))
        x1, y1 = min(pix.width - 1, int(rect.x1 * z)), min(pix.height - 1, int(rect.y1 * z))
        if direction in ("left", "right"):     # sideways: only the text band, so a bar
            band = (y1 - y0) // 4              # just taller than the text still counts
            y0, y1 = y0 + band, y1 - band
        if direction == "up":
            y = y0 - 1
            while y >= 0 and all(clean(x, y) for x in range(x0, x1 + 1, 2)):
                y -= 1
            return (y0 - 1 - y) / z
        if direction == "down":
            y = y1 + 1
            while y < pix.height and all(clean(x, y) for x in range(x0, x1 + 1, 2)):
                y += 1
            return (y - y1 - 1) / z
        if direction == "left":
            x = x0 - 1
            while x >= 0 and all(clean(x, y) for y in range(y0, y1 + 1, 2)):
                x -= 1
            return (x0 - 1 - x) / z
        x = x1 + 1
        while x < pix.width and all(clean(x, y) for y in range(y0, y1 + 1, 2)):
            x += 1
        return (x - x1 - 1) / z

    def fit_size(self, text, maxw, start, mins=5.0, step=0.25):
        """Largest font size <= start at which text fits maxw on one line."""
        s = start
        while s > mins and self.mfont.text_length(text, s) > maxw:
            s -= step
        return s

    def put_textbox(self, pno, rect, text, fontsize, color=(0, 0, 0), align="left"):
        self.doc[pno].insert_textbox(rect, text, fontname="ar", fontfile=self.font_file,
                                     fontsize=fontsize, color=color, align=ALIGN[align])

    def save(self, out):
        """Subset fonts first: otherwise full Arial is embedded per page (~10x size)."""
        try:
            self.doc.subset_fonts(verbose=False)
        except Exception as ex:
            print("subset warn:", ex)
        self.doc.save(out, deflate=True, garbage=4, clean=True)
        print("saved", out)
