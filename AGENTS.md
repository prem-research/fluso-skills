# AGENTS.md

Working notes for agents operating in the Fluso Skills marketplace repository.
Read this before creating or editing skills so changes pass CI on the first try.

## What this repo is

A public catalog of optional skills for the Fluso Skill Marketplace. Fluso reads
`marketplace.json` from this repo and, on install, copies a skill's listed files
into a user's workspace. Everything here is public source — never commit secrets,
tokens, credentials, or private data.

A skill is a self-contained workflow package. At minimum it is a single
`SKILL.md` with YAML frontmatter; it may also ship `references/`, `scripts/`, and
`assets/` when a real workflow needs them.

## Layout

```text
marketplace.json                 # V1 catalog; one entry per skill (hand-maintained)
schemas/marketplace.schema.json  # JSON Schema the catalog is validated against
scripts/validate_skills.py       # cross-file consistency checks CI runs
skills/<skill-id>/SKILL.md        # required entrypoint for every skill
skills/<skill-id>/references/     # optional deeper docs
skills/<skill-id>/scripts/        # optional reviewed helpers
skills/<skill-id>/assets/         # optional templates/samples
.pre-commit-config.yaml           # local + CI checks (pre-commit)
.github/workflows/ci.yml          # runs `pre-commit run --all-files` on PRs and main
.claude/skills/                   # meta-skills for authoring (this repo's tooling, not catalog entries)
```

## Invariants CI enforces

These are checked by `scripts/validate_skills.py` and the JSON Schema. Breaking any
one fails CI, so verify them before opening a PR:

- **Identity match**: a skill's frontmatter `name`, its folder name, and its
  `marketplace.json` `id` must all be the identical kebab-case string.
- **Labels equal categories**: SKILL.md `labels` must match `marketplace.json`
  `categories` exactly (same set), be 1–2 items, and come from the taxonomy below.
- **Files list is the install manifest**: `marketplace.json` `files` must list
  every tracked file in the skill folder — no more, no fewer — and must include
  `SKILL.md`. Adding a file to a skill folder means adding it to `files`.
- **No orphans**: every `skills/<id>/` directory needs a catalog entry and vice
  versa; ids must be unique.
- **No forbidden paths**: never commit `__pycache__/`, `.venv/`, `node_modules/`,
  `.DS_Store`, or `.env` (also enforced by `.gitignore`).
- **Schema-valid catalog**: `marketplace.json` must satisfy
  `schemas/marketplace.schema.json` (required fields, id/tag patterns, version
  `x.y.z`, `entrypoint` == `SKILL.md`).
- **Hygiene**: markdown passes markdownlint, no typos (crate-ci/typos), no secrets
  (gitleaks), LF line endings, single trailing newline, no trailing whitespace.

## Label taxonomy

Pick one or two, based on the user's workflow (not the implementation):

```text
Marketing, Sales, Legal, Operations, Engineering, Finance, Research, Content, Support, Travel
```

This set is duplicated in three places that must stay in sync:
`schemas/marketplace.schema.json` (`$defs.label`), `scripts/validate_skills.py`
(`TAXONOMY`), and `README.md` (Labels section).

## Footprint convention

The existing entries follow a consistent rule; match it:

- `source_size_bytes` = sum of the bytes of the skill's tracked files.
- `estimated_installed_size_bytes` = `source_size_bytes + 1024`.
- `estimated_runtime_cache_bytes` = 0 unless the skill downloads user-space tools
  at runtime (e.g. a `uv`-installed package), in which case estimate that download.

Use `.claude/skills/skill-authoring/scripts/footprint.py <skill-dir>` to compute
this block instead of counting bytes by hand.

## Adding or editing a skill

Prefer the meta-skills in `.claude/skills/` — they encode this workflow in detail:

1. Scaffold the folder and a valid SKILL.md skeleton
   (`skill-authoring/scripts/new_skill.py`).
2. Write the SKILL.md body and a strong `description` (triggers matter most).
3. Fill the `marketplace.json` entry; compute the footprint block.
4. Review against the quality rubric (the `skill-review` meta-skill).
5. Run the checks locally, then open a PR.

## Running the checks locally

```bash
pre-commit run --all-files          # everything CI runs
python scripts/validate_skills.py   # just the cross-file consistency checks
```

If `pre-commit` is not installed: `uv tool install pre-commit` (or pipx/brew/nix),
then `pre-commit install`.

## Meta-skills in this repo

Under `.claude/skills/` — tooling for building catalog skills, not catalog entries
themselves. They are platform-agnostic and name no specific AI model.

- **skill-authoring** — create a new marketplace skill end-to-end: scaffold, write
  the SKILL.md and description, build the catalog entry, compute footprint,
  validate. Has `references/` guides and `scripts/` helpers.
- **skill-review** — audit an existing or draft skill against the quality bar
  before a PR: runs validation, checks consistency, footprint, safety, and clarity.

## Repo conventions

- **Atomic commits by concern**: keep CI/tooling, fixes, and new skills in separate
  commits; never bundle unrelated changes.
- **Git identity**: this repo commits as `Multipixelone` (GitHub noreply email),
  not the global identity.
- **Platform naming**: catalog skills may reference Fluso as the runtime platform,
  but no skill should reference a specific AI model or vendor.
- **main is protected**: direct pushes are blocked; all changes land via PRs that
  must pass CI. Commit or push only when the user asks.

## Gotchas

- `validate_skills.py` has `always_run: true` — it runs even when your change
  touched no skill files, so a pre-existing inconsistency will still block your PR.
- After adding, renaming, or removing a file in a skill folder, update both the
  `files` list and the footprint in `marketplace.json`.
- markdownlint runs on every `.md` in the tree (including `.claude/` and this
  file): keep blank lines around headings, lists, and fenced code blocks; give
  every code fence a language; end files with a single newline.
- Long `description` lines are fine — MD013 (line length) is disabled — but the
  description is what makes a skill discoverable, so invest in it.
