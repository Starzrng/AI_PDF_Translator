"""Cover / back cover: swap the baked-in title and QR caption, emit assets/cover.pdf + assets/back.pdf."""
import fitz
import numpy as np
from PIL import Image, ImageDraw, ImageFont

AVENIR = '/System/Library/Fonts/Avenir Next.ttc'
ARIAL = '/System/Library/Fonts/Supplemental/Arial.ttf'


def erase(im, box, pad=4):
    """Fill box column-wise with a vertical gradient between the clean rows just above/below."""
    a = np.asarray(im).astype(float)
    x0, y0, x1, y1 = box
    top = a[y0 - pad:y0, x0:x1].mean(0)
    bot = a[y1:y1 + pad, x0:x1].mean(0)
    t = np.linspace(0, 1, y1 - y0)[:, None, None]
    a[y0:y1, x0:x1] = top[None] * (1 - t) + bot[None] * t
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))


def text_c(im, cx, y, s, font, fill):
    d = ImageDraw.Draw(im)
    w = d.textlength(s, font=font)
    d.text((cx - w / 2, y), s, font=font, fill=fill)


def page_from(img, out):
    doc = fitz.open()
    p = doc.new_page(width=594.96, height=841.92)
    p.insert_image(p.rect, filename=img)
    doc.save(out, deflate=True)


cov = Image.open('extract/img/p001_x38876.png').convert('RGB')
cov = erase(cov, (510, 764, 1025, 818))
f = ImageFont.truetype(AVENIR, 50, index=2)   # Demi Bold
text_c(cov, 767, 762, 'Руководство пользователя V1.0', f, (112, 112, 112))
cov.save('assets/cover.jpg', quality=92)
page_from('assets/cover.jpg', 'assets/cover.pdf')

back = Image.open('extract/img/p161_x607.png').convert('RGB')
back = erase(back, (530, 1792, 1015, 1862))
text_c(back, 785, 1806, 'Сканируйте QR-код и следите за новостями', ImageFont.truetype(ARIAL, 31), (236, 236, 236))
back.save('assets/back.jpg', quality=92)
page_from('assets/back.jpg', 'assets/back.pdf')
print('covers ok')
