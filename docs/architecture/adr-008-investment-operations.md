# ADR-008: Investment operations focus and incremental architecture

[繁中閱讀摘要](../zh-TW/architecture.md) — selected concepts; the complete English specification remains authoritative.

Status: Accepted for direction and incremental refactor on 2026-10-30. Java service extraction, messaging and cloud vendor choices remain proposed implementation steps.

## Context

The user requested the name AlphaPulse, a project suitable for asset management software engineering roles, evidence of business and technical understanding, appropriate AI, enterprise specifications, an isolated branch, English-primary documentation and AI Flywheel Core's context architecture.

Baseline commit `81bbd4d` contains an existing Python/React financial-data application, legacy crypto/ML workflows, a containerized local core and a standalone synthetic-data tool-calling agent. The initial local directory lacked those tracked files; the public upstream was cloned without its private submodule. The pre-existing personal OpenCode audit was preserved locally and remains untracked; it is not a project instruction or public-core artifact. No private repository content was imported.

## Decision

1. Rename local directory and public repository to `alphapulse`, preserve the Python package/CLI names and local data volume names, and make changes on `refactor/asset-management-platform`.
2. Adopt investment operations as the product scope, with domain acceptance rules and explicit status/evidence. Supersede ADR-006's infrastructure-first product positioning; preserve its historical rationale.
3. Keep the working stack and introduce a pure portfolio domain first. Develop the Java/Spring order boundary when its business workflow is ready; introduce Kafka only for concrete cross-service consumers.
4. Use one project context router, authority map, stable domain IDs, ADRs, and reproducible checks. Do not copy personal AI roles or install adapters into the project.
5. Make English authoritative. Chinese orientation and architecture companions point to canonical rules; historical evidence is preserved in its original language.
6. Keep AI read-only for investment decisions. Deterministic systems own calculations, limits and state changes.

## Alternatives and consequences

A full Java rewrite would discard verified Python behavior and delay the first business scenario. A Python-only final system is simpler, but gives less direct JVM evidence for relevant roles; the phased order service permits a purposeful comparison. Immediate microservices/Kafka/Kubernetes would add operating overhead before validating the workflow. Continuing crypto/MLOps branding does not satisfy the user's revised objective.

The project temporarily contains legacy and new boundaries. This is visible in the router and roadmap rather than concealed by renaming routes or claiming legacy mocks are real investment workflows. Enterprise readiness remains an acceptance target requiring implementation and operating evidence.

## References

[Product](../product/strategy.md) · [Target architecture](target.md) · [Roadmap](../ROADMAP.md) · [Previous ADR](adr-006-backend-first-strategy.md)
