# Delivery roadmap and decision backlog

[繁中閱讀摘要](zh-TW/overview.md) — selected concepts; the complete English specification remains authoritative.

This is the work/status authority. Dates are not delivery promises. “Implemented” means source exists; “verified” requires the stated run. Existing baseline results are preserved separately from new work.

| Phase | Outcome | Acceptance / evidence | Current state |
|---|---|---|---|
| 0: identity and context | Rename, branch, English router, authority map, ADR, legacy classification | Current URLs/settings, link/boundary check and reviewable Git diff | Implemented in this branch |
| 1a: domain seed | Offline synthetic multi-currency valuation with fail-closed quality | VAL-01–05 golden, rounding, invalid/missing/stale/future data tests | Implemented; see current verification record |
| 1b: investable book | Versioned instruments/transactions/marks, trade-date holdings, cash reconciliation | PostgreSQL migrations and constraints; duplicate/replay/correction tests; independent statement breaks; typed authenticated API and operations UI | Planned |
| 2: investment analysis | Exposure, benchmark-aligned performance, deterministic stresses | PERF-01/RISK-01 examples, cash flows/dividends, missing history, scenario explainability and reconciliation | Planned |
| 3: controlled proposals | Java/Spring order workflow, maker-checker, mandate evidence and audit | ORDER-01–03/CTRL-01; portfolio ACL, self-approval rejection, concurrent stale-version rejection, atomic persistence and idempotent retries | Planned; Spring version pin at implementation |
| 4: event delivery and AI | Outbox/Kafka consumers if justified; read-only evidence-grounded explanations | Replay/deduplication/DLQ tests; AI authorization, citation, numerical and abstention evaluations | Planned; existing Ollama PoC stays isolated |
| 5: operating evidence | Deployable cloud profile, telemetry and recovery | Measured load profile, SLO report, backup restore, migration rollback and incident drill with reviewed findings | Proposed; cloud budget/provider pending |

## Refactor order and compatibility

Preserve existing local Compose/CLI and security tests while introducing domain modules. Add persisted investment data through migrations; do not rename crypto tables into a ledger. Add a versioned portfolio API and UI only after input provenance and portfolio authorization exist. Deprecate the legacy signals dashboard explicitly; never replace a real failure with demo values.

Extract an approval service only when it owns a complete transaction and can operate under dependency failure. Keep a modular implementation until that point. Publish new container images before using renamed cloud manifests. The public repository name changes immediately, but these branch changes are not deployed and existing GHCR packages have not been migrated.

## Decisions that block later work

| Decision | Evidence needed / impact | Responsible perspective |
|---|---|---|
| Market calendar and corporate actions | Exchange/vendor policy; affects holdings and return correctness | Domain/data |
| Mandate examples and override policy | Explicit educational thresholds and reviewer authority; affects approval tests | Product/risk |
| Settlement, cash flow and fee conventions | Selected instruments and business rules; affects accounting and TWR | Domain |
| Data source and benchmark license | Permitted use, retention and reproducibility; synthetic fixtures remain default | Product/data |
| OIDC and portfolio access model | Identity provider, subject lifecycle, role/portfolio grants | Security |
| Cloud profile and budget | Provider/region, residency needs, target workload and monthly budget | Maintainer/operations |
| Service objectives | Workload, freshness windows, RPO/RTO and measurement method | Product/operations |

These do not block the offline synthetic valuation slice. No legal mandate or production policy is inferred from a job advertisement.

## Next concrete slice

Deliver phase 1b in one reviewable workflow: import a synthetic transaction file twice, reconstruct positions once, quarantine stale FX, show the reconciliation break, correct the evidence and retain both snapshot versions. Include a PostgreSQL integration test, an authenticated portfolio endpoint, typed UI exception state, and a dated verification record. This is planned work, not already completed by the architecture refactor.
