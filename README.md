# Fluso Skills

Public skill catalog for the [Fluso](https://fluso.ai/) Skill Marketplace.

This repository stores optional skills that can be discovered in Fluso and added to a user's workspace. These are different from Fluso's built-in skills: marketplace skills live here, are listed through `marketplace.json`, and are installed only when a user chooses to add them.

## How It Works

Fluso reads `marketplace.json` from this public repository. Each entry in that catalog points to a folder under `skills/<skill-id>/`.

When a user clicks **Add** in Fluso:

1. Fluso reads the skill entry from `marketplace.json`.
2. Fluso copies the matching `skills/<skill-id>/` folder into the user's workspace skills directory.
3. The runtime reloads idle sessions so the skill can be used.
4. The user can later remove the skill from their workspace.

Because this repository is public, Fluso does not need a GitHub token to discover or install skills. Write access is only needed when adding or updating skills in this repository.

## Repository Structure

```text
marketplace.json
skills/
  example-skill/
    SKILL.md
    scripts/
    references/
    assets/
```

- `marketplace.json` is the V1 marketplace catalog.
- `skills/<skill-id>/SKILL.md` is required for every skill.
- `scripts/`, `references/`, and `assets/` are optional and should only be included when useful.

## What Is a Skill?

A skill is a self-contained instruction package that teaches Fluso how to handle a specific workflow.

Every skill must include a `SKILL.md` file with YAML frontmatter:

```yaml
---
name: podcast-production
description: Plan, script, and prepare podcast episodes. Use when the user asks for podcast workflows, show notes, episode planning, or production support.
labels:
  - Content
---
```

The `name` must match the folder name and the `id` in `marketplace.json`.

## Adding a Skill

1. Create a folder under `skills/<skill-id>/`.
2. Add a `SKILL.md` file with `name`, `description`, and `labels`.
3. Add optional resources if needed:
   - `scripts/` for small deterministic helpers.
   - `references/` for deeper documentation.
   - `assets/` for templates, images, sample files, or other reusable resources.
4. Add the skill to `marketplace.json`.
5. Open a pull request.

Keep skill IDs in kebab case, for example `podcast-production`, `contract-review`, or `revenue-forecast`.

## Marketplace Entry

Each skill needs a matching `marketplace.json` entry:

```json
{
  "id": "podcast-production",
  "display_name": "Podcast Production",
  "version": "0.1.0",
  "publisher": "Fluso",
  "summary": "Plan, script, and prepare podcast episodes.",
  "description": "Use this skill for podcast planning, show notes, episode outlines, and production workflows.",
  "categories": ["Content"],
  "tags": ["podcast", "audio", "production"],
  "license": "MIT",
  "entrypoint": "SKILL.md",
  "footprint": {
    "source_size_bytes": 1024,
    "estimated_installed_size_bytes": 2048
  },
  "dependencies": {
    "tier": "instruction_only",
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

For V1, `marketplace.json` is updated manually. Later, CI may generate or update it automatically from the skill folders.

## Labels

Use one or two labels from this controlled set:

```text
Marketing, Sales, Legal, Operations, Engineering, Finance, Research, Content, Support
```

Choose labels based on the user's workflow, not the implementation detail.

Examples:

- Podcast workflow -> `Content`
- Contract review -> `Legal`
- Revenue forecast -> `Finance`
- Browser automation -> `Engineering`
- Lead follow-up -> `Sales`

Do not invent free-form labels such as `Podcast`, `AI`, or `Productivity`.

## Dependencies

Prefer instruction-only skills when possible. If a skill needs dependencies, keep the install path explicit and user-space friendly.

Supported V1 patterns:

- Python dependencies through `pyproject.toml` and `uv`.
- Node dependencies through `package.json`.
- Small bundled static binaries when reviewed and necessary.

Avoid:

- Arbitrary install scripts.
- `sudo`, `apt`, Docker, or root-level setup.
- Committed dependency folders such as `node_modules/` or `.venv/`.
- Large generated caches or build artifacts.

## Quality Checklist

Before opening a PR, check that:

- `SKILL.md` is clear and concise.
- `name`, folder name, and marketplace `id` match.
- The skill has one or two valid labels.
- No secrets, tokens, credentials, or private data are committed.
- No `.git`, `node_modules`, `.venv`, `__pycache__`, or generated caches are included.
- Any scripts are small, purposeful, and documented by the skill.
- `marketplace.json` describes the skill accurately.
- The skill can be understood by a reviewer without reading unrelated context.

## Current Status

This repository is the public source for Fluso's optional marketplace skills. The catalog is intentionally simple for V1: add skill files, update `marketplace.json`, and submit a PR.

Future improvements may include CI validation, automatic marketplace catalog generation, size checks, and template-based skill creation.
