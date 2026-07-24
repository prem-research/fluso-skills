# Recognizing questionnaire formats

Most inbound assessments are one of a few standard frameworks or a custom sheet
built in their style. Recognizing the format tells you where the question text
lives, which column expects the answer, and how the response is scored. Use
`extract` to detect columns automatically; use this reference when a header is
ambiguous or you need `--header-row` / `--sheet` to point the tool correctly.

## Column detection

`extract` maps each column to a field by matching the header text. It handles
common synonyms:

| Field | Header text it recognizes |
| --- | --- |
| `ref` | Ref, ID, No, Item, Control ID, Question ID, QID |
| `domain` | Domain, Category, Section, Control Family, Principle, Topic |
| `question` | Question, Control, Requirement, Description, Control Specification |
| `response` | Response, Answer, Yes/No, Compliant, Vendor Response |
| `detail` | Detail, Comment, Notes, Explanation, Justification, Response Detail |
| `evidence` | Evidence, Reference, Source, Citation, Supporting Documentation, Attachment |
| `status` | Status, Review Status, State, Disposition |

A bare **Reference** column is treated as evidence, since assessments use
**Ref** or **Control ID** for the identifier. If a sheet genuinely uses
"Reference" as its ID column, confirm the mapping in the `extract` output and
override with `--header-row` if needed.

If `extract` reports a field in `unmapped_answer_fields`, the sheet has no
column for it. Do not invent one — `fill` will skip it and warn.

## Common frameworks

### CAIQ (CSA Consensus Assessments Initiative Questionnaire)

Cloud Security Alliance's standard, aligned to the Cloud Controls Matrix (CCM).
Questions are grouped by control domain (e.g. IAM, DSP, AIS) with a Control ID
per row. The answer is usually a **Yes / No / NA** column plus a free-text
notes column. Multiple tabs are common — the questionnaire is often not on the
first sheet, so check `--sheet`.

### SIG and SIG Lite (Shared Assessments)

The Standardized Information Gathering questionnaire. SIG Core is very large
(hundreds to thousands of questions across ~20 risk domains); SIG Lite is a
condensed subset. Answers are typically **Yes / No / N/A** with a comments
column. Because SIG is large, batch by domain and lean on the answer library.

### VSAQ (Google Vendor Security Assessment Questionnaire)

Google's open-sourced Vendor Security Assessment Questionnaire — an interactive,
form-style questionnaire that adapts follow-up questions to earlier answers.
When exported to a sheet it is compact: a question and a free-text or yes/no
response per row.

### VSA (Vendor Security Alliance)

The Vendor Security Alliance publishes its own annual questionnaire in Core and
Full editions. It is a structured spreadsheet grouped by control area, with a
yes/no or compliance response and a comments column per row.

### HECVAT (Higher Education Community Vendor Assessment Toolkit)

Used in higher education. Comes in Full and Lite variants. Rows carry a
question, a **Yes / No / N/A** answer, and a dedicated column for additional
information; a separate tab often lists standards and references.

### Custom and buyer-specific sheets

Many enterprises ship their own spreadsheet. They still follow the same shape:
an identifier, a question, an answer cell, a comments cell, and sometimes an
evidence cell. `extract` handles these the same way. Watch for merged header
cells, a title/branding row above the header (auto-detection skips it), and
instructions on a separate tab.

## Scoring and response conventions

- **Yes / No / N/A** is the most common answer set. Some sheets add **Partial**
  or a maturity scale (e.g. Not Implemented / Planned / Implemented). Map a
  roadmap or planned control to **No** or **Partial**, never to **Yes**.
- Some frameworks expect a compliance level (Fully / Partially / Not) rather
  than yes/no. Choose the level the source actually supports and explain it in
  the detail column.
- A few sheets separate "Response" from a required "Evidence/Attachment"
  column. Put the citation in the evidence column; do not paste document
  contents into the sheet.
