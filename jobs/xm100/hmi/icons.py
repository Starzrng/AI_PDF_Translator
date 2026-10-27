"""Cut icon glyphs out of the original raster UI and turn them into clean alpha masks.

mask  -> white glyph + alpha (tinted later with CSS mask-image), upscaled ×4
color -> RGBA crop with the flat background keyed out (multi-colour pictograms)
Catalogue entries: name: (source png in extract/img, (x0, y0, x1, y1) search region, mode)
A region in 0..1 floats is relative to the image size.
"""
import os, sys
import numpy as np
from PIL import Image, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, 'extract', 'img')
OUT = os.path.join(ROOT, 'assets', 'icons')
BTN = (0.06, 0.04, 0.94, 0.56)          # icon zone of a standalone button picture

CAT = {
    # standalone doc buttons
    'classic': ('p026_x83.png', BTN, 'mask'),
    'graphic': ('p027_x88.png', BTN, 'mask'),
    'guide': ('p028_x94.png', BTN, 'mask'),
    'edit': ('p029_x103.png', BTN, 'mask'),
    'allg': ('p029_x106.png', BTN, 'mask'),
    'g': ('p029_x109.png', BTN, 'mask'),
    'm': ('p029_x100.png', BTN, 'mask'),
    'aux': ('p030_x121.png', BTN, 'mask'),
    'switch': ('p030_x124.png', BTN, 'mask'),
    'relative': ('p030_x127.png', BTN, 'mask'),
    'fs': ('p030_x112.png', BTN, 'mask'),
    'time': ('p030_x115.png', BTN, 'mask'),
    'progctl': ('p030_x118.png', BTN, 'mask'),
    'tsm': ('p031_x135.png', BTN, 'mask'),
    'seltool': ('p031_x138.png', BTN, 'mask'),
    'seloffset': ('p032_x143.png', BTN, 'mask'),
    'jogstep': ('p032_x146.png', BTN, 'mask'),
    'workpos': ('p032_x149.png', BTN, 'mask'),
    'single': ('p033_x159.png', BTN, 'mask'),
    'cuboid': ('p033_x162.png', BTN, 'mask'),
    'cylinder': ('p033_x165.png', BTN, 'mask'),
    'toolpos': ('p033_x153.png', BTN, 'mask'),
    'probepos': ('p034_x172.png', BTN, 'mask'),
    'toolmeasure': ('p034_x178.png', BTN, 'mask'),
    'probecal': ('p035_x184.png', BTN, 'mask'),
    'toolset': ('p035_x188.png', BTN, 'mask'),
    # from full screenshots (1277x797)
    'tab_machining': ('p026_x620.png', (840, 10, 884, 52), 'mask'),
    'tab_tools': ('p026_x620.png', (955, 20, 981, 43), 'mask'),
    'tab_program': ('p026_x620.png', (1055, 14, 1085, 48), 'mask'),
    'tab_system': ('p026_x620.png', (1170, 14, 1203, 48), 'mask'),
    'control': ('p026_x620.png', (1150, 632, 1272, 680), 'mask'),
    'help': ('p026_x620.png', (1150, 727, 1272, 772), 'mask'),
    'next': ('p026_x620.png', (1010, 726, 1135, 766), 'mask'),
    'clear': ('p035_x189.png', (1150, 352, 1272, 396), 'mask'),
    'prog_g': ('p026_x620.png', (18, 392, 52, 422), 'mask'),
    'tsm_t': ('p031_x132.png', (26, 390, 62, 420), 'mask'),
    'guide_head': ('p028_x95.png', (22, 78, 62, 116), 'mask'),
    'clock': ('p027_x89.png', (330, 662, 364, 694), 'mask'),
    'tile_single': ('p032_x150.png', (100, 470, 180, 540), 'color'),
    'tile_cuboid': ('p032_x150.png', (275, 470, 355, 540), 'color'),
    'tile_cylinder': ('p032_x150.png', (450, 470, 530, 540), 'color'),
}


SB_Y = [63, 156, 249, 342, 435, 528, 621, 717]


def SB(src, i):
    """sidebar button i (7 = Help) icon zone of a full 1280×800-ish screenshot"""
    return (src, ('sb', i), 'mask')


def BB(src, i):
    return (src, ('bb', i), 'mask')


CAT.update({
    'toollist': SB('p036_x195.png', 0), 'details': BB('p036_x195.png', 2),
    'toolchange': ('p037_x204.png', BTN, 'mask'), 'spindle_rel': ('p037_x207.png', BTN, 'mask'),
    'spindle_clamp': ('p037_x210.png', BTN, 'mask'), 'mag_out': ('p037_x198.png', BTN, 'mask'),
    'mag_in': ('p037_x201.png', BTN, 'mask'),
    'localfiles': SB('p038_x227.png', 0), 'usb': SB('p038_x227.png', 1), 'sdcard': SB('p038_x227.png', 2),
    'progedit': SB('p038_x227.png', 3), 'loadfile': SB('p038_x227.png', 4),
    'preview': BB('p038_x227.png', 2), 'new': BB('p038_x227.png', 3), 'open': BB('p038_x227.png', 4),
    'select': ('p038_x230.png', BTN, 'mask'), 'cut': ('p038_x217.png', BTN, 'mask'), 'close': ('p038_x220.png', BTN, 'mask'),
    'paste': ('p038_x223.png', BTN, 'mask'), 'find': ('p038_x226.png', BTN, 'mask'), 'save': ('p038_x233.png', BTN, 'mask'),
    'copy': ('p038_x236.png', BTN, 'mask'),
    'toolpath': SB('p039_x245.png', 5), 'pan_xp': BB('p039_x245.png', 0), 'pan_xm': BB('p039_x245.png', 1),
    'pan_yp': BB('p039_x245.png', 2), 'pan_ym': BB('p039_x245.png', 3), 'back': BB('p039_x245.png', 7),
    'zoom_in': ('p039_x241.png', BTN, 'mask'), 'zoom_out': ('p039_x244.png', BTN, 'mask'),
    'view_front': ('p039_x248.png', BTN, 'mask'), 'view_top': ('p039_x251.png', BTN, 'mask'),
    'view_left': ('p039_x254.png', BTN, 'mask'), 'step': ('p040_x266.png', BTN, 'mask'),
    'ovr_minus': ('p040_x269.png', BTN, 'mask'), 'ovr_plus': ('p040_x272.png', BTN, 'mask'),
    'rot_xp': ('p040_x257.png', (0.04, 0.04, 0.48, 0.56), 'mask'), 'rot_xm': ('p040_x257.png', (0.53, 0.04, 0.97, 0.56), 'mask'),
    'rot_yp': ('p040_x260.png', (0.04, 0.04, 0.48, 0.56), 'mask'), 'rot_ym': ('p040_x260.png', (0.53, 0.04, 0.97, 0.56), 'mask'),
    'rot_zp': ('p040_x263.png', (0.04, 0.04, 0.48, 0.56), 'mask'), 'rot_zm': ('p040_x263.png', (0.53, 0.04, 0.97, 0.56), 'mask'),
    'mach_calib': SB('p043_x305.png', 0), 'axis_calib': ('p050_x354.png', BTN, 'mask'), 'probe_pair': SB('p043_x305.png', 2),
    'update': ('p051_x363.png', BTN, 'mask'), 'prev': SB('p043_x305.png', 6),
    'export_log': ('p043_x308.png', BTN, 'mask'), 'clear_data': ('p044_x314.png', BTN, 'mask'),
    'reset_params': ('p044_x317.png', BTN, 'mask'), 'alarm_info': ('p042_x293.png', BTN, 'mask'),
    'alarm_hist': ('p042_x296.png', BTN, 'mask'), 'mach_config': ('p043_x301.png', BTN, 'mask'),
    'hmi_set': ('p043_x304.png', BTN, 'mask'), 'monitor': ('p044_x320.png', BTN, 'mask'),
    'aio': ('p044_x311.png', BTN, 'mask'), 'dio': ('p045_x327.png', BTN, 'mask'), 'drive': ('p046_x332.png', BTN, 'mask'),
    'probe': ('p047_x337.png', BTN, 'mask'), 'scope': ('p048_x344.png', BTN, 'mask'),
    'network': ('p051_x359.png', BTN, 'mask'), 'online_up': ('p051_x366.png', BTN, 'mask'), 'usb_up': ('p051_x369.png', BTN, 'mask'),
    'samp_set': BB('p048_x345.png', 0), 'mon_start': BB('p048_x345.png', 1), 'ptr_a': BB('p048_x345.png', 2),
    'ptr_left': BB('p048_x345.png', 3), 'ptr_right': BB('p048_x345.png', 4), 'view3d': BB('p048_x345.png', 5),
    'exit': BB('p048_x345.png', 7),
    'x_axis': BB('p049_x349.png', 0), 'ax_zin': BB('p049_x349.png', 1), 'ax_zout': BB('p049_x349.png', 2),
    'ax_left': BB('p049_x349.png', 3), 'ax_right': BB('p049_x349.png', 4), 'autofit': BB('p049_x349.png', 5),
    'samp_pts': BB('p049_x349.png', 6),
    'pair': BB('p052_x374.png', 0), 'auxaxis': BB('p014_x38.png', 6),
})


def lum(a):
    return a[..., 0] * 0.299 + a[..., 1] * 0.587 + a[..., 2] * 0.114


def region(im, r):
    w, h = im.size
    if r[0] in ('sb', 'bb'):
        sx, sy = w / 1280, h / 800
        if r[0] == 'sb':
            y = SB_Y[r[1]]
            r = (1148, y + 6, 1274, y + 52)
        else:
            x = 3 + r[1] * 143
            r = (x + 6, 731, x + 134, 768)
        return (int(r[0] * sx), int(r[1] * sy), int(r[2] * sx), int(r[3] * sy))
    if all(isinstance(v, float) for v in r):
        w, h = im.size
        r = (int(r[0] * w), int(r[1] * h), int(r[2] * w), int(r[3] * h))
    return r


def extract(name, src, reg, mode, scale=4):
    im = Image.open(os.path.join(IMG, src)).convert('RGB')
    x0, y0, x1, y1 = region(im, reg)
    a = np.asarray(im.crop((x0, y0, x1, y1))).astype(float)
    L = lum(a)
    bg = np.median(L)                      # icon covers a minority of the zone

    if mode == 'color':
        bgc = np.median(np.concatenate([a[0], a[-1], a[:, 0], a[:, -1]]), axis=0)
        dist = np.sqrt(((a - bgc) ** 2).sum(-1))
        fgmask = dist > 28
    else:
        fgmask = L > bg + 45
        # drop button borders / highlight lines that run across the zone
        fgmask[fgmask.mean(1) > 0.55, :] = False
        fgmask[:, fgmask.mean(0) > 0.6] = False
        W = fgmask.shape[1]
        for r in range(fgmask.shape[0]):          # long thin horizontal runs = borders
            row = fgmask[r].astype(np.int8)
            d = np.diff(np.concatenate([[0], row, [0]]))
            st, en = np.nonzero(d == 1)[0], np.nonzero(d == -1)[0]
            for a0, a1 in zip(st, en):
                if a1 - a0 > 0.4 * W:
                    fgmask[r, a0:a1] = False
        fgmask[:, :4] = False
        fgmask[:, -4:] = False
    ys, xs = np.nonzero(fgmask)
    if len(xs) == 0:
        print('!! nothing found for', name)
        return
    bx0, bx1, by0, by1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
    pad = 2
    bx0, by0 = max(bx0 - pad, 0), max(by0 - pad, 0)
    bx1, by1 = min(bx1 + pad, a.shape[1]), min(by1 + pad, a.shape[0])
    c = a[by0:by1, bx0:bx1]
    if mode == 'color':
        bgc = np.median(np.concatenate([a[0], a[-1], a[:, 0], a[:, -1]]), axis=0)
        dist = np.sqrt(((c - bgc) ** 2).sum(-1))
        alpha = np.clip((dist - 12) / 60, 0, 1)
        rgba = np.dstack([c, alpha * 255]).astype(np.uint8)
        out = Image.fromarray(rgba, 'RGBA')
    else:
        Lc = lum(c)
        fg = np.percentile(Lc[Lc > bg + 45], 90)
        alpha = np.clip((Lc - bg - 8) / max(fg - bg - 8, 1), 0, 1)
        rgba = np.dstack([np.full_like(alpha, 255)] * 3 + [alpha * 255]).astype(np.uint8)
        out = Image.fromarray(rgba, 'RGBA')
    out = out.resize((out.width * scale, out.height * scale), Image.LANCZOS)
    if mode == 'mask':  # tighten soft upscaled edges
        al = np.asarray(out.getchannel('A')).astype(float) / 255
        al = np.clip((al - 0.5) * 1.6 + 0.5, 0, 1)
        out.putalpha(Image.fromarray((al * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6)))
    out.save(os.path.join(OUT, name + '.png'))
    return out.size


def draw_tools_tab():
    """the Tools-tab glyph is too faint in the sources: draw it (a ⊏ with a pointed tip)"""
    from PIL import ImageDraw
    im = Image.new('RGBA', (240, 160), (255, 255, 255, 0))
    ImageDraw.Draw(im).polygon([(36, 16), (232, 16), (232, 46), (76, 46), (76, 114), (232, 114), (232, 144),
                                (36, 144), (8, 80)], fill=(255, 255, 255, 255))
    im.resize((120, 80), Image.LANCZOS).save(os.path.join(OUT, 'tab_tools.png'))


def main():
    os.makedirs(OUT, exist_ok=True)
    draw_tools_tab()
    names = sys.argv[1:] or list(CAT)
    for n in names:
        if n != 'tab_tools':
            print(n, extract(n, *CAT[n]))


if __name__ == '__main__':
    main()
