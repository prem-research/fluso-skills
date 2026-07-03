#!/usr/bin/env python3
"""Compute the marketplace.json footprint block for a skill folder.

Sums the bytes of the skill's files and applies this repository's convention:

    source_size_bytes             = sum of file bytes in the folder
    estimated_installed_size_bytes = source_size_bytes + 1024
    estimated_runtime_cache_bytes  = 0 (edit if the skill downloads tools at runtime)

Files under forbidden components (__pycache__, .venv, node_modules, .env,
.DS_Store) and .git are ignored. Standard library only.

Usage:

    python .claude/skills/skill-authoring/scripts/footprint.py skills/contract-review
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

INSTALL_OVERHEAD = 1024

FORBIDDEN = {"__pycache__", ".venv", "node_modules", ".DS_Store", ".env", ".git"}


def iter_files(skill_dir: Path):
    for path in sorted(skill_dir.rglob("*")):
        if not path.is_file():
            continue
        if FORBIDDEN.intersection(path.parts):
            continue
        yield path


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: footprint.py <skill-dir>", file=sys.stderr)
        return 2

    skill_dir = Path(sys.argv[1])
    if not skill_dir.is_dir():
        print(f"error: {skill_dir} is not a directory", file=sys.stderr)
        return 1

    files = list(iter_files(skill_dir))
    if not files:
        print(f"error: no files found under {skill_dir}", file=sys.stderr)
        return 1

    source = sum(p.stat().st_size for p in files)
    footprint = {
        "source_size_bytes": source,
        "estimated_installed_size_bytes": source + INSTALL_OVERHEAD,
        "estimated_runtime_cache_bytes": 0,
    }

    print(f"# {skill_dir}  ({len(files)} file(s))", file=sys.stderr)
    for p in files:
        print(f"#   {p.stat().st_size:>8}  {p.relative_to(skill_dir)}", file=sys.stderr)
    print(
        "# runtime cache stays 0 unless the skill downloads tools at first use",
        file=sys.stderr,
    )

    print(json.dumps({"footprint": footprint}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
