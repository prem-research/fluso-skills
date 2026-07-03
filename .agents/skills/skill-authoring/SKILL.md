---
name: skill-authoring
description: Author a new marketplace skill end-to-end for this repository — scaffold the folder, write a strong SKILL.md and description, build the marketplace.json entry, compute the footprint, and validate. Use when creating a new skill, splitting a large skill, or turning a workflow into an installable skill package.
---

# Skill Authoring

Use this skill to create a new marketplace skill in this repository so it is
correct, discoverable, and passes CI on the first try. It covers the whole path:
scaffold, write, catalog, validate.

Two things decide whether a skill succeeds: whether it **triggers** at the right
time (the `description`) and whether its **instructions** produce good output
(the body). Spend your effort there; the rest is mechanical consistency the
tooling can check for you.

## When to use

- Creating a brand-new skill from a described workflow.
- Splitting one overloaded skill into focused skills.
- Converting an ad-hoc process into an installable, reviewable package.

For auditing an existing or draft skill, use the companion `skill-review` skill.

## Workflow

1. **Clarify the job.** Name the single task the skill owns, who triggers it, the
   inputs it needs, and the output it produces. If it owns more than one
   unrelated task, make two skills. A skill should be describable in one sentence.

2. **Choose the identity.** Pick a kebab-case `id` (e.g. `contract-review`). This
   one string is the folder name, the frontmatter `name`, and the catalog `id` —
   they must be identical. Pick 1–2 `labels` from the taxonomy (see
   `references/marketplace-entry.md`); labels describe the user's workflow, not
   the implementation.

3. **Scaffold.** Run the helper to create the folder and a valid SKILL.md
   skeleton:

   ```bash
   python .claude/skills/skill-authoring/scripts/new_skill.py \
     --id contract-review \
     --display-name "Contract Review" \
     --labels Legal \
     --summary "Review contracts for risky clauses and produce a redline summary."
   ```

   It refuses to overwrite an existing skill and prints a ready-to-paste
   `marketplace.json` entry plus the next steps.

4. **Write the description.** This is the highest-leverage sentence in the skill.
   Follow `references/skill-md-guide.md` (Descriptions section): third person,
   state what the skill does, then an explicit "Use when …" clause listing the
   trigger conditions and the words a user would actually say.

5. **Write the body.** Give the assistant a concrete, ordered workflow, the rules
   and quality bar, and the failure handling. Keep the frequently-needed content
   in `SKILL.md`; push long or rarely-needed detail into `references/`. See
   `references/skill-md-guide.md` (Body section) for structure and anti-patterns.

6. **Add supporting files only if they earn their place.** `scripts/` for
   deterministic reviewed helpers, `references/` for deep docs the body links to,
   `assets/` for templates or samples. Every file you add must be listed in the
   catalog `files` array.

7. **Build the catalog entry.** Fill the `marketplace.json` entry using
   `references/marketplace-entry.md`. Set `categories` equal to the SKILL.md
   `labels`. List every tracked file in `files`. Declare dependencies and safety
   honestly.

8. **Compute the footprint.** Run the helper on the finished folder and paste the
   block it prints:

   ```bash
   python .claude/skills/skill-authoring/scripts/footprint.py skills/contract-review
   ```

9. **Validate.** Run the repo checks and fix anything they report:

   ```bash
   python scripts/validate_skills.py
   pre-commit run --all-files
   ```

10. **Review.** Run the `skill-review` skill against the finished skill before
    opening the PR.

## Rules

- Keep the skill self-contained: a reviewer should understand it without outside
  context.
- Prefer instruction-only skills. Add dependencies only when a real workflow
  needs them, and keep any setup in user space (no `sudo`, `apt`, Docker, root).
- Never bundle `node_modules/`, `.venv/`, `__pycache__/`, generated caches, build
  artifacts, or secrets.
- Write platform-agnostically: do not name a specific AI model or vendor. Refer
  to "the assistant" or "the agent" and to the runtime platform generically.
- Keep the `files` array and the footprint in sync with the folder every time you
  add or remove a file.

## Reference files

- `references/skill-md-guide.md` — how to write the description and the body:
  triggers, progressive disclosure, structure, tone, and anti-patterns.
- `references/marketplace-entry.md` — the `marketplace.json` entry field by field:
  labels/categories, tags, files manifest, footprint, dependencies, safety.

## Scripts

- `scripts/new_skill.py` — scaffold a skill folder and a valid SKILL.md skeleton;
  prints a catalog entry template. Standard-library Python, no dependencies.
- `scripts/footprint.py` — compute the `footprint` block for a skill folder using
  the repo's `installed = source + 1024` convention.

## Quality check

Before handing off, confirm:

- `name`, folder, and catalog `id` are the identical string.
- `labels` equal `categories`, are 1–2 items, and are all in the taxonomy.
- `files` lists exactly the tracked files in the folder and includes `SKILL.md`.
- The description names concrete trigger conditions, not just a topic.
- The body gives an ordered workflow and a quality bar, and links to any
  `references/` instead of inlining rarely-needed detail.
- `python scripts/validate_skills.py` and `pre-commit run --all-files` pass.
