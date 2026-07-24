---
name: security-questionnaire
description: Complete a vendor security questionnaire from the organization's own policy documents and past questionnaires. Answers only from cited internal sources; flags anything unanswerable for human review instead of guessing. Use when a customer or prospect sends a security assessment, CAIQ/SIG-style spreadsheet, or due-diligence questionnaire to fill in.
labels:
  - Legal
  - Operations
---

# Security questionnaire skill

Complete an inbound vendor security questionnaire using only the organization's own documentation. Every answer must cite its source. Never invent a control, a certification, or a number.

A wrong answer on a security questionnaire is worse than a flagged one: it can become a contractual representation. When in doubt, flag it.

## Inputs

1. **The questionnaire** — a spreadsheet with one row per question (any reasonable column layout; detect Ref / Domain / Question / Response / Detail / Evidence columns by header). Common formats and how to recognize them are in `references/questionnaire-formats.md`.
2. **Internal policy documents** — the organization's security, access control, data protection, and related policies.
3. **Past completed questionnaires** — previously answered assessments, used as reference material for phrasing and precedent, never as a substitute for a current policy citation when one exists.

If the user has not provided policy documents, ask for them before answering. This skill cannot answer from general knowledge.

## The helper tool

`scripts/questionnaire.py` handles the spreadsheet I/O deterministically so you never rebuild the sheet by hand and never disturb its formatting. It does the mechanical work only — it does not decide answers. It runs entirely locally with no network access.

Read a questionnaire into clean JSON rows:

```bash
uv run --project /fluso/user/workspace/skills/security-questionnaire \
  python scripts/questionnaire.py extract questionnaire.xlsx --out rows.json
```

`extract` auto-detects the header row and column mapping and reports any answer column it could not find. If it maps the wrong header, add `--header-row N` (1-based) or `--sheet NAME` after the file, for example `... extract questionnaire.xlsx --header-row 3`.

After you have decided each answer from the sources, write them back into a formatting-preserving copy:

```bash
uv run --project /fluso/user/workspace/skills/security-questionnaire \
  python scripts/questionnaire.py fill questionnaire.xlsx answers.json --out questionnaire-completed.xlsx
```

`answers.json` is a list, one object per row, matched by `row` (from `extract`) or by `ref`:

```json
{
  "answers": [
    {"row": 2, "response": "Yes", "detail": "...", "evidence": "InfoSec Policy v3.1 §2", "status": "Complete"},
    {"row": 3, "status": "Needs review"}
  ]
}
```

`fill` only touches the response, detail, evidence, and status columns of the rows you name. It leaves every other cell, column width, and style untouched, and writes to a copy so the original is never overwritten. If `uv` is unavailable or dependencies are not prepared, say so plainly rather than editing the spreadsheet by hand. Both `.xlsx` and `.csv` are supported.

`assets/example/` is a complete worked run — sample questionnaire, source policy, the `answers.json` in between, the completed sheet, and the evidence appendix.

## Method

1. Read every row of the questionnaire first. Run `extract` and build the full list before answering anything.
2. Index the policy documents by section. Note document name, version, and section numbers; citations use the form `Document name vX.Y §N`.
3. For each question, answer **only** if a policy section or past-questionnaire answer substantively covers it. The decision rules — how to pick Yes / No / Partial / N/A, how to word the detail, and what must always be flagged — are in `references/answering-rules.md`. In brief:
   - **Response:** Yes / No / Partial / N/A, chosen conservatively. If the source says a capability is planned or on a roadmap, the response is No or Partial, stated plainly.
   - **Response detail:** one to three sentences in plain, professional language, restating what the source actually says. No marketing language, no adjectives the source does not support.
   - **Evidence / source:** the citation. If a past questionnaire informed the phrasing, cite both the policy and the past questionnaire.
4. If no source covers the question, or the question asks for facts outside the documents (insurance limits, breach history, legal positions, certifications not evidenced, customer-specific commitments), set **Status = Needs review** and leave the response blank.
5. Fill the Status column: `Complete` for answered rows, `Needs review` for flagged rows. Run `fill` to write everything back at once.
6. Produce a short **evidence appendix** (one page) using `assets/evidence-appendix-template.md`: the list of source documents used with versions, the count of rows answered per source, and the full list of flagged rows with one line each on what a human needs to supply.
7. Report the totals: rows answered with citations, rows flagged, sources used, and elapsed time.

## Reusing prior answers

To make repeat questionnaires faster, keep vetted answers in an answer library under the workspace, for example `security-questionnaires/answer-library.md`, keyed by control topic with the approved wording and its citation. When a new questionnaire arrives, reuse a library answer only after confirming the cited policy section still exists and still says what the answer claims. A stale citation is treated as no source: re-verify or flag. The library is a shortcut for phrasing, never a bypass of the citation rule.

## Rules

- Answer from the documents, not from general knowledge of what companies usually do.
- One conservative answer beats one optimistic answer, every time.
- Questions about legal exposure, insurance, past incidents, or anything reputational are always flagged for a human, even when a document appears to cover them.
- Keep the requester's column layout and formatting intact. Fill cells; do not restructure the sheet. The `fill` command enforces this.
- If two sources conflict, flag the row and name both sources in the appendix.
- Never send questionnaire contents, policies, or answers to an external service. The whole workflow runs on local documents.
