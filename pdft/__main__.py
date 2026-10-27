"""Harness CLI for overlay jobs. Run from the repo root:

  python -m pdft inspect jobs/<id>            what is in the source: text, fonts, images, TM hits
  python -m pdft init    jobs/<id>            blocks.json + translations.py skeleton (TODOs, TM prefill)
  python -m pdft build   jobs/<id> [--pages]  build out/ PDF, then QA (exit 1 on QA errors)
  python -m pdft review  jobs/<id> [--pages]  source | translation PNG pairs in tmp/<id>/

--pages: "5", "2-4" or "2,3,20" (1-based).
"""
import argparse
import json
import re
import sys
from pathlib import Path

import pymupdf
from PIL import Image

from . import blocks as blocks_mod
from . import qa
from .job import Job, build
from .render import parse_pages
from .segments import segment
from .tm import Memory

ROOT = Path(__file__).resolve().parents[1]
REDRAW_DPI = 200      # raster below this effective resolution is a redraw candidate


def cmd_inspect(job_dir):
    src = job_dir / "source.pdf"
    doc = pymupdf.open(src)
    print(f"{src}: {doc.page_count} pages, {doc[0].rect.width:.0f}×{doc[0].rect.height:.0f} pt")
    fonts = sorted({f[3] for p in doc for f in p.get_fonts()})
    print("fonts:", ", ".join(fonts))
    if any("+" in f for f in fonts):
        print("  subset fonts: translated text goes in Arial (subsets lack Cyrillic)")
    low, vector = [], []
    for p in doc:
        if len(p.get_drawings()) > 1000:
            vector.append(p.number + 1)
        for img in p.get_images():
            for r in p.get_image_rects(img[0]):
                dpi = img[2] / max(r.width, 1) * 72
                if dpi < REDRAW_DPI and r.width > 40:
                    low.append(f"p{p.number + 1} xref{img[0]} {img[2]}×{img[3]} → {dpi:.0f} dpi")
    print("vector-heavy pages (labels sit on line art):", vector or "none")
    print(f"raster below {REDRAW_DPI} dpi (redraw candidates):", low or "none")
    bpath = job_dir / "blocks.json"
    if bpath.exists():
        segs = segment(json.loads(bpath.read_text()))
        mem = Memory(exclude={job_dir.name})
        hits = [mem.lookup(s["text"]) for s in segs]
        exact = sum(1 for h in hits if h and h[0] == 1.0)
        fuzzy = sum(1 for h in hits if h and h[0] < 1.0)
        print(f"segments: {len(segs)}; translation memory: {exact} exact, {fuzzy} close (≥75 %)")


def _lit(s):
    return repr(s)


def cmd_init(job_dir):
    src = job_dir / "source.pdf"
    if not (job_dir / "blocks.json").exists():
        out = blocks_mod.dump(src)
        (job_dir / "blocks.json").write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
        print("blocks.json:", len(out), "blocks")
    if not (job_dir / "job.json").exists():
        cfg = {"source": "source.pdf", "output": f"out/{job_dir.name}_RU.pdf", "mode": "overlay",
               "source_lang": "en", "target_lang": "ru",
               "overlay": {"sample_step": 1, "bg_pad": 0.8, "lh": 1.25, "grow": True}}
        (job_dir / "job.json").write_text(json.dumps(cfg, indent=1) + "\n", encoding="utf-8")
    segs = segment(json.loads((job_dir / "blocks.json").read_text()))
    mem = Memory(exclude={job_dir.name})
    lines = [
        '# -*- coding: utf-8 -*-',
        f'"""RU translations for {job_dir.name} (skeleton from `python -m pdft init`).',
        '',
        'Fill every html=TODO. Each t() is one segment: `merge` lists the line blocks',
        'joined into it. "TM" comments show translations of matching text from other',
        'jobs: exact ones are prefilled (check them), close ones are hints to adapt.',
        'Rules: docs/translation-conventions.md. Format: pdft/job.py docstring."""',
        '',
        'TODO = None',
        'W = "#ffffff"   # white text on dark title bars',
        '',
        'TR, OPS, KEEP = {}, [], set()',
        'def t(k, **kw): TR[k] = kw',
        'def op(pg, rect, html, **kw): OPS.append(dict(pg=pg, rect=rect, html=html, **kw))',
        'def keep(*keys): KEEP.update(keys)',
    ]
    page = None
    stats = [0, 0, 0]
    for s in segs:
        if s["pg"] != page:
            page = s["pg"]
            lines += ["", f"# {'=' * 20} PAGE {page} {'=' * 20}"]
        bb = ", ".join(f"{v:.1f}" for v in s["bbox"])
        lines.append(f'# {s["key"]}{" +" + str(len(s["merge"])) if s["merge"] else ""}  sz{s["sz"]}{" B" if s["bold"] else ""}  ({bb})')
        lines.append(f'# EN: {s["h"]}')
        hit = mem.lookup(s["text"])
        merge = f', merge={s["merge"]!r}' if s["merge"] else ""
        if hit and hit[0] == 1.0:
            html = hit[2] if s["bold"] else re.sub(r"^<b>(.*)</b>$", r"\1", hit[2])  # weight follows this source
            lines.append(f't({s["key"]!r}{merge}, html={_lit(html)})  # TM exact: {hit[3]}')
            stats[0] += 1
        else:
            if hit:
                lines.append(f'# TM {hit[0]:.0%} ({hit[3]}): {hit[1]}')
                lines.append(f'#   → {hit[2]}')
                stats[1] += 1
            lines.append(f't({s["key"]!r}{merge}, html=TODO)')
            stats[2] += 1
    target = job_dir / "translations.py"
    if target.exists():
        target = job_dir / "translations.skeleton.py"
        print("translations.py exists — skeleton written next to it")
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{target.relative_to(ROOT)}: {len(segs)} segments, {stats[0]} prefilled from TM, "
          f"{stats[1]} with TM hints, {stats[2]} TODO")


def cmd_build(job_dir, pages):
    job = Job(job_dir)
    log = build(job, pages)
    (job.output.parent / "layout.json").write_text(json.dumps(log, ensure_ascii=False, indent=1), encoding="utf-8")
    return 1 if qa.report(job, qa.check(job, log, pages), pages) else 0


def cmd_review(job_dir, pages, dpi=100):
    job = Job(job_dir)
    src, out = pymupdf.open(job.source), pymupdf.open(job.output)
    dest = ROOT / "tmp" / job.id
    dest.mkdir(parents=True, exist_ok=True)
    for n in parse_pages(",".join(map(str, pages)) if pages else None, src.page_count):
        ims = []
        for d in (src, out):
            pix = d[n - 1].get_pixmap(dpi=dpi, alpha=False)
            ims.append(Image.frombytes("RGB", (pix.width, pix.height), pix.samples))
        w, h = ims[0].size
        pair = Image.new("RGB", (w * 2 + 12, h), (200, 200, 200))
        pair.paste(ims[0], (0, 0)); pair.paste(ims[1], (w + 12, 0))
        path = dest / f"review_p{n}.png"
        pair.save(path)
        print(path.relative_to(ROOT))


def main():
    ap = argparse.ArgumentParser(prog="python -m pdft", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["inspect", "init", "build", "review"])
    ap.add_argument("job", type=Path)
    ap.add_argument("--pages")
    a = ap.parse_args()
    job_dir = a.job.resolve()
    pages = parse_pages(a.pages, 10_000) if a.pages else None
    if a.command == "inspect":
        cmd_inspect(job_dir)
    elif a.command == "init":
        cmd_init(job_dir)
    elif a.command == "build":
        sys.exit(cmd_build(job_dir, pages))
    else:
        cmd_review(job_dir, pages)


if __name__ == "__main__":
    main()
