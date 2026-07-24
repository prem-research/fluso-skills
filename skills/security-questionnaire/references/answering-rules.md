# Answering rules

The controlling principle: **every answer is traceable to a cited internal
source, and anything else is flagged.** These rules make that principle
operational. When two rules seem to conflict, choose the more conservative
outcome.

## Choosing the response value

Pick the value the source actually supports, reading conservatively.

- **Yes** — a policy section states the control is in place today, without
  qualification. Cite the section.
- **No** — the source says the control is absent, or describes it as planned,
  in progress, or on a roadmap. Planned is not Yes. State it plainly.
- **Partial** — the control exists for some systems, environments, or cases but
  not universally, and the source says so. Name the boundary in the detail.
  If the sheet has no Partial option, use No and explain the limitation.
- **N/A** — the control genuinely does not apply to the organization's model
  (for example, a question about a payment card environment when none exists).
  Only mark N/A when a source supports the reason; otherwise flag it.

If the source is silent, the answer is not No — it is **Needs review**. No
means "the source says we do not"; Needs review means "no source addresses
this." Keep them distinct.

## Writing the detail

- One to three sentences, plain and professional. Restate what the source says.
- No marketing language, no superlatives, no adjectives the source does not
  support ("robust", "military-grade", "industry-leading" are all banned unless
  they are literally quoting the policy).
- Do not add scope the source lacks. If the policy says "production systems,"
  do not generalize to "all systems."
- Do not paste document contents or secrets into the sheet. Summarize and cite.

## Writing the citation

- Format: `Document name vX.Y §N` — e.g. `InfoSec Policy v3.1 §4.2`.
- Cite the most specific section that supports the answer.
- If a past questionnaire supplied the phrasing, cite both the policy and the
  past questionnaire, so a reviewer can see the precedent and the source.
- If the only support is a past questionnaire with no current policy behind it,
  treat the claim as unverified and flag the row.

## Always flag these

Set **Status = Needs review** and leave the response blank, even if a document
appears to touch the topic:

- Insurance coverage and limits.
- Breach, incident, or litigation history.
- Legal positions, indemnities, liability, and contractual commitments.
- Certifications or attestations (SOC 2, ISO 27001, PCI DSS, HIPAA) unless a
  current attestation document is in the provided sources — a policy mentioning
  a certification is not evidence the certification is held.
- Customer-specific commitments, SLAs, or exceptions.
- Anything reputational, or anything a wrong answer would expose the
  organization to.

## Conflicts and ambiguity

- If two sources conflict, flag the row and name both sources in the appendix.
  Do not silently pick one.
- If a source is outdated relative to another, prefer the current one but still
  flag if the difference is material.
- If a question bundles several asks ("Do you encrypt data at rest and in
  transit, and rotate keys annually?"), answer only the parts the source
  covers, and flag the row if any part is unsupported.

## Never

- Never infer a control from what similar companies usually do.
- Never upgrade a planned or partial control to Yes to look better.
- Never fabricate a document name, version, or section number to satisfy the
  evidence column. An empty evidence cell with a Needs review status is correct
  when there is no source.
