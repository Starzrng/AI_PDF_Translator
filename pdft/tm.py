"""Translation memory: reuse translations from finished overlay jobs.

Every job with blocks.json + translations.py contributes pairs
(source text of the TR key block -> translated html). Exact matches are
prefilled into a new job's skeleton, close ones are offered as hints.
"""
import difflib
import importlib.util
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def norm(s):
    s = s.replace("Ï", "ffi").lower()          # broken ffi ligature in some Creality PDFs
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"\s+([.,:;!?)\]])", r"\1", s)
    return s.strip()


def load_translations(job_dir):
    path = Path(job_dir) / "translations.py"
    spec = importlib.util.spec_from_file_location(f"tr_{abs(hash(str(path)))}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _text(blocks, key):
    """Source text of a block key or of a part key ('P3b10.2'); None if unknown."""
    m = re.fullmatch(r"P(\d+)b(\d+)(?:\.(\d+))?", key)
    o = blocks.get((int(m[1]), int(m[2]))) if m else None
    if o is None:
        return None
    if m[3]:
        parts = o.get("parts", [])
        return parts[int(m[3]) - 1]["t"] if int(m[3]) <= len(parts) else None
    return o["t"]


def _sources(exclude):
    """(name, dir) of every job with translations, incl. a job's legacy/ build.

    A job's own legacy/ counts even when the job is excluded: re-doing a job
    with the harness starts from its old translations. Later entries win on
    identical source text, so a sibling's newer translation beats legacy.
    """
    for job in sorted(p for p in (ROOT / "jobs").iterdir() if p.is_dir()):
        if job.name not in exclude:
            yield job.name, job
        if (job / "legacy").is_dir():
            yield f"{job.name}/legacy", job / "legacy"


class Memory:
    def __init__(self, exclude=()):
        self.pairs = []                       # (norm source, source, html, origin)
        for name, job in _sources(exclude):
            if not (job / "translations.py").exists() or not (job / "blocks.json").exists():
                continue
            blocks = {(o["pg"], o["bi"]): o for o in json.loads((job / "blocks.json").read_text())}
            try:
                tr = load_translations(job).TR
            except Exception as ex:          # a broken job must not block the others
                print(f"tm: skip {name}: {ex}")
                continue
            for k, e in tr.items():
                html = e.get("html")
                texts = [_text(blocks, x) for x in [k] + list(e.get("merge", []))]
                if not html or None in texts:
                    continue
                src = " ".join(texts)          # whole segment, not just its first line
                self.pairs.append((norm(src), src, html, f"{name} {k}"))
        self.exact = {p[0]: p for p in self.pairs}

    def lookup(self, text, min_ratio=0.75):
        """-> (ratio, source, html, origin) or None."""
        n = norm(text)
        if n in self.exact:
            p = self.exact[n]
            return (1.0, p[1], p[2], p[3])
        best = None
        for p in self.pairs:
            if not 0.6 < len(p[0]) / max(1, len(n)) < 1.6:
                continue
            r = difflib.SequenceMatcher(None, n, p[0], autojunk=False).ratio()
            if r >= min_ratio and (best is None or r > best[0]):
                best = (r, p[1], p[2], p[3])
        return best
