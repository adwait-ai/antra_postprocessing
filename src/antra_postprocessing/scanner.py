"""Recursive music file discovery and duplicate grouping."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path

from .titles import normalize_title

MUSIC_EXTENSIONS = {"mp3", "m4a", "flac", "wav", "aac", "ogg", "wma", "opus"}


def find_music_files(root: Path, extensions: set[str] = MUSIC_EXTENSIONS) -> list[Path]:
    """Recursively find all music files under root."""
    return [
        path
        for path in root.rglob("*")
        if path.is_file() and path.suffix.lstrip(".").lower() in extensions
    ]


def group_by_title(files: list[Path]) -> dict[str, list[Path]]:
    """Group files by their normalized title, regardless of directory or extension."""
    groups: dict[str, list[Path]] = defaultdict(list)
    for path in files:
        groups[normalize_title(path)].append(path)
    return groups


def find_duplicate_groups(root: Path, extensions: set[str] = MUSIC_EXTENSIONS) -> list[list[Path]]:
    """Return groups of files (size >= 2) that are considered duplicates of each other."""
    files = find_music_files(root, extensions)
    groups = group_by_title(files)
    return [paths for paths in groups.values() if len(paths) > 1]
