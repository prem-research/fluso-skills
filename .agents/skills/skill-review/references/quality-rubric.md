# Skill quality rubric

The pass/fail questions for reviewing a marketplace skill. Structural items are
also enforced by tooling; the judgment items are yours to make.

## Blockers (must fix — these fail CI or are unsafe)

- **Identity mismatch** — SKILL.md `name`, folder name, and catalog `id` are not
  the same kebab-case string.
- **Label ↔ category mismatch** — SKILL.md `labels` do not equal
  `marketplace.json` `categories`, are not 1–2 items, or include a value outside
  the taxonomy.
- **Files manifest drift** — `files` omits a tracked file, lists a missing file,
  or omits `SKILL.md`.
- **Missing dependency file** — a recipe references a `pyproject.toml` /
  `package.json` that is absent or unlisted.
- **Forbidden content** — `__pycache__/`, `.venv/`, `node_modules/`, `.DS_Store`,
  `.env`, secrets, or large generated artifacts are tracked.
- **Unsafe setup** — the skill requires `sudo`, `apt`, Docker, or root, or mutates
  system packages instead of staying in user space.
- **Schema violation** — a missing required field, bad version string, wrong
  `entrypoint`, or malformed id/tag.

## Description (judgment — the highest-value check)

Ask, in order:

1. Does it state **what the skill does** in the third person?
2. Does it name **concrete trigger conditions** — the file types, nouns, verbs,
   and synonyms a user would actually type — not just a topic?
3. Would it **fire for the right requests**? Imagine three realistic user
   messages that should trigger it; does the description cover them?
4. Would it **stay quiet for the wrong ones**? Imagine an adjacent request that
   should not trigger it; is the boundary clear?
5. Is it **distinct from neighboring skills** so the right one wins when two could
   match?
6. Is it free of any specific AI model or vendor name?

A description that fails 2, 3, or 4 is a quality blocker even though no validator
will flag it — the skill will misfire in practice.

## Body (judgment)

- **Purpose** — one line stating the job and the outcome.
- **Workflow** — an explicit, ordered set of steps that a reader could follow
  without guessing.
- **Rules** — the non-negotiables and safety limits are stated.
- **Output** — the deliverable's shape is defined (a template or schema where it
  helps).
- **Failure handling** — what to do when a tool, key, or input is missing.
- **Quality check** — a short self-verification list before finishing.
- **Progressive disclosure** — rarely-needed detail lives in `references/`, not
  inline; the common path is easy to reach.
- **Defaults** — the assistant is given defaults rather than forced to guess.
- **Honest claims** — best-effort results (searches, lookups, generations) are
  presented with confidence and caveats, not as guaranteed facts.

## Dependencies and footprint (judgment + tooling)

- Instruction-only where possible; dependencies added only when a real workflow
  needs them.
- `tier`, `recipes`, and `system_capabilities` describe what the skill actually
  uses.
- Setup stays in user space and explains what it downloads.
- `footprint` recomputed and matches: source = folder bytes, installed = source +
  1024, runtime cache = 0 unless the skill downloads tools at runtime.

## Safety flags (judgment)

- `has_helper_scripts` true exactly when the folder has a `scripts/`.
- `runs_install_script` true exactly when using the skill runs a setup step.
- `network_at_runtime` true exactly when the workflow makes network calls.

## Neutrality and self-containment

- No specific AI model or vendor is named; the actor is "the assistant" or "the
  agent" and the platform is referred to generically.
- A reviewer can understand the skill without outside context.
- Every shipped file is used or referenced by the body; there are no silent files.

## Verdict

- **Ship** — no blockers, description passes the trigger test, body has a workflow
  and a quality bar.
- **Revise** — no blockers but the description or body needs work; list concrete
  fixes.
- **Reject** — one or more blockers; list them with fixes.
