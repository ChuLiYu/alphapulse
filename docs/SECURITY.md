# Security boundaries

Status: required controls for the target architecture, plus the existing selected security baseline. [Existing agent review](agents/SECURITY_REVIEW.md) and [security remediation evidence](local/SECURITY_REMEDIATION.zh-TW.md) retain their original limits.

Financial correctness, access control and audit integrity are release properties. Portfolio records require server-side portfolio grants as well as action permissions. A user cannot approve their own proposal. Token role changes/revocation must affect subsequent actions. The existing JWT/global permission implementation does not yet satisfy the portfolio-scoped OIDC target.

Secrets stay in ignored local settings or a deployment secret manager. Redact tokens, credentials, client data and model source content from logs. Public synthetic examples must be reviewed before publishing. Do not initialize the private submodule or copy personal AI account settings into this repository.

AI tool access is read-only and authorized before retrieval; imported documents are untrusted content. [AI governance](ai/governance.md) owns the detailed controls and evaluation. New investment endpoints must fail closed on missing financial evidence and never rely on the legacy frontend's demo response interceptor.

Cloud deployment, namespace migration and new image publishing require the environment's normal release gate. The rename changes source configuration; it does not certify historical k3s/Terraform settings or transfer existing GHCR packages. [Operations](engineering/operations.md) owns rollout/recovery evidence.

Report a suspected vulnerability privately to the repository maintainer using a private channel supported by the repository; do not post secrets or exploit data in a public issue. No security accreditation is claimed.
