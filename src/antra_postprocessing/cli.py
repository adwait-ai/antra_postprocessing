"""Command-line entry point for antra-postprocessing."""

from __future__ import annotations

import argparse
from pathlib import Path

from .config import Config, load_config
from .dedupe import delete_duplicates, resolve_duplicates


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Find and delete duplicate music files downloaded via Antra."
    )
    parser.add_argument("root", type=Path, help="Directory to scan recursively")
    parser.add_argument(
        "--config",
        type=Path,
        default=None,
        help="Path to YAML config with directory/extension preferences",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually delete files. Without this flag, only prints what would be deleted",
    )
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)

    config = load_config(args.config) if args.config else Config()
    resolutions = resolve_duplicates(args.root, config)

    if not resolutions:
        print("No duplicates found.")
        return

    for resolution in resolutions:
        print(f"KEEP:   {resolution.keep}")
        for path in resolution.delete:
            print(f"DELETE: {path}")

    deleted = delete_duplicates(resolutions, dry_run=not args.apply)
    action = "Deleted" if args.apply else "Would delete"
    print(f"\n{action} {len(deleted)} file(s) across {len(resolutions)} duplicate group(s).")
    if not args.apply:
        print("Re-run with --apply to actually delete these files.")


if __name__ == "__main__":
    main()
