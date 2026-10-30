# Verification strategy

Tests are selected from financial and control failure modes. A passing mock, link check, type checker or coverage percentage does not approve business semantics or establish production readiness.

| Boundary | Required evidence | Entry point / state |
|---|---|---|
| Context and new portfolio dependency direction | Required authority files, active relative links, stale active repo names, no framework/ORM/model imports in pure portfolio domain | `python3 scripts/verify_context.py` |
| Verifier failure behavior | Isolated broken link with nonzero CLI exit; missing authority, stale identity and prohibited import failures | `python3 -m unittest discover -s tests/context -v` |
| Valuation | Hand-calculated golden values, precision/rounding, unsupported/nonfinite/duplicate inputs and missing/stale/future marks | `PYTHONPATH=src python3 -m unittest discover -s tests/portfolio -v` |
| Existing agent protocol | Tool budgets, schema/transport/dependency checks; no live model by default | `PYTHONPATH=src python3 -m unittest discover -s tests/agent_poc -v` |
| Existing security + core | Auth rejection, scoped route access, secret handling; PostgreSQL/API/frontend integration | `./alphapulse test` in the existing isolated container stack |
| API and persistence (new investment workflow) | Real PostgreSQL transaction/constraint tests, migrations, idempotency, corrections and authorization, OpenAPI contract checks | Planned with phase 1b; SQLite cannot prove PostgreSQL behavior |
| Approval / event delivery | State and version races, self-approval denial, atomic audit/outbox, crash/retry/replay and duplicate delivery | Planned phase 3/4 |
| AI explanations | Independent numeric oracle, reviewed citation support and authorization/adversarial cases | Planned; [AI evaluation](ai/governance.md) |
| Operating release | Pinned workload, load/failure experiment, restore and migration drill | Planned; [operations](engineering/operations.md) |

The portfolio unit tests cover only supplied synthetic snapshots. They do not prove custody, accounting, legal compliance or market-data accuracy. The existing selected security tests cover specific paths rather than a full audit.

The security suite uses pytest so both unittest classes and function-style tests are collected. Host fallback with the pinned test dependencies: `PYTHONPATH=src:airflow/plugins python -m pytest tests/security -v`. These SQLite/mocked-path checks do not replace PostgreSQL and service integration.

CI runs the context/domain checks independently of historical ML dependencies. Existing container and agent workflows remain. See [current refactor verification](engineering/refactor-verification.md) for commands actually run, outputs and limitations; earlier results stay in their original evidence records.
