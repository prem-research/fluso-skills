# Writing a SKILL.md

A SKILL.md has two parts that carry almost all of the value: the `description`
in the frontmatter (decides whether the skill triggers) and the body (decides
whether the output is good). This guide covers both, plus the frontmatter
mechanics.

## Frontmatter

Required keys for this repository:

```yaml
---
name: contract-review
description: <one paragraph — see below>
labels:
  - Legal
---
```

- `name` — kebab-case, identical to the folder name and the `marketplace.json`
  `id`.
- `description` — the trigger sentence(s). See the next section.
- `labels` — 1 or 2 items from the taxonomy, equal to the catalog `categories`.

The file must start with the `---` fence on line 1. The body follows the closing
`---`.

## Descriptions: the trigger sentence

The description is how the platform decides whether to load this skill for a
given user message. A vague description means the skill never fires or fires at
the wrong time. Treat it as the single most important line in the skill.

Write it in **two moves**:

1. **What it does** — a plain statement of the capability, in the third person.
2. **When to use it** — an explicit "Use when …" clause that names concrete
   trigger conditions and the words a user would actually type.

Good:

```text
description: Review contracts for risky clauses and obligations and produce a
  redline summary. Use when the user shares a contract, MSA, NDA, SOW, or lease
  and asks to review it, find risks, check terms, or compare against a standard.
```

Weak (topic only, no triggers — will misfire):

```text
description: Helps with contracts.
```

Guidelines:

- Third person ("Review …", "Guides the assistant through …"), never "I" or "you".
- Lead with the capability, then the triggers. Both matter.
- Name the concrete nouns and verbs a user says: file types, synonyms, actions.
- Distinguish it from neighboring skills so the right one wins. If two skills
  could both match, say what is in scope and what is not.
- Do not name a specific AI model or vendor.
- Length is not limited (MD013 is off), but every clause should add a trigger or
  a boundary, not filler.

## Body: structure

The body is the instruction set the assistant follows once the skill is loaded.
Use a predictable shape so it is easy to follow under load:

1. **One-line purpose** — restate the job and the outcome.
2. **When to use / preflight** — any classification or clarifying questions to
   ask before acting (scope, inputs, authorization).
3. **Workflow** — an explicit, ordered set of steps. This is the spine.
4. **Rules / constraints** — the non-negotiables and safety limits.
5. **Output format** — the shape of the deliverable (a template or schema helps).
6. **Failure handling** — what to do when a tool, key, or input is missing.
7. **Quality check** — a short checklist to verify before finishing.

Not every skill needs every section, but every skill needs a workflow and a
quality bar.

## Body: progressive disclosure

Keep the SKILL.md focused on what is needed most of the time. Move long,
optional, or rarely-needed material into `references/` and link to it. The body
should fit comfortably in working memory; a reader should not scroll past detail
they rarely need to reach the common path.

- Frequently needed → in `SKILL.md`.
- Deep tables, schemas, exhaustive option lists, edge-case playbooks →
  `references/<topic>.md`, referenced by name from the body.
- Deterministic multi-step logic → a reviewed script in `scripts/`, invoked by
  the body rather than described step-by-step in prose.

## Body: tone and precision

- Write imperative, concrete instructions ("Run RDAP for registration data"),
  not vague advice ("consider looking at registration").
- Prefer numbered steps for anything sequential; bullets for unordered rules.
- Give defaults so the assistant is not forced to guess (e.g. a default output
  folder, a default confidence score, a default cabin class to ask about).
- State boundaries explicitly: what the skill must not do, and when to stop and
  ask.
- Use tables for structured reference (option → meaning, tier → posture).

## Anti-patterns

- **Topic-only description** — no trigger conditions, so it never fires reliably.
- **Kitchen-sink skill** — two or more unrelated jobs in one skill; split them.
- **Everything inline** — a giant body that buries the common path; use
  `references/`.
- **Unlabeled expectations** — assuming inputs or tools exist without a preflight
  check or a failure path.
- **Model or vendor references** — naming a specific AI model; keep it agnostic.
- **Silent files** — shipping a script or asset the body never mentions; either
  use it from the body or remove it.
- **Guaranteed claims** — presenting best-effort results (searches, lookups) as
  confirmed facts; state confidence and caveats.

## Minimal example

```markdown
---
name: contract-review
description: Review contracts for risky clauses and obligations and produce a
  redline summary. Use when the user shares a contract, MSA, NDA, SOW, or lease
  and asks to review it, find risks, check terms, or compare against a standard.
labels:
  - Legal
---

# Contract Review

Turn a contract into a prioritized risk summary with suggested redlines.

## Preflight

Confirm the contract type, the user's side of the deal, and any standard or
playbook to compare against. Ask only if these are unclear.

## Workflow

1. Read the document and identify the parties, term, and governing law.
2. Extract obligations, liabilities, termination, IP, and payment clauses.
3. Flag risky, missing, or non-standard terms with severity.
4. Produce a redline summary table and a plain-language recommendation.

## Output

A `risk-summary.md` with a severity table and a short recommendation. Separate
findings from advice. Note anything that needs a lawyer's judgment.

## Quality check

- Every flagged clause cites the section it came from.
- Severity is justified, not asserted.
- The summary is usable without re-reading the full contract.
```
