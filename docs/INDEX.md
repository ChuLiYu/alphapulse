# Context router and authority map

Start here for active project knowledge. Read the task row, then its dependencies; do not load every document. English specifications are canonical. [Traditional Chinese orientation](zh-TW/overview.md) explains the same direction without becoming a second rule source.

## Authority and maintenance

The repository maintainer owns product decisions and acceptance. Engineering, data, security, and operations below are maintenance responsibilities, not claims that a staffed team exists.

| Task / knowledge | Single authority | Maintainer responsibility | Update / validation |
|---|---|---|---|
| Purpose, users, scope, hiring evidence | [Product strategy](product/strategy.md) | Product | Review business scope against user intent and delivery plan |
| Investment semantics and acceptance | [Domain rules](domain/investment-operations.md) | Product + domain/data engineering | Stable rule IDs; independent golden examples and boundary tests |
| Current implementation | [Source](../src/alphapulse/) and [tests](../tests/) | Engineering | Execute scoped checks; do not infer approval from code |
| Runtime API contract | FastAPI route/schema definitions under [api](../src/alphapulse/api/) | API engineering | Generate OpenAPI from running app at `/api/openapi.json`; do not hand-maintain duplicate schemas |
| Existing database structure | [SQLAlchemy models](../src/alphapulse/api/models.py), [identity models](../src/alphapulse/api/models_user.py) and existing initialization scripts | Data engineering | Current workflow uses `create_all`; versioned migrations are a release blocker for new persistent investment data |
| Target boundaries and operational requirements | [Target architecture](architecture/target.md) | Architecture + engineering | ADRs for changed boundaries; acceptance evidence before promotion |
| Decision rationale | [ADR index](architecture/README.md) | Decision author / maintainer | Preserve alternatives and supersession links |
| AI scope, trust and evaluation | [AI governance](ai/governance.md) | AI + security engineering | Evaluate numerical grounding, citations, permissions, refusal and failure modes |
| Work order, gaps, decision backlog | [Roadmap](ROADMAP.md) | Product + engineering | Update evidence with each delivered slice |
| Local commands and dependencies | [Development guide](DEVELOPMENT.md), actual dependency/Compose files | Engineering | Build and integration checks; versions live in executable manifests |
| Verification and release gates | [Testing](TESTING.md) | Test + engineering | Golden oracles, integration boundaries, measured results |
| Security and operations | [Security](SECURITY.md), [operations](engineering/operations.md) | Security + operations | Threat-path tests, recovery drill and release evidence |
| Agent behavior | [Project instructions](../AGENTS.md) | Maintainer | Keep short; project facts remain in this map |
| Historical agent and local results | [Agent evidence](agents/EVIDENCE.md), [local evidence](local/VERIFICATION.zh-TW.md) | Evidence author | Append new dated evidence; never relabel old runs as current |
| Reproducible context validation | [Verifier](../scripts/verify_context.py) | Engineering | `python3 scripts/verify_context.py` in local development and CI |

## AI Flywheel Core application

Method provenance: [ai-flywheel-core](https://github.com/ChuLiYu/ai-flywheel-core) principles were read from the local asset repository during this refactor. This project owns its product rules and commands; it does not vendor personal roles, tokens, adapters, or home-directory symlinks. There is no automatic synchronization from personal defaults.

Use **Locate → Load context → Resolve ambiguity → Implement → Synchronize → Validate**. Example: to add an FX valuation behavior, start with `VAL-02` in the domain rules, load the valuation module and tests, resolve unsupported currency/as-of semantics, implement, update the domain acceptance mapping, and run the portfolio suite plus context verifier. The current valuation slice applies this process; it does not demonstrate the later approval workflow.

## Historical documents

Files carrying a `Legacy reference` notice are preserved for rationale and compatibility, not current product instructions. This includes old architecture prompts, MLOps execution plans, frontend specifications and deployment guides. Historical ADRs and test artifacts remain at their original paths so existing evidence can be traced. New work must resolve conflicts using this map rather than an archived prompt or a document's modification date.

## Module navigation and migration coverage

This table covers every top-level delivery module. “Preserved” means kept for compatibility, not validated as a new investment capability. Existing source dependencies remain authoritative; the target does not rewrite them by declaration.

| Module / entry | Purpose and context route | Refactor disposition / check | Remaining gap |
|---|---|---|---|
| [API](../src/alphapulse/main.py), [security](../src/alphapulse/security/) | Existing routes, identity, permission checks; [security policy](SECURITY.md) | Preserved; product metadata renamed; selected security regression | Global roles only; portfolio ACL and new investment API planned |
| [Portfolio](../src/alphapulse/portfolio/) | New pure valuation; [VAL-01–05](domain/investment-operations.md) | Implemented; golden/failure tests and import boundary check | Persistence, provenance and reconciliation planned |
| [Agents](../src/alphapulse/agents/) | Existing bounded Ollama PoC; [protocol/evidence](agents/EVIDENCE.md), [future AI](ai/governance.md) | Preserved; host protocol regressions | Investment tools, retrieval and grounding evals planned |
| [ML](../src/alphapulse/ml/), [monitoring](../src/alphapulse/monitoring/) | Legacy crypto ingestion, predictions and drift | Preserved as legacy; no investment claims | Full ML dependency conflict and workflow tests unresolved |
| [Frontend](../frontend/) | Existing React dashboard; [target UI boundary](architecture/target.md) | Title renamed; legacy UX preserved | Investment workflow, typed new API and quality states planned |
| [Airflow](../airflow/), [training](../training/) | Legacy scheduling and training; [historical training](TRAINING.md) | Preserved; not part of new valuation runtime | Scheduled EOD workflow/backfill and model need not established |
| [Infrastructure](../infra/) | Compose core plus historical Terraform/k3s; [operations](engineering/operations.md) | Repo/image references renamed; volume identities preserved; Compose/config checks | New images unpublished; no new cloud validation/deploy/restore evidence |
| [Scripts](../scripts/), [CLI](../alphapulse) | Repeatable setup, maintenance and validation; [development](DEVELOPMENT.md) | New context checker; domain tests added to container test command | Historical deployment scripts remain opt-in and require review |
| [Tests](../tests/), [CI](../.github/workflows/) | Risk-based verification; [test strategy](TESTING.md) | New context/domain CI uses local commands; fake scheduled cost claims retired | Container/live-model/ML/recovery gates reported separately |
| [Examples](../examples/) | Historical/synthetic agent examples | Preserved; no reclassification as investment evidence | New demo lives beside the portfolio domain |
| [Docs](.) and [project instructions](../AGENTS.md) | Authority map, English specs, ADRs and derived guides | Active navigation verified; legacy documents labeled | Mechanical check does not prove semantic equivalence |
| Optional private submodule (`private/`) | Existing separate repository; [.gitmodules](../.gitmodules) | Excluded from public-core runtime; not initialized or modified | Its code was not inspected or tested |

Actual command outcomes and exceptions are recorded in [refactor verification](engineering/refactor-verification.md). This coverage map governs the refactor scope; the roadmap governs future capability delivery.

## Document language and reading editions

English is authoritative for active project specifications. The selected Traditional Chinese editions are summaries, not full translations: [orientation](zh-TW/overview.md) covers purpose, navigation, setup and key domain ideas; [architecture](zh-TW/architecture.md) covers boundaries and ADR-008 tradeoffs. Their headers identify reviewed sources and synchronization status. Update covered content with its English source or mark it outdated.

Existing Chinese local verification, setup audits and prior review records retain their original historical/evidence status. The existing local Chinese setup guide is retained as a baseline reference; current setup commands are owned by the English development guide. Historical ADRs and prompts retain their original language. Do not duplicate executable schemas or AGENTS instructions as translated authorities.
