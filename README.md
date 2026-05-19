# Fluso Skills

Public skill catalog for the [Fluso](https://fluso.ai/) Skill Marketplace.

This repository stores optional skills that can be discovered in Fluso and added to a user's workspace. These are different from Fluso's built-in skills: marketplace skills live here, are listed through `marketplace.json`, and are installed only when a user chooses to add them.

Marketplace skills can be simple instruction packages, or they can include reviewed helper scripts, references, and assets that let Fluso prepare a real workflow inside the user's workspace.

## How It Works

Fluso reads `marketplace.json` from this public repository. Each entry in that catalog points to a folder under `skills/<skill-id>/`.

When a user clicks **Add** in Fluso:

1. Fluso reads the skill entry from `marketplace.json`.
2. Fluso copies the listed files from `skills/<skill-id>/` into the user's workspace skills directory.
3. The runtime reloads idle sessions so the skill can be used.
4. When the skill is used, Fluso can follow its instructions and run reviewed helper scripts to prepare user-space dependencies if needed.
5. The user can later remove the skill from their workspace.

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
- `scripts/`, `references/`, and `assets/` are optional and should only be included when they directly support the skill.

## What Is a Skill?

A skill is a self-contained workflow package that teaches Fluso how to handle a specific task. It can include instructions only, or it can include small supporting files that help Fluso produce the requested output.

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
   - `scripts/` for reviewed helpers, validation, setup, or deterministic workflow steps.
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
  "summary": "Plan, script, render audio drafts, and package podcast episodes.",
  "description": "Guides Fluso through end-to-end podcast production with outlines, scripts, audio drafts, show notes, chapters, and launch copy.",
  "categories": ["Content"],
  "tags": ["podcast", "audio", "script", "show-notes"],
  "entrypoint": "SKILL.md",
  "files": [
    "SKILL.md"
  ],
  "footprint": {
    "source_size_bytes": 4055,
    "estimated_installed_size_bytes": 5079,
    "estimated_runtime_cache_bytes": 0
  },
  "dependencies": {
    "tier": "built_in_audio_tool",
    "recipes": [],
    "system_capabilities": []
  },
  "safety": {
    "has_helper_scripts": false,
    "runs_install_script": false,
    "network_at_runtime": true
  }
}
```

For V1, `marketplace.json` is updated manually. The `files` list is important: it tells Fluso exactly which files are part of the installable skill. `estimated_runtime_cache_bytes` is optional, but useful for skills that may download large user-space tools only when the skill runs.

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

## Dependencies And Runtime Setup

Prefer instruction-only skills when that is enough. When a real workflow needs tools or packages, the skill can include a reviewed setup helper that prepares dependencies in user space when the skill is used.

Supported V1 patterns:

- Python dependencies through `pyproject.toml` and `uv`.
- Node dependencies through `package.json`.
- Project-local npm setup helpers, for tools like CLIs or static binaries.
- Small bundled static binaries when reviewed and necessary.
- Runtime checks that explain missing system capabilities clearly.

Avoid:

- `sudo`, `apt`, Docker, or root-level setup.
- Committed dependency folders such as `node_modules/` or `.venv/`.
- Large generated caches or build artifacts.
- Hidden or broad scripts that are hard to review.

Helper scripts are allowed, but they should be narrow, readable, and tied directly to the skill's workflow. They may download user-space dependencies into the workspace, a shared runtime cache, or a project-local tools directory, but they should not mutate system packages or require root access.

## Quality Checklist

Before opening a PR, check that:

- `SKILL.md` is clear and concise.
- `name`, folder name, and marketplace `id` match.
- The skill has one or two valid labels.
- No secrets, tokens, credentials, or private data are committed.
- No `.git`, `node_modules`, `.venv`, `__pycache__`, or generated caches are included.
- Any scripts are small, purposeful, reviewable, and documented by the skill.
- Any dependency setup stays in user space and explains what it downloads.
- `marketplace.json` describes the skill accurately.
- The skill can be understood by a reviewer without reading unrelated context.

## Current Status

This repository is the public source for Fluso's optional marketplace skills. Current skills include:

- `podcast-production` — helps Fluso plan, script, render audio drafts, and package podcast episodes.
- `osint-investigation` — guides structured public-source investigation workflows for domains, organizations, public profiles, metadata, threat intelligence, and evidence-based reports.

These skills do not bundle Chromium, FFmpeg, local TTS models, generated caches, or heavy recon frameworks by default, so they stay lightweight for marketplace install testing.

The catalog is intentionally simple for V1: add skill files, update `marketplace.json`, and submit a PR. Future improvements may include CI validation, automatic marketplace catalog generation, size checks, dependency review automation, and template-based skill creation.
