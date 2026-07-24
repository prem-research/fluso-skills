# Acme Corp Information Security Policy v3.1

Illustrative internal policy excerpt used by the security-questionnaire skill's
worked example. It stands in for the kind of source document the skill answers
from. Every answer in `completed-questionnaire.csv` cites a section below.

## 2. Access Control

All administrative and remote access to production systems requires
multi-factor authentication (MFA). User access rights are reviewed quarterly by
system owners, and access is revoked within 24 hours of an employee's
termination.

## 4. Data Protection

All data transmitted over public networks is encrypted in transit using
TLS 1.2 or higher. Customer data at rest is encrypted using AES-256.

## 5. Incident Response

Acme maintains a documented incident response plan, reviewed annually, with
defined roles, severity levels, and escalation paths.

## 6. Vulnerability Management

Automated vulnerability scans of production infrastructure are performed
weekly. Critical findings are remediated within 30 days.

## 7. Business Continuity

Disaster recovery procedures are documented and tested. Formal recovery time
objectives (RTO) and recovery point objectives (RPO) are still being defined
and are targeted for the next policy revision.
