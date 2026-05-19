---
name: osint-investigation
description: High-capability lawful OSINT investigation orchestration for public cyber/domain intelligence, organization reconnaissance, metadata analysis, public-code intelligence, username/profile verification, threat-intel enrichment, entity graphing, and evidence-based reports. Use when the user asks to investigate public entities, domains, organizations, public observables, documents, brand threats, public profiles, or authorized cybersecurity reconnaissance.
labels:
  - Research
  - Engineering
---

# OSINT Investigation

Run serious public-source intelligence workflows with evidence, scope control, confidence scoring, and structured reporting. Optimize for useful cybersecurity and investigation outcomes, not shallow search summaries.


## Investigation Preflight

Before running tools, classify the request:

1. **Purpose**
   - `security_research`
   - `owned_asset_recon`
   - `brand_monitoring`
   - `threat_intel`
   - `public_entity_research`
   - `profile_verification`
   - `metadata_review`
   - `consented_check`

2. **Target type**
   - `domain`
   - `organization`
   - `ip`
   - `asn`
   - `url`
   - `file`
   - `hash`
   - `public_username`
   - `public_profile`
   - `email`
   - `phone`
   - `person`

3. **Collection mode**
   - `passive`: third-party/public records only.
   - `light_active`: benign live checks such as DNS/HTTP status for owned or authorized assets.
   - `advanced_active`: broad probing or scanning. Require explicit authorization and bounded scope.

4. **Output**
   - quick summary
   - JSON evidence
   - graph
   - Markdown report
   - executive brief

Ask a concise clarification only if scope or authorization is ambiguous.

## Output Standard

Every claim should include:

- source name
- source URL or command/tool name
- observed timestamp
- confidence score
- collection mode
- limitation or caveat when relevant

Never merge weak signals into one conclusion without explaining the evidence chain.

Use these confidence defaults:

| Confidence | Meaning |
|---:|---|
| 90-100 | Deterministic primary-source result, hash-bound file metadata, authoritative API result |
| 70-89 | Corroborated by multiple independent public sources |
| 40-69 | Plausible but not independently confirmed |
| 10-39 | Weak candidate lead, not a fact |

## Evidence Schema

Use this structure for machine-readable findings:

```json
{
  "evidence_id": "ev_...",
  "target": "example.com",
  "target_type": "domain",
  "observation_type": "dns_record",
  "source": "dns",
  "source_url": null,
  "tool": "dnspython",
  "observed_at": "2026-05-19T00:00:00Z",
  "raw_value": {},
  "normalized_value": {},
  "confidence": 85,
  "collection_mode": "passive",
  "sensitivity": "low",
  "limitations": []
}
```

Use JSONL for large investigations:

- `targets.jsonl`
- `evidence.jsonl`
- `entities.jsonl`
- `relationships.jsonl`
- `report.md`

## Entity Graph Schema

Represent findings as nodes and edges.

Node types:

- `domain`
- `subdomain`
- `ip`
- `asn`
- `url`
- `certificate`
- `organization`
- `email`
- `phone`
- `username`
- `public_profile`
- `document`
- `file_hash`
- `metadata_tag`
- `software`
- `threat_indicator`
- `source`

Edge types:

- `resolves_to`
- `registered_to`
- `served_by`
- `seen_in_certificate`
- `mentions`
- `contains`
- `uses_mail_server`
- `hosted_on`
- `associated_candidate`
- `corroborated_by`
- `conflicts_with`
- `derived_from`

Keep uncertain links as `associated_candidate`, not `same_as`.

## Tool Selection

Prefer lightweight deterministic tools and APIs first. Use broad automation frameworks only when they are justified by the scope.

### Core Lightweight Tools

Use these for MVP/default workflows:

| Area | Preferred tools/APIs | Notes |
|---|---|---|
| RDAP/WHOIS | RDAP HTTP APIs, registrar RDAP endpoints | Prefer RDAP JSON over raw WHOIS parsing |
| DNS | `dnspython`, system `dig` if present | Record resolver, TTL, status |
| Certificate transparency | crt.sh-style JSON, Censys cert search if keyed | Mark as historical/passive, not live proof |
| Metadata | ExifTool | Read-only extraction; hash files first |
| Public web | search API/connectors with citations | Avoid uncited synthesis |
| Public code | GitHub/GitLab search APIs | Redact secrets; do not expose credentials |
| Threat intel | VirusTotal, AbuseIPDB, GreyNoise, URLhaus, OTX, MISP | Normalize confidence and freshness |

### Optional Advanced Tools

Use only when scope and dependencies justify them:

| Tool | Best use | Default posture |
|---|---|---|
| Amass | deep domain/attack-surface mapping | passive by default; advanced active only with authorization |
| theHarvester | public emails/subdomains/names for organizations | organization/domain scope only |
| Subfinder | passive subdomain enumeration | good optional Go binary |
| httpx | live HTTP probing | only for owned/authorized assets |
| SpiderFoot | broad multi-source OSINT automation | internal orchestrator, not default |
| Recon-ng | methodology framework | internal/reference; avoid as default runtime dependency |
| Sherlock | public username existence search | candidate leads only |
| WhatsMyName | username rule corpus | good controlled resolver data |
| Maigret | broad username/profile discovery | optional, disable proxy/Tor/bypass/recursive modes by default |
| Social Analyzer | username/profile analysis | internal only; heavier browser/OCR surface |
| PhoneInfoga | phone metadata | restricted, weak identity signal |
| GHunt | Google account OSINT | restricted/internal; avoid authenticated probing unless explicitly approved |

## Workflow: Domain / Organization Recon

Use for owned asset review, vendor assessment, brand/domain monitoring, or public cyber footprint.

1. Normalize domain and organization name.
2. Run RDAP for registration data.
3. Resolve DNS records:
   - A
   - AAAA
   - CNAME
   - MX
   - NS
   - TXT
   - SOA
   - DMARC
   - SPF
4. Query certificate transparency for candidate subdomains.
5. Deduplicate and classify subdomains:
   - certificate-observed
   - DNS-resolving
   - HTTP-live
   - historical-only
6. Enrich IPs with ASN/RDAP.
7. Optionally enrich with Shodan/Censys if API keys are available.
8. Highlight risks:
   - dangling DNS
   - expired or suspicious certificates
   - exposed admin/login surfaces
   - weak email security records
   - unexpected cloud/vendor infrastructure
9. Produce a report with evidence tables.


## Workflow: Threat Intelligence Enrichment

Use for IPs, domains, URLs, or hashes.

1. Classify observable type.
2. Validate format.
3. Query safe enrichment sources:
   - VirusTotal
   - AbuseIPDB
   - GreyNoise
   - URLhaus
   - OTX
   - MISP/OpenCTI if configured
4. Normalize:
   - detections
   - reputation
   - first seen
   - last seen
   - source count
   - provider confidence
5. Compare sources and flag conflicts.
6. Report whether the observable is:
   - benign/no known signal
   - suspicious
   - malicious
   - inconclusive

Do not upload files to third-party malware services unless the user explicitly approves sharing that file externally.

## Workflow: Public Username / Profile Verification

Use for public profile verification, impersonation review, brand monitoring, or consented/self checks.

1. Confirm the target username and purpose.
2. Run low-risk username lookup first:
   - Sherlock
   - WhatsMyName-derived checks
3. Treat each match as a candidate lead.
4. Verify candidate profiles using public page evidence:
   - profile URL
   - display name
   - bio text
   - avatar presence
   - account creation date if public
   - linked domains/usernames if public
5. Score each candidate independently.
6. Avoid declaring real-world identity unless multiple strong public signals support it and the purpose permits that conclusion.
7. Output candidates with caveats.


## Workflow: Internal Authorized Person / Profile Investigation

Use for internal authorized investigations where the requester has a legitimate case purpose and the goal is to verify public signals, identify candidate public profiles, or correlate public evidence. Keep the output framed as investigative leads with evidence, not as a guaranteed identity claim.

This workflow is intentionally stronger than a basic username search. It can combine public web, public usernames, public profiles, public code, documents, domains, emails, phone metadata, organization records, and threat-intel context when those signals are relevant to the case.

1. Record the case scope:
   - purpose
   - requester
   - target identifiers provided by the requester
   - allowed geography/platform/source boundaries
   - time window
   - output sensitivity
2. Normalize seed identifiers:
   - names and aliases
   - usernames/handles
   - public profile URLs
   - domains/websites
   - emails
   - phone numbers
   - organization names
   - document/file hashes
3. Run source-specific collection:
   - username tools for public handle existence
   - public web search for exact identifiers
   - public profile pages linked by the target or the case material
   - public code search for unique handles/domains/emails
   - domain/DNS/RDAP/CT if a website or organization is involved
   - metadata extraction for provided files
   - threat-intel enrichment for domains, IPs, URLs, and hashes
   - official/public registry sources when relevant to the case
4. Score each candidate profile independently:
   - exact identifier match
   - self-linked website/domain
   - same avatar or display name, if public
   - repeated unique phrase or bio fragment
   - public cross-link from one profile to another
   - timestamp/activity consistency
   - conflicting location/name/organization signals
5. Build a graph:
   - seed identifiers
   - public candidate profiles
   - public URLs/domains
   - public documents
   - observed emails/phones only when relevant
   - evidence source nodes
6. Produce a report with:
   - high-confidence matches
   - medium-confidence candidates
   - weak leads
   - conflicts and reasons for doubt
   - sources that failed or were rate-limited
   - recommended human verification steps

Do not output unsupported conclusions such as "this is definitely the person" unless the evidence is direct and strong. Use "candidate", "likely", "corroborated", or "unverified" precisely.

## Workflow: Email / Phone Signal Review

Use only for authorized, consented, or organization-owned contexts.

For email:

1. Validate syntax and domain.
2. Check domain MX and deliverability signals without sending mail.
3. Check public breach/reputation APIs only when terms permit and output does not expose secrets.
4. Search public web/code references only within the stated scope.
5. Report presence signals, not account ownership conclusions.

For phone:

1. Normalize to E.164.
2. Identify country/region/carrier where public and lawful.
3. Check public reputation/spam indicators if configured.
4. Treat all ownership claims as weak unless confirmed by user-provided evidence.

## High-Capability People/Identity Source Strategy

For authorized internal work, prioritize sources that produce inspectable public evidence:

| Source type | Use | Output posture |
|---|---|---|
| Public profile pages | Candidate profile discovery and verification | Lead with URL and confidence |
| Public web search | Exact identifier references and cross-links | Cite every result |
| Username tools | Broad handle existence search | Candidate only, high false-positive caution |
| Public code search | Handles, domains, emails, package references | Redact secrets; cite repo/file path |
| Public documents | Metadata, embedded author/software/path signals | Hash-bound evidence |
| Domain/DNS/RDAP/CT | Website and organization links | Strong for domains, weak for people unless self-linked |
| Threat intel APIs | Malicious domains/IPs/hashes connected to case material | Observable reputation only |
| Official registries | Public organization/corporate context | Use primary source links |

Prefer direct public cross-links over fuzzy matching. A profile that links to another profile is stronger than a shared display name. An exact unique handle is stronger than a common real name. Metadata from a user-provided file is stronger than web-search snippets.

Avoid turning weak correlation into identity resolution. Preserve uncertainty.

## Workflow: Metadata / Document Intelligence

Use for uploaded files, user-provided files, or explicitly authorized public documents.

1. Hash every artifact before extraction.
2. Record:
   - file path or URL
   - size
   - MIME/type guess
   - SHA-256
   - collection timestamp
3. Extract metadata with ExifTool when available.
4. Normalize:
   - author/creator fields
   - software/tooling
   - timestamps
   - device/camera
   - GPS/location tags
   - embedded URLs/domains
   - document paths/usernames
5. Mark sensitive metadata such as GPS or personal names.
6. Build graph edges from artifacts to metadata entities.
7. Produce `report.md` and JSONL evidence.

Do not crawl a website for documents unless the user has scoped the domain and authorization.

## Workflow: Public Code Intelligence

Use for organization/domain exposure review, brand monitoring, and public reference discovery.

1. Scope the organization, domain, package names, or unique identifiers.
2. Query public code hosts:
   - GitHub
   - GitLab
   - package registries
3. Search for:
   - domains
   - subdomains
   - package names
   - public config references
   - exposed endpoints
   - leaked brand references
4. Redact secrets by default.
5. Report repository URL, file path, line context, timestamp, and confidence.

Do not print full credentials, private keys, or tokens. Report that a likely secret was found and provide enough location context for remediation.

## Workflow: Entity Graph Build

After collecting evidence:

1. Create one node per normalized entity.
2. Attach raw evidence to the node.
3. Add edges only when the relationship is supported by evidence.
4. Keep conflicting observations rather than overwriting.
5. Merge entities only when canonical identifiers match.
6. Use `associated_candidate` for weak username/person/profile relationships.
7. Export:
   - graph JSON
   - evidence JSONL
   - report Markdown

## Report Format

Use this structure:

```markdown
# OSINT Report: <target>

## Scope
- Target:
- Purpose:
- Collection mode:
- Time window:
- Tools/sources:

## Executive Summary
- Key finding 1
- Key finding 2
- Key limitation

## Findings
| Finding | Confidence | Evidence | Risk/Meaning |
|---|---:|---|---|

## Entity Graph Summary
- Nodes:
- Important relationships:
- Candidate links:
- Conflicts:

## Evidence
| ID | Source | Observation | Timestamp | Confidence |
|---|---|---|---|---:|

## Limitations
- Source coverage gaps
- API limits
- Historical/passive data caveats
- Unverified candidate links

## Recommended Next Steps
- Verification steps
- Remediation steps
- Monitoring suggestions
```

## Failure Handling

Handle failures explicitly:

- API key missing: continue with free/passive sources and list missing enrichment.
- Rate limited: stop that provider, cache partial results, and record the limitation.
- Tool missing: use a lighter fallback or produce a tool requirement note.
- Conflicting results: include both and reduce confidence.
- No results: report no public signal found, not proof of absence.

## Local Capability Test Plan

Good test targets:

- A consenting team member's public handles.
- A company-owned test domain.
- A deliberately created synthetic profile set.
- Public demo documents created for metadata testing.
- Known benign test observables such as reserved domains and documentation IPs.

Test scenarios:

1. **Domain investigation**
   - Input: company-owned domain.
   - Expected: RDAP/DNS/CT evidence, subdomain candidates, email security records, report.

2. **Public username footprint**
   - Input: synthetic username used on 3-5 public test profiles.
   - Expected: candidate profile list with confidence and source URLs.

3. **Profile correlation**
   - Input: one public profile URL and one known linked handle.
   - Expected: graph with direct cross-link evidence and no unsupported claims.

4. **Document metadata**
   - Input: test PDF/image/docx with known metadata.
   - Expected: SHA-256, extracted tags, sensitive metadata flags, report.

5. **Threat-intel enrichment**
   - Input: known benign domain/IP and known test malware hash from provider docs if allowed.
   - Expected: provider-attributed result with confidence and limits.

Quality checks:

- Every finding has a source.
- Candidate identity links are not presented as confirmed without direct evidence.
- Missing API keys degrade gracefully.
- Rate limits are recorded.
- Reports include limitations.

## Runtime And Dependency Guidance

Keep the base skill lightweight. Prefer Python scripts with declared dependencies only when implementation is needed.

Good default dependencies for future scripts:

- `httpx`
- `dnspython`
- `pydantic`
- `python-whois` only as fallback; prefer RDAP HTTP

Optional external binaries:

- ExifTool for metadata
- Amass/Subfinder/httpx for advanced domain recon

Do not require Chromium, Docker, sudo, apt, Tor, or browser automation for the default skill.
