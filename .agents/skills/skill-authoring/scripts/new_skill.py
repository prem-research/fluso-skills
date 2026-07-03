#!/usr/bin/env python3
"""Scaffold a new marketplace skill.

Creates skills/<id>/SKILL.md with valid frontmatter and prints a ready-to-paste
marketplace.json entry plus the next steps. Refuses to overwrite an existing
skill. Standard library only; no third-party dependencies.

Run from the repository root, for example:

    python .claude/skills/skill-authoring/scripts/new_skill.py \
        --id contract-review \
        --display-name "Contract Review" \
        --labels Legal \
        --summary "Review contracts for risky clauses and produce a redline summary."
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# Keep in sync with schemas/marketplace.schema.json and scripts/validate_skills.py.
TAXONOMY = [
    "Marketing",
    "Sales",
    "Legal",
    "Operations",
    "Engineering",
    "Finance",
    "Research",
    "Content",
    "Support",
    "Travel",
]

ID_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def find_repo_root(start: Path) -> Path:
    """Walk upward until a directory containing marketplace.json is found."""
    for candidate in [start, *start.parents]:
        if (candidate / "marketplace.json").is_file():
            return candidate
    # Fall back to the current directory; the caller will get a clear error later.
    return start


def slugify(text: str) -> str:
    text = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return text


def build_skill_md(skill_id: str, description: str, labels: list[str]) -> str:
    label_block = "\n".join(f"  - {label}" for label in labels)
    title = " ".join(word.capitalize() for word in skill_id.split("-"))
    return f"""---
name: {skill_id}
description: {description}
labels:
{label_block}
---

# {title}

One-line purpose: state the single job this skill owns and the outcome it
produces.

## Workflow

1. First step.
2. Second step.
3. Third step.

## Rules

- Non-negotiable constraints and safety limits.

## Output

Describe the deliverable and where it is saved.

## Quality check

- Confirm the key properties before finishing.
"""


def build_entry(args: argparse.Namespace, labels: list[str]) -> dict:
    return {
        "id": args.id,
        "display_name": args.display_name or " ".join(
            w.capitalize() for w in args.id.split("-")
        ),
        "version": "0.1.0",
        "publisher": args.publisher,
        "summary": args.summary or "TODO: one-line summary of what the user gets.",
        "description": args.summary or "TODO: fuller catalog description of the workflow.",
        "categories": labels,
        "tags": [t for t in (args.tags.split(",") if args.tags else []) if t] or [
            slugify(args.id)
        ],
        "entrypoint": "SKILL.md",
        "files": ["SKILL.md"],
        "footprint": {
            "source_size_bytes": 0,
            "estimated_installed_size_bytes": 0,
            "estimated_runtime_cache_bytes": 0,
        },
        "dependencies": {"tier": "instructions", "recipes": [], "system_capabilities": []},
        "safety": {
            "has_helper_scripts": False,
            "runs_install_script": False,
            "network_at_runtime": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--id", required=True, help="kebab-case skill id / folder / name")
    parser.add_argument("--display-name", default="", help="human-readable title")
    parser.add_argument(
        "--labels",
        default="",
        help="comma-separated labels from the taxonomy (1-2)",
    )
    parser.add_argument("--summary", default="", help="one-line summary for the catalog")
    parser.add_argument(
        "--description",
        default="",
        help="SKILL.md trigger description; defaults to a TODO placeholder",
    )
    parser.add_argument("--tags", default="", help="comma-separated search tags")
    parser.add_argument("--publisher", default="Fluso", help="publisher name")
    args = parser.parse_args()

    if not ID_RE.match(args.id):
        print(f"error: id {args.id!r} is not kebab-case (^[a-z0-9]+(-[a-z0-9]+)*$)", file=sys.stderr)
        return 2

    labels = [l.strip() for l in args.labels.split(",") if l.strip()]
    if not 1 <= len(labels) <= 2:
        print("error: provide 1 or 2 --labels from the taxonomy", file=sys.stderr)
        print(f"       taxonomy: {', '.join(TAXONOMY)}", file=sys.stderr)
        return 2
    unknown = [l for l in labels if l not in TAXONOMY]
    if unknown:
        print(f"error: labels {unknown} are not in the taxonomy", file=sys.stderr)
        print(f"       taxonomy: {', '.join(TAXONOMY)}", file=sys.stderr)
        return 2

    repo_root = find_repo_root(Path.cwd())
    skill_dir = repo_root / "skills" / args.id
    skill_md = skill_dir / "SKILL.md"
    if skill_md.exists():
        print(f"error: {skill_md} already exists; refusing to overwrite", file=sys.stderr)
        return 1

    summary_clause = (args.summary or "...").rstrip(". ").strip() or "..."
    description = args.description or (
        f"TODO: what the skill does. Use when the user asks to {summary_clause}."
    )

    skill_dir.mkdir(parents=True, exist_ok=True)
    skill_md.write_text(build_skill_md(args.id, description, labels), encoding="utf-8")

    entry = build_entry(args, labels)

    rel = skill_md.relative_to(repo_root)
    print(f"created {rel}\n")
    print("Paste this object into the `skills` array in marketplace.json:\n")
    print(json.dumps(entry, indent=2, ensure_ascii=False))
    print()
    print("Next steps:")
    print(f"  1. Write the description and body in {rel}")
    print("  2. Add the entry above to marketplace.json")
    print(
        f"  3. Compute footprint: "
        f"python .claude/skills/skill-authoring/scripts/footprint.py skills/{args.id}"
    )
    print("  4. Validate: python scripts/validate_skills.py && pre-commit run --all-files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
