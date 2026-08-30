"""Orchestration: find duplicate groups and plan which files to delete."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .config import Config
from .ranking import rank_key
from .scanner import MUSIC_EXTENSIONS, find_duplicate_groups


@dataclass(frozen=True)
class DuplicateResolution:
    keep: Path
    delete: list[Path]


def resolve_duplicates(root: Path, config: Config) -> list[DuplicateResolution]:
    """Find duplicate groups under root and decide which file to keep in each group."""
    groups = find_duplicate_groups(root, MUSIC_EXTENSIONS)

    resolutions = []
    for group in groups:
        ranked = sorted(group, key=lambda path: rank_key(path, root, config))
        resolutions.append(DuplicateResolution(keep=ranked[0], delete=ranked[1:]))
    return resolutions


def delete_duplicates(resolutions: list[DuplicateResolution], dry_run: bool = True) -> list[Path]:
    """Delete the losing files from each resolution. Returns the list of deleted (or to-be-deleted) paths."""
    deleted = []
    for resolution in resolutions:
        for path in resolution.delete:
            deleted.append(path)
            if not dry_run:
                path.unlink()
    return deleted
