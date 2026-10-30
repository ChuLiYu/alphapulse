# Operating model and release evidence

Status: target operating requirements; no new cloud environment has been deployed.

## Identity migration

The public repository and local directory are `alphapulse`. Git remote and active clone/image settings use the new name. Python namespace, database `alphapulse`, Kubernetes namespace `alphapulse`, CLI `./alphapulse`, Compose project `alphapulse-local` and named local volumes already matched the stable product identity and are preserved.

GitHub repository redirects preserve old source links, but GHCR packages do not automatically move. Publish and scan images under `ghcr.io/chuliyu/alphapulse/*`, pin reviewed digests, then validate pull permissions and a staging rollout before applying cloud manifests. Do not delete old packages/volumes as part of this source refactor. Private submodule identity is unchanged.

External portfolio/profile repositories may still contain the former URL and older product descriptions; they are outside this project branch. Update those claims only with matching implementation evidence. Historical logs, saved plans and archived documents retain old identifiers as evidence; do not use them as execution instructions.

## Service objectives to validate

Proposed engineering exercise profile: 20 synthetic portfolios, 1,000 positions each, 20 concurrent read users, an end-of-day data batch and one approval workflow. Candidate gates are read API p95 under 500 ms at that load, no duplicate economic events under replay, and daily recoverable snapshots. These are unmeasured proposals, not achieved SLOs.

Freshness windows must be derived from the selected market/calendar rather than wall-clock guesses. RPO/RTO, availability target and cloud cost budget remain open in the roadmap; demonstrate a restore and measure actual recovery before adopting numerical commitments.

## Observability and failure handling

Instrument request traces, portfolio/snapshot correlation IDs, ingestion lag, data freshness, reconciliation breaks, blocked approval counts, outbox lag, retries and AI timeout/abstention. Do not log private holdings or prompts in unrestricted telemetry. Alert on actionable quality/recovery failures, with an owner and runbook.

A failed data batch quarantines its input and leaves the last published version identifiable as stale. A failed model request leaves the evidence screen usable. An outbox publisher retry must not duplicate state transitions. Never repair a ledger by editing rows without an attributable correction.

## Release and rollback gate

1. Run scoped domain, security, contract and PostgreSQL migration tests; record exact source revision and dependency/image versions.
2. Build immutable images and review vulnerability findings; do not equate an audit with absence of vulnerabilities.
3. Apply backward-compatible migrations in staging, verify existing readers/writers and test backup restore to a separate database.
4. Measure the named workload and failure cases. Document the migration's rollback/forward-recovery plan; an image rollback cannot undo every database migration.
5. Obtain the configured environment release approval and deploy only reviewed artifacts. Confirm health, freshness, reconciliation and audit continuity; retain a dated evidence record.

Historical cloud deployment files remain an implementation reference. No infrastructure apply, image push or workload migration was performed by the architecture refactor.
