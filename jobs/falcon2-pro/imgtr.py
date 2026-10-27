"""Swap baked-in EN labels for RU in the packing-list illustration (p.6)."""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from pdft.fonts import font_path  # noqa: E402

ARIAL = font_path("regular")
def F(s): return ImageFont.truetype(ARIAL,s)
def fit(draw,text,maxw,start):
    s=start
    while s>8 and max(draw.textlength(l,font=F(s)) for l in text.split("\n"))>maxw: s-=1
    return s
def label(draw, box, text, maxsize=14, color=(45,45,45)):
    x0,y0,x1,y1=box
    draw.rectangle(box, fill=(255,255,255))
    s=fit(draw,text,(x1-x0),maxsize); f=F(s); lh=s*1.25
    lines=text.split("\n"); ty=(y0+y1)/2-lh*len(lines)/2
    for l in lines:
        w=draw.textlength(l,font=f); draw.text(((x0+x1)/2-w/2,ty),l,fill=color,font=f); ty+=lh
def text_at(draw,cx,cy,text,size,color=(45,45,45)):
    f=F(size); w=draw.textlength(text,font=f); draw.text((cx-w/2,cy),text,fill=color,font=f)

im=Image.open(HERE / "content_imgs" / "p06_x110.png").convert("RGB"); d=ImageDraw.Draw(im)
# rows 1-2 + clean row3 items
label(d,(30,85,250,114),"Винты с овальной\nголовкой ×26",13)
label(d,(345,87,500,109),"Выхлопная труба",14)
label(d,(640,87,765,109),"Хомут",14)
label(d,(865,87,1100,109),"Модуль обдува",14)
label(d,(68,290,216,314),"Силиконовая трубка",13)
label(d,(283,285,557,351),"Липа ×1 (300×300×3 мм)\nЛипа ×1 (150×150×2 мм)\nКалибровочная карта",13)
label(d,(628,290,777,314),"Блок питания",14)
label(d,(933,290,1032,314),"Защитные очки",13)
label(d,(635,634,772,662),"Руководство",13)
label(d,(910,634,1055,662),"Наклейки Creality",13)
# cramped bottom-left: whiteout band then place 3 small labels
d.rectangle((18,610,528,664),fill=(255,255,255))
text_at(d,152,615,"Блок фокусировки",10); text_at(d,152,640,"Переходник USB-A→C",10)
text_at(d,335,615,"Кабель USB-C ×2",10); text_at(d,335,640,"Ключ M4",10)
text_at(d,460,628,"Антистат. щётка",10)
im.save(HERE / "imgs_ru" / "p06_packing_ru.png"); print("saved imgs_ru/p06_packing_ru.png")
