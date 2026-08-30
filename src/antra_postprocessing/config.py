"""Configuration loading for antra-postprocessing."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml

DEFAULT_EXTENSION_PRIORITY = ["mp3"]


@dataclass(frozen=True)
class Config:
    """User-configurable duplicate resolution preferences.

    preferred_directories: directory names checked first (closest ancestor wins),
        earlier entries take priority over later ones.
    least_preferred_directories: directory names to avoid keeping files from,
        earlier entries are less preferred than later ones.
    extension_priority: file extensions (without dot) in order of preference,
        e.g. ["mp3", "flac"]. Extensions not listed rank after all listed ones.
    """

    preferred_directories: list[str] = field(default_factory=list)
    least_preferred_directories: list[str] = field(default_factory=list)
    extension_priority: list[str] = field(default_factory=lambda: list(DEFAULT_EXTENSION_PRIORITY))


def load_config(config_path: Path) -> Config:
    """Load and validate a YAML config file into a Config object."""
    with config_path.open("r", encoding="utf-8") as f:
        raw = yaml.safe_load(f) or {}

    if not isinstance(raw, dict):
        raise ValueError(f"Config file {config_path} must contain a YAML mapping")

    preferred = raw.get("preferred_directories", []) or []
    least_preferred = raw.get("least_preferred_directories", []) or []
    extension_priority = raw.get("extension_priority", DEFAULT_EXTENSION_PRIORITY) or DEFAULT_EXTENSION_PRIORITY

    for name, value in (
        ("preferred_directories", preferred),
        ("least_preferred_directories", least_preferred),
        ("extension_priority", extension_priority),
    ):
        if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
            raise ValueError(f"Config field '{name}' must be a list of strings")

    return Config(
        preferred_directories=[d.lower() for d in preferred],
        least_preferred_directories=[d.lower() for d in least_preferred],
        extension_priority=[e.lower().lstrip(".") for e in extension_priority],
    )
