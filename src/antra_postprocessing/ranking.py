"""Ranking logic to decide which duplicate file to keep."""

from __future__ import annotations

from pathlib import Path

from .config import Config


def _directory_rank(path: Path, root: Path, config: Config) -> int:
    """Rank a file by its ancestor directory names, closest to the file wins first match.

    Lower rank is more preferred. Preferred directories occupy the lowest ranks
    (in list order), then a neutral rank for unmatched files, then least-preferred
    directories (in list order, later entries rank worse).
    """
    neutral_rank = len(config.preferred_directories)
    ancestors = []
    for parent in path.parents:
        if parent == root or root not in parent.parents:
            break
        ancestors.append(parent.name.lower())

    for name in ancestors:
        if name in config.preferred_directories:
            return config.preferred_directories.index(name)
        if name in config.least_preferred_directories:
            return neutral_rank + 1 + config.least_preferred_directories.index(name)

    return neutral_rank


def _extension_rank(path: Path, config: Config) -> int:
    """Lower rank is more preferred. Unlisted extensions rank after all listed ones."""
    ext = path.suffix.lstrip(".").lower()
    if ext in config.extension_priority:
        return config.extension_priority.index(ext)
    return len(config.extension_priority)


def rank_key(path: Path, root: Path, config: Config) -> tuple[int, int, str]:
    """Sort key for a candidate file; lowest value is the preferred file to keep.

    Extension preference takes priority over directory preference. The path string
    is used as a final tiebreaker for deterministic results.
    """
    return (_extension_rank(path, config), _directory_rank(path, root, config), str(path))
