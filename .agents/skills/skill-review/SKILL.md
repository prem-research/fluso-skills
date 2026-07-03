---
name: skill-review
description: Audit a new or draft marketplace skill against this repository's quality bar before opening a PR — checks identity and label consistency, the files manifest, footprint, dependencies, safety, description strength, and body clarity. Use when reviewing a skill someone wrote, self-reviewing before a PR, or diagnosing why validation or CI fails for a skill.
---

# Skill Review

Use this skill to review a marketplace skill before it ships: catch the
consistency errors that fail CI, and judge the qualities a validator cannot —
whether the description triggers correctly and the body is actually usable.

Run this against your own drafts before opening a PR, or against a contributor's
skill during review. To create a skill from scratch, use the `skill-authoring`
skill first.

## Workflow

1. **Run the mechanical checks.** Let the repo's tooling find structural
   problems first:

   ```bash
   python scripts/validate_skills.py
   pre-commit run --all-files
   ```

   Fix everything they report before spending time on judgment calls — a failing
   validator blocks the PR regardless of how good the prose is.

2. **Verify identity and labels by hand.** Confirm the SKILL.md `name`, the
   folder name, and the `marketplace.json` `id` are the identical string, and
   that `labels` equals `categories` (1–2 items, all from the taxonomy).

3. **Verify the files manifest.** Confirm `files` lists every tracked file in the
   folder and nothing that is absent, and that it includes `SKILL.md`. Confirm any
   `pyproject.toml` or `package.json` a dependency recipe references is present
   and listed.

4. **Verify the footprint.** Recompute it and compare:

   ```bash
   python .claude/skills/skill-authoring/scripts/footprint.py skills/<id>
   ```

   `source_size_bytes` should match the folder; installed should be source +
   1024; runtime cache should be 0 unless the skill downloads tools at runtime.

5. **Judge the description.** This is where skills most often fail silently. Ask:
   does it state what the skill does *and* name concrete trigger conditions and
   the words a user would type? Would it fire for the right requests and stay
   quiet for the wrong ones? Is it distinct from neighboring skills? See the
   rubric for the full test.

6. **Judge the body.** Is there an ordered workflow, clear rules, an output
   format, failure handling, and a quality check? Is rarely-needed detail pushed
   into `references/` rather than bloating the body? Are there defaults so the
   assistant is not left guessing?

7. **Check safety and honesty.** Are the `safety` booleans accurate? Does the
   skill avoid `sudo`/`apt`/Docker/root and keep setup in user space? Does it
   avoid presenting best-effort results as guaranteed facts? Does it name no
   specific AI model or vendor?

8. **Report findings.** Group them: blockers (fail CI or are unsafe), quality
   issues (weak description, unclear body), and nits. For each, give the file,
   the problem, and a concrete fix.

## What to rely on the tooling for vs. judge yourself

- `validate_skills.py` catches: id/name/folder mismatch, label ↔ category
  mismatch, out-of-taxonomy labels, files-manifest drift, orphans, duplicate ids,
  forbidden paths.
- The JSON Schema catches: missing fields, bad id/tag patterns, bad version,
  wrong `entrypoint`.
- markdownlint / typos / gitleaks catch: formatting, spelling, secrets.
- **You** must judge: description trigger quality, body clarity and completeness,
  correct labels, honest safety flags, sensible dependencies, and platform/model
  neutrality. The rubric in `references/quality-rubric.md` is the checklist.

## Reference

- `references/quality-rubric.md` — the full pass/fail rubric with the specific
  questions to ask about the description, the body, dependencies, and safety.

## Output

A short review with three buckets — **blockers**, **quality**, **nits** — each
item naming the file, the problem, and the fix. If the skill is clean, say so and
confirm which checks passed.
