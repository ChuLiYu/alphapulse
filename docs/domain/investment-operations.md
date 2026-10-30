# Investment operations domain rules

[繁中閱讀摘要](../zh-TW/overview.md) — selected concepts; the complete English specification remains authoritative.

Status: proposed educational-product policies, with the implemented subset identified below. The user selected the project direction; these detailed policies are not representations of a real client's mandate. Changes affecting investment behavior require explicit rationale and acceptance updates.

## Implemented valuation slice

`src/alphapulse/portfolio/valuation.py` evaluates caller-supplied snapshots. There is no database, network, ledger mutation, portfolio ACL, or order capability in this slice. `python -m alphapulse.portfolio.demo` uses explicitly synthetic inputs.

| Rule | Policy / observable acceptance |
|---|---|
| VAL-01 | Inputs use finite `Decimal` values, never floats. Long-only positions and cash must be nonnegative; price and FX must be positive. USD/CAD only; USD reporting only. Reject unsupported values, duplicate instrument/cash/FX keys, excessive precision, and malformed input. |
| VAL-02 | FX is **USD per one unit of local currency**. USD is identity 1. A CAD position's USD value is quantity × unadjusted local price × CAD/USD rate. Never guess an inverse rate or missing quote. |
| VAL-03 | All required price and FX marks must have the exact snapshot business date. Missing, stale, or future marks block the complete total: return quality issues and `total_usd = null`, not zero or a partial total disguised as complete. The caller owns business-calendar selection; calendar-aware carry-forward is not implemented. Unused supplied marks do not contribute to the valuation; their basic types and bounds are still validated. |
| VAL-04 | Policy bounds: quantity ≤ 10^12 with ≤ 6 decimal places; price ≤ 10^9 with ≤ 6 places; FX ≤ 10^3 with ≤ 8 places; cash ≤ 10^15 with ≤ 2 places. Use an isolated Decimal context with precision 64. Sum unrounded values, then round the total to USD cents using HALF_EVEN. Report line values at cents separately; their rounded sum may differ. No global Decimal context mutation. |
| VAL-05 | Scope is marked security value plus supplied cash, **not fund NAV**: excludes accruals, fees, tax, unsettled receivables/payables and corporate actions. Require `data_kind = synthetic` in the demo result and emit a snapshot ID and business date for traceability. No runtime synthetic fallback for missing real inputs. |

Independent golden scenario: 10 shares × USD 100.005 + 2 shares × CAD 50 × 0.75 + USD cash 25 = USD 1100.05. A separate pair of USD 0.005 lines sums to USD 0.01, even though each line rounds to USD 0.00 under HALF_EVEN.

Implementation/test mapping: VAL-01–05 → [valuation](../../src/alphapulse/portfolio/valuation.py), [golden and failure cases](../../tests/portfolio/test_valuation.py). The tests prove only the stated synthetic snapshot behavior; persisted accounting and production correctness remain unverified.

## Target accounting and investment semantics

| Rule | Required future behavior / acceptance gate |
|---|---|
| DATA-01 | Instrument identity separates internal ID, ticker, exchange, currency and effective dates. Use immutable vendor/source versions, event/as-of time and ingestion time; corrections create a new version and can reproduce the previous result. |
| DATA-02 | Validate schema, duplicate keys, calendar, missingness, freshness and source reconciliation before publication. Store raw input evidence with checksums and provenance. Bad inputs are quarantined; no implicit demo fallback. |
| BOOK-01 | Transactions have immutable business IDs, versions and idempotency keys. Position reconstruction is trade-date based; settlement cash is tracked separately. Handle buys/sells, fees and corporate actions through explicit event policies, not ad hoc adjustments. |
| BOOK-02 | Compare derived positions and cash with an independent synthetic custodian statement; distinguish timing differences from breaks. A break has owner, reason, resolution and an audit trail. Reimports do not double-count. |
| PERF-01 | Time-weighted return neutralizes external cash-flow timing through defined subperiod valuations. Money-weighted return is distinct. Define dividends, expenses, missing marks and benchmark total-return/currency/calendar alignment before implementation. Never compute an annualized ratio or VaR from insufficient history and substitute zero. |
| RISK-01 | Show gross/net exposure, currency and sector concentration and explicit deterministic price/FX stress. Label assumptions, input versions and limitations. Historical VaR is a later model with a documented window, horizon, quantile convention, backtest and failure policy; a scenario is not a prediction. |
| ORDER-01 | Proposal state: DRAFT → CHECKED → APPROVED → SIMULATED → RECONCILED; REJECTED/CANCELLED are terminal for that version. Checks bind input snapshot, order version, mandate version and results. Any material edit or expired evidence invalidates approval. |
| ORDER-02 | The creator cannot approve their own proposal. Permissions are role- and portfolio-scoped, checked server-side on every transition. Stale evidence, breaches and unresolved required checks block approval; concurrency uses version checks and one database transaction. |
| ORDER-03 | No live broker connection. Simulation records deterministic fills, fees and settlement assumptions. Audit records actor, action, subject/version, before/after references, timestamp, reason and correlation ID. Retries cannot create duplicate orders or fills. |
| CTRL-01 | Example concentration, cash and restricted-security rules are configurable, versioned **demo policies**, not legal compliance advice. Risk reviewer overrides, if introduced, must have explicit authorization, reason and immutable evidence; the AI cannot issue an override. |

## Worked future scenario

Given a portfolio mandate with a configured single-name cap, when a proposed order breaches that cap, the deterministic result is blocked with rule ID and input versions. A generated explanation can describe that result but cannot change it. An independent approver must also fail if the underlying snapshot was corrected after checking. This is a specification scenario, not a passing integration test today.

## Decisions still needed

Supported exchange calendars, corporate-action vendor policy, fee/tax treatment, settlement conventions, benchmark license, numerical performance method and real mandate thresholds need explicit selection before their implementation phase. No rule in the legacy trading-signal code establishes these policies.
