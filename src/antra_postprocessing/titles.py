"""Filename normalization to identify duplicate tracks."""

from __future__ import annotations

import re
from pathlib import Path

# Matches a leading track number prefix like "73 - " or "73. " or "73_"
_LEADING_TRACK_NUMBER_RE = re.compile(r"^\s*\d+\s*[-._]\s*")
_WHITESPACE_RE = re.compile(r"\s+")


def normalize_title(file_path: Path) -> str:
    """Derive a comparison key for a music file, ignoring track number and extension.

    "73 - Jadoo Hai Tera.mp3" and "12 - Jadoo Hai Tera.m4a" both normalize to
    "jadoo hai tera".
    """
    stem = file_path.stem
    stem = _LEADING_TRACK_NUMBER_RE.sub("", stem)
    stem = _WHITESPACE_RE.sub(" ", stem).strip()
    return stem.lower()
