"""Picture crops (no text) reused inside redrawn screens -> assets/hmi_img."""
from pathlib import Path
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / 'extract' / 'img'
OUT = ROOT / 'assets' / 'hmi_img'


def keyed(src, box, bg_pt, tol=(10, 40), scale=1):
    """Crop and make the flat background transparent (bg colour sampled at bg_pt)."""
    im = Image.open(IMG / src).convert('RGB')
    bgc = np.array(im.getpixel(bg_pt), float)
    a = np.asarray(im.crop(box)).astype(float)
    d = np.sqrt(((a - bgc) ** 2).sum(-1))
    al = np.clip((d - tol[0]) / tol[1], 0, 1)
    out = Image.fromarray(np.dstack([a, al * 255]).astype(np.uint8), 'RGBA')
    if scale != 1:
        out = out.resize((out.width * scale, out.height * scale), Image.LANCZOS)
    return out


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    g = Image.open(IMG / 'p028_x95.png').convert('RGB')
    g.crop((470, 236, 1010, 640)).save(OUT / 'guide_bg.png')
    keyed('p027_x89.png', (40, 500, 258, 560), (30, 530), (10, 40)).save(OUT / 'endmill.png')
    # tool list pictures (p036 tool page): spindle probe + magazine slots 1..6
    rows = [128, 183, 236, 289, 341, 394, 446]
    names = ['probe', 'endmill', 'taper_ball', 'taper_ball2', 'ball', 'reamer', 'bullnose']
    for n, cy in zip(names, rows):
        keyed('p036_x195.png', (282, cy - 18, 420, cy + 18), (272, cy), (14, 40), 2).save(OUT / f'tool_{n}.png')
    # boot screen without the status line
    b = Image.open(IMG / 'p014_x37.png').convert('RGB')
    a = np.asarray(b).astype(float)
    a[645:685, 405:760] = a[688:693, 405:760].mean(0)[None]
    Image.fromarray(a.astype(np.uint8)).save(OUT / 'boot_bg.png')
    # toolpath 3D view (p039): black viewport without the "80%" label
    t = Image.open(IMG / 'p039_x245.png').convert('RGB')
    v = t.crop((25, 148, 1118, 595))
    a = np.asarray(v).copy()
    a[0:40, 980:1093] = 0
    Image.fromarray(a).save(OUT / 'toolpath_view.png')
    # probe illustrations (p047 status panel, p052 pairing steps)
    keyed('p047_x339.png', (880, 190, 1100, 500), (875, 300), (8, 30)).save(OUT / 'probe_big.png')
    pp = Image.open(IMG / 'p052_x374.png').convert('RGB')
    a = np.asarray(pp).astype(float)
    a[474:522, 284:384] = a[526:531, 284:384].mean(0).mean(0)[None, None]   # remove green CN hint text
    Image.fromarray(a.astype(np.uint8)).crop((150, 228, 430, 545)).save(OUT / 'pair_1.png')
    pp.crop((515, 228, 735, 545)).save(OUT / 'pair_2.png')
    pp.crop((845, 228, 1065, 545)).save(OUT / 'pair_3.png')
    print('crops ok')


if __name__ == '__main__':
    main()
