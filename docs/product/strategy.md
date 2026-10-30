# Product strategy

[繁中閱讀摘要](../zh-TW/overview.md) — selected concepts; the complete English specification remains authoritative.

Status: project direction selected on 2026-10-30; detailed target policies below are engineering proposals for an educational product. They are not approved investment mandates or firm policies.

## Objective and users

Demonstrate readiness for software engineering in asset management by delivering an explainable investment workflow with correct financial data, explicit controls, useful APIs, and credible operational evidence.

| User | Decision / job | Software evidence |
|---|---|---|
| Portfolio manager | Understand holdings, exposure, cash, and rebalance impact | As-of valuation, drill-down provenance, scenarios and proposed orders |
| Investment operations analyst | Find and resolve position/cash breaks | Idempotent imports, reconciliation reports, corrections with audit history |
| Risk / compliance reviewer | Check a proposal against a versioned mandate | Deterministic checks, stale-data rejection, independent approval |
| Research analyst | Explain changes using permitted sources | Grounded AI summaries with citations and abstention |

The interview story is a reproducible case: a CAD security arrives with stale FX; valuation is blocked, an exception is visible, a corrected input yields a versioned result, and a proposed overweight trade cannot bypass independent review. Only the first valuation portion is implemented in this refactor.

## Scope and exclusions

Start with synthetic, licensed-safe equity/ETF fixtures; long-only quantities; USD/CAD instruments and cash; USD reporting; end-of-day marks. A portfolio is an investment book of record (IBOR) exercise, not legal fund NAV. Settlement-aware cash, corporate actions, benchmark handling and transaction accounting enter through staged acceptance gates.

No live order routing, custody, tax accounting, derivatives, margin, high-frequency execution, return promises, or claims of regulatory certification. Existing cryptocurrency code is a legacy technical example and is not silently mapped to equities.

## Hiring evidence

Selected official examples, checked 2026-10-30, support relevance rather than a claim about market-wide prevalence:

- [BlackRock software engineering](https://careers.blackrock.com/students-and-graduates-functions-software-engineering): investment workflow knowledge, Java/Python, databases, React/Angular, Kafka, containers and AI.
- [Fidelity asset management engineering role](https://jobs.fidelity.com/en/jobs/2133344/principal-software-engineer-javaspringboot/): Java/Spring, SQL, AWS/EKS, messaging, security and delivery discipline. This senior role informs technical context, not a claim that this project qualifies its author for that seniority.
- [Aladdin workflow overview](https://www.blackrock.com/aladdin/about-us/about/faqs): integrated portfolio management, risk, trading, compliance and operations motivates the end-to-end scenario; this project is not an Aladdin replica.
- [CFA portfolio performance evaluation](https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/portfolio-performance-evaluation): measurement, attribution and appraisal have distinct meanings; attribution must reconcile and benchmarks must fit the portfolio.

## Evidence standard

Success means a reviewer can run the fixtures, trace a business rule to code/test, explain failure handling, inspect an approval/audit trail when implemented, and reproduce recorded operations. Coverage percentage or a collection of enterprise tools alone does not demonstrate this. Quantitative latency, throughput, reliability, AI quality and cost targets require recorded workloads and measurements before being described as achieved.

Open decisions belong to the [roadmap](../ROADMAP.md); financial definitions belong to the [domain authority](../domain/investment-operations.md).
