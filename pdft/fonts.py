"""Locate the Cyrillic-capable TTF fonts used for translated text.

Defaults are macOS Arial. Override per machine with the environment variables
PDFT_FONT_REGULAR / PDFT_FONT_BOLD.
"""
import os
from pathlib import Path

DEFAULTS = {
    "regular": "/System/Library/Fonts/Supplemental/Arial.ttf",
    "bold": "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
}


def font_path(style: str = "regular") -> str:
    var = f"PDFT_FONT_{style.upper()}"
    path = os.environ.get(var, DEFAULTS[style])
    if not Path(path).exists():
        raise FileNotFoundError(f"Font not found: {path}. Set {var} to a Cyrillic-capable .ttf")
    return path
