# antra-postprocessing

Finds and deletes duplicate music files downloaded via the Antra app.

Antra sometimes downloads the same track twice, e.g.:

```
73 - Jadoo Hai Tera.mp3
12 - Jadoo Hai Tera.m4a
```

These may differ by track number, file extension, or live in different
folders. This tool recursively scans a directory, groups files that share
the same normalized title (ignoring leading track number and extension),
and deletes all but one file per group.

## Usage

```bash
uv run antra-postprocessing /path/to/music --config config.yaml
```

By default this is a dry run that only prints what would be deleted. Pass
`--apply` to actually delete files:

```bash
uv run antra-postprocessing /path/to/music --config config.yaml --apply
```

## Config

See [config.example.yaml](config.example.yaml). All fields are optional.

```yaml
preferred_directories:
  - Favorites
  - Downloads

least_preferred_directories:
  - Archive
  - Old

extension_priority:
  - mp3
  - flac
  - m4a
```

- `preferred_directories`: directory names (matched against the closest
  ancestor folder of each file) that should be kept over others, in order
  of priority.
- `least_preferred_directories`: directory names to avoid keeping files
  from, in order (later entries are less preferred).
- `extension_priority`: preferred file extensions, in order. Defaults to
  `["mp3"]`. Extensions not listed rank below all listed ones.

Extension preference is applied before directory preference: mp3 (or
whatever `extension_priority` specifies) is kept even if a duplicate in a
preferred directory has a less-preferred extension.

## Project layout

- `src/antra_postprocessing/config.py` — YAML config loading
- `src/antra_postprocessing/titles.py` — filename normalization
- `src/antra_postprocessing/scanner.py` — recursive file discovery and grouping
- `src/antra_postprocessing/ranking.py` — duplicate preference scoring
- `src/antra_postprocessing/dedupe.py` — orchestration and deletion
- `src/antra_postprocessing/cli.py` — command-line entry point
