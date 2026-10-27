"""Render redrawn screens to PNG and build original-vs-new comparison sheets.
usage: python3 hmi/preview.py [name ...]"""
import os, sys
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from screens import SCREENS, SRC  # noqa: E402

OUT = HERE / 'out'
IMG = HERE.parent / 'extract' / 'img'


def page_html(body):
    return ('<!doctype html><html><head><meta charset="utf-8">'
            f'<link rel="stylesheet" href="{(HERE / "kit.css").as_uri()}">'
            '<style>body{margin:0;background:#fff}</style></head><body>' + body + '</body></html>')


def main():
    OUT.mkdir(exist_ok=True)
    names = sys.argv[1:] or list(SCREENS)
    with sync_playwright() as p:
        br = p.chromium.launch()
        pg = br.new_page(viewport={'width': 1300, 'height': 820}, device_scale_factor=1)
        for n in names:
            hp = OUT / f'{n}.html'
            hp.write_text(page_html(SCREENS[n]()))
            pg.goto(hp.as_uri())
            pg.wait_for_load_state('networkidle')
            pg.locator('.hmi').first.screenshot(path=str(OUT / f'{n}.png'))
            src = SRC.get(n)
            if src:
                a = Image.open(IMG / src).convert('RGB')
                b = Image.open(OUT / f'{n}.png').convert('RGB')
                a = a.resize((b.width, round(a.height * b.width / a.width)))
                m = Image.new('RGB', (b.width, a.height + b.height + 10), 'white')
                m.paste(a, (0, 0)); m.paste(b, (0, a.height + 10))
                m.save(OUT / f'cmp_{n}.png')
            print('ok', n)
        br.close()


if __name__ == '__main__':
    main()
