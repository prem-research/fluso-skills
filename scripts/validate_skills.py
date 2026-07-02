#!/usr/bin/env python3
"""Cross-file consistency checks for the Fluso skill marketplace.

Validates what the JSON Schema cannot express: agreement between
marketplace.json, the skills/ directory layout, and each SKILL.md
frontmatter. Reports every violation found, then exits non-zero.

Run from anywhere: paths are resolved relative to the repository root.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
MARKETPLACE = REPO_ROOT / "marketplace.json"
SKILLS_DIR = REPO_ROOT / "skills"

# Keep in sync with README.md (Labels section) and
# schemas/marketplace.schema.json ($defs.label).
TAXONOMY = {
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
}

# Path components that must never be tracked, per the README quality checklist.
FORBIDDEN_COMPONENTS = {
    "__pycache__",
    ".venv",
    "node_modules",
    ".DS_Store",
    ".env",
}


def git_tracked_files() -> list[str]:
    out = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    return [p for p in out.split("\0") if p]


def parse_frontmatter(skill_md: Path) -> dict | str:
    """Return the frontmatter dict, or an error message string."""
    lines = skill_md.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return "missing YAML frontmatter (file must start with ---)"
    try:
        end = next(i for i, line in enumerate(lines[1:], start=1) if line.strip() == "---")
    except StopIteration:
        return "unterminated YAML frontmatter (no closing ---)"
    try:
        data = yaml.safe_load("\n".join(lines[1:end]))
    except yaml.YAMLError as exc:
        return f"frontmatter is not valid YAML: {exc}"
    if not isinstance(data, dict):
        return "frontmatter must be a YAML mapping"
    return data


def check_skill(entry: dict, tracked: list[str], errors: list[str]) -> None:
    skill_id = entry["id"]
    skill_dir = SKILLS_DIR / skill_id
    prefix = f"skills/{skill_id}"

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        errors.append(f"{prefix}: missing SKILL.md")
        return

    fm = parse_frontmatter(skill_md)
    if isinstance(fm, str):
        errors.append(f"{prefix}/SKILL.md: {fm}")
        return

    for key in ("name", "description", "labels"):
        if not fm.get(key):
            errors.append(f"{prefix}/SKILL.md: frontmatter is missing '{key}'")

    if fm.get("name") and fm["name"] != skill_id:
        errors.append(
            f"{prefix}/SKILL.md: frontmatter name {fm['name']!r} does not match "
            f"folder name and marketplace id {skill_id!r}"
        )

    labels = fm.get("labels")
    if labels:
        if not isinstance(labels, list):
            errors.append(f"{prefix}/SKILL.md: 'labels' must be a list")
        else:
            if not 1 <= len(labels) <= 2:
                errors.append(f"{prefix}/SKILL.md: use one or two labels, found {len(labels)}")
            unknown = [lbl for lbl in labels if lbl not in TAXONOMY]
            if unknown:
                errors.append(
                    f"{prefix}/SKILL.md: labels {unknown} are not in the controlled set "
                    f"(see README Labels section)"
                )
            if set(labels) != set(entry["categories"]):
                errors.append(
                    f"{prefix}: SKILL.md labels {labels} do not match "
                    f"marketplace categories {entry['categories']}"
                )

    listed = set(entry["files"])
    for rel in sorted(listed):
        if not (skill_dir / rel).is_file():
            errors.append(f"marketplace.json: {skill_id} lists {rel!r}, but {prefix}/{rel} does not exist")

    tracked_in_skill = {
        p[len(prefix) + 1 :] for p in tracked if p.startswith(prefix + "/")
    }
    unlisted = tracked_in_skill - listed
    if unlisted:
        errors.append(
            f"marketplace.json: {skill_id} 'files' is missing tracked files {sorted(unlisted)} "
            f"(the files list must be the exact install manifest)"
        )


def main() -> int:
    errors: list[str] = []

    try:
        catalog = json.loads(MARKETPLACE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"marketplace.json: cannot parse: {exc}", file=sys.stderr)
        return 1

    tracked = git_tracked_files()

    for path in tracked:
        bad = FORBIDDEN_COMPONENTS.intersection(Path(path).parts)
        if bad:
            errors.append(f"{path}: forbidden path component {sorted(bad)} must not be tracked")

    skills = catalog.get("skills", [])
    ids = [entry["id"] for entry in skills]
    if len(ids) != len(set(ids)):
        dupes = sorted({i for i in ids if ids.count(i) > 1})
        errors.append(f"marketplace.json: duplicate skill ids {dupes}")

    dirs = sorted(p.name for p in SKILLS_DIR.iterdir() if p.is_dir()) if SKILLS_DIR.is_dir() else []
    for missing in sorted(set(ids) - set(dirs)):
        errors.append(f"marketplace.json: skill {missing!r} has no skills/{missing}/ directory")
    for orphan in sorted(set(dirs) - set(ids)):
        errors.append(f"skills/{orphan}/: directory has no marketplace.json entry")

    for entry in skills:
        if entry["id"] in dirs:
            check_skill(entry, tracked, errors)

    if errors:
        print(f"validate-skills: {len(errors)} problem(s) found:\n", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
