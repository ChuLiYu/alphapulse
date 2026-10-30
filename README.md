# AlphaPulse

**An investment operations workbench for asset management software engineering.**

AlphaPulse is being refactored from a crypto/MLOps portfolio into a system that explains how portfolio data becomes a valuation, a risk decision, an independently approved trade proposal, and an auditable operating record.

The goal is to demonstrate both software engineering and investment business understanding. Enterprise requirements are defined as measurable acceptance gates; they are not a claim that this personal project is production ready.

[Context router](docs/INDEX.md) · [Product scope](docs/product/strategy.md) · [Target architecture](docs/architecture/target.md) · [Delivery plan](docs/ROADMAP.md) · [繁體中文導讀](docs/zh-TW/overview.md)

## What exists today

| Area | Evidence and limits |
|---|---|
| Existing application | Python/FastAPI, SQLAlchemy/PostgreSQL, React/TypeScript, containerized local core; legacy crypto endpoints and dashboard remain. |
| New investment domain | A deterministic, offline holdings valuation slice with explicit FX direction, decimal policy, and fail-closed data quality. See [rules](docs/domain/investment-operations.md) and [tests](tests/portfolio/). |
| Existing AI | Bounded Python/Ollama tool-calling over synthetic monitoring fixtures. [Evidence](docs/agents/EVIDENCE.md). This agent does not yet retrieve portfolio data or investment research. |
| Infrastructure | Compose, Terraform and k3s definitions exist. Hosted services are offline; the cloud design is historical and not validated for the new scope. |
| Planned capabilities | Persisted positions, reconciliation, risk/performance, maker-checker approvals, portfolio authorization, and grounded AI explanations. Track delivery in the roadmap. |

## Intended workflow

```text
Versioned prices / FX / transactions
    → reconciled trade-date positions → valuation + quality exceptions
    → exposure / benchmark / scenario analysis
    → proposed rebalance → deterministic mandate checks
    → independent approval → simulated execution → reconciliation + audit
```

The first investment universe is synthetic long-only listed equities and ETFs in USD/CAD, with USD reporting. This is an educational investment book of record, not a fund accounting, brokerage, or regulatory compliance product. The [domain specification](docs/domain/investment-operations.md) owns the rules and exclusions.

## Technology and engineering judgment

The existing delivery stack is Python, FastAPI, PostgreSQL, React/TypeScript, Docker Compose, and GitHub Actions. Target extensions include Java/Spring Boot for the order/approval boundary, Kafka with a transactional outbox when cross-service delivery is needed, S3-compatible immutable input storage, OIDC, and OpenTelemetry. AWS/Terraform is a proposed deployment target; Kubernetes is an optional later operating exercise.

Each addition has a purpose and entry gate in the [architecture](docs/architecture/target.md). Airflow and MLflow remain legacy capabilities until a scheduled pipeline or real model lifecycle justifies their use. Repository dependency files remain the source for actual installed versions.

## Run and verify

Host-only, dependency-free checks:

```sh
python3 scripts/verify_context.py
python3 -m unittest discover -s tests/context -v
PYTHONPATH=src python3 -m unittest discover -s tests/portfolio -v
PYTHONPATH=src python3 -m alphapulse.portfolio.demo
PYTHONPATH=src python3 -m unittest discover -s tests/agent_poc -v
```

Existing local platform (OrbStack and Docker Compose required):

```sh
./alphapulse setup
./alphapulse up
./alphapulse test
./alphapulse down
```

[English development guide](docs/DEVELOPMENT.md) · [Existing local guide / 中文](docs/local/README.zh-TW.md) · [Verification policy](docs/TESTING.md). The investment valuation slice is currently a Python library/CLI; the legacy web dashboard has not been converted into a portfolio UI.

## AI with a defined boundary

The intended AI features explain deterministic risk/quality results and summarize permission-filtered research with source citations and as-of dates. AI cannot approve or submit trades, change limits, alter ledgers, or supply unverified prices. See [AI design and evaluation](docs/ai/governance.md).

## Evidence and historical context

The imported baseline is commit `81bbd4d`. Existing [agent evidence](docs/agents/EVIDENCE.md) and [local verification](docs/local/VERIFICATION.zh-TW.md) describe their original test scope; they do not certify the refactored platform. Older specifications and prompts are explicitly marked as legacy. No latency, cost saving, investment return, or production-readiness claim is inferred from the presence of configuration files.
