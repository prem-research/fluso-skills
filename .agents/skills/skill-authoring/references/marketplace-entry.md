# The marketplace.json entry

Every skill needs one object in the `skills` array of `marketplace.json`. It is
maintained by hand in V1 and validated against `schemas/marketplace.schema.json`
and `scripts/validate_skills.py`. This guide covers each field.

## Template

```json
{
  "id": "contract-review",
  "display_name": "Contract Review",
  "version": "0.1.0",
  "publisher": "Fluso",
  "summary": "Review contracts for risky clauses and produce a redline summary.",
  "description": "Guides the assistant through contract review: clause extraction, risk flagging by severity, comparison against a standard, and a redline summary.",
  "categories": ["Legal"],
  "tags": ["contract", "legal", "redline", "risk"],
  "entrypoint": "SKILL.md",
  "files": ["SKILL.md"],
  "footprint": {
    "source_size_bytes": 0,
    "estimated_installed_size_bytes": 0,
    "estimated_runtime_cache_bytes": 0
  },
  "dependencies": {
    "tier": "instructions",
    "recipes": [],
    "system_capabilities": []
  },
  "safety": {
    "has_helper_scripts": false,
    "runs_install_script": false,
    "network_at_runtime": false
  }
}
```

## Fields

- **id** — kebab-case, identical to the folder name and SKILL.md `name`.
- **display_name** — human-readable title shown in the marketplace.
- **version** — semantic `x.y.z`. Start new skills at `0.1.0`.
- **publisher** — the publishing entity (e.g. `Fluso`).
- **summary** — one line; what the user gets. Shown in listings.
- **description** — a fuller catalog description of the workflow. This is the
  catalog copy, distinct from the SKILL.md frontmatter trigger description.
- **categories** — 1–2 labels, and they must equal the SKILL.md `labels` exactly.
  Allowed values only (see Taxonomy). Chosen by the user's workflow, not the
  implementation.
- **tags** — kebab-case search keywords; at least one. Add the words users search.
- **entrypoint** — always `SKILL.md`.
- **files** — the exact install manifest: every tracked file in the skill folder,
  including `SKILL.md`. If it is in the folder and tracked, it must be here; if it
  is here, it must exist. This is the field most commonly out of sync.
- **footprint** — byte sizes; see below.
- **dependencies** — runtime needs; see below.
- **safety** — honest booleans; see below.

## Taxonomy

```text
Marketing, Sales, Legal, Operations, Engineering, Finance, Research, Content, Support, Travel
```

`categories` must be a subset of this set and must equal the SKILL.md `labels`.
Do not invent free-form labels.

## Footprint

Follow the repo convention (compute it with `scripts/footprint.py`):

- `source_size_bytes` — sum of the bytes of the skill's tracked files.
- `estimated_installed_size_bytes` — `source_size_bytes + 1024`.
- `estimated_runtime_cache_bytes` — 0 for instruction-only skills; otherwise an
  estimate of what the skill downloads into user space at runtime (for example, a
  `uv`-installed Python package tree).

## Dependencies

For an instruction-only skill, keep it empty:

```json
"dependencies": { "tier": "instructions", "recipes": [], "system_capabilities": [] }
```

When the skill needs a runtime package, declare a recipe and the system
capabilities it assumes. Python via `uv` is the established pattern:

```json
"dependencies": {
  "tier": "python_uv",
  "recipes": [
    { "type": "python_uv", "project": ".", "package": "somepackage", "version": ">=1.0,<2" }
  ],
  "system_capabilities": ["python", "uv"]
}
```

- `tier` — a short label for the dependency style (e.g. `instructions`,
  `python_uv`, `built_in_audio_tool`).
- `recipes` — each needs `type`, `project`, `package`, `version`. Ship the
  matching `pyproject.toml` (or `package.json`) in the skill folder and list it in
  `files`.
- `system_capabilities` — the tools the runtime must already provide (e.g.
  `python`, `uv`).

Keep dependency setup in user space: no `sudo`, `apt`, Docker, or root-level
installs. Prefer letting the skill download into the workspace or a runtime cache
at first use.

## Safety

Answer honestly — reviewers and installers rely on these:

- `has_helper_scripts` — true if the skill ships anything under `scripts/`.
- `runs_install_script` — true if using the skill runs a setup/install step.
- `network_at_runtime` — true if the workflow makes network calls when used.

## Checklist

- `id` matches folder and SKILL.md `name`.
- `categories` equals SKILL.md `labels`, 1–2 items, all in the taxonomy.
- `files` lists every tracked file and includes `SKILL.md`.
- `footprint` computed from the real folder, not guessed.
- `dependencies` and `safety` reflect what the skill actually does.
- Any `pyproject.toml` / `package.json` the recipes reference is present and
  listed in `files`.
