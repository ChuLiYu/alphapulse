# Refactor verification — 2026-10-30

Scope: rename and asset-management architecture refactor on `refactor/asset-management-platform`, imported baseline `81bbd4d`. Results below apply to the branch changes recorded with this file, not an upstream CI run or a deployed system. [Coverage map](../INDEX.md#module-navigation-and-migration-coverage) accounts for the preserved and changed modules; [roadmap](../ROADMAP.md) distinguishes implemented slices from future work.

## Executed checks

Environment: macOS arm64, CPython 3.12.14. Existing API/test dependencies were installed from `infra/local/requirements-test.txt` into a temporary virtual environment outside the repository. No project dependencies were installed into the system Python. Frontend dependencies/build were isolated in a temporary source copy, using its existing lockfile, Node 26.0.0 and npm 11.12.1; this is not the Node 22 container build.

| Command / check | Observed result | Limit |
|---|---|---|
| `python3 scripts/verify_context.py` | Active authority/link/identity/import checks passed | Static literal links/imports only; no business approval, external URL or translated-meaning validation |
| `python3 -m unittest discover -s tests/context -v` | 5 passed | Isolated fixtures: missing authority, broken link with nonzero CLI exit, stale identity, invalid Python and forbidden imports |
| `PYTHONPATH=src python3 -m unittest discover -s tests/portfolio -v` | 14 passed | Synthetic supplied snapshots only; no persistence, API or market-data correctness claim |
| `PYTHONPATH=src python3 -m alphapulse.portfolio.demo` | Complete synthetic snapshot, USD `1100.05` | Matches the independent arithmetic in VAL-01–05 |
| `PYTHONPATH=src python3 -m unittest discover -s tests/agent_poc -v` | 15 passed; 1 opt-in live Ollama test skipped | Protocol/replay and failure handling only; no new live inference result |
| `PYTHONPATH=src:airflow/plugins python -m pytest tests/security -q` in temporary environment | 18 passed; 88 warnings | Existing auth uses isolated SQLite and mocked dependencies; not PostgreSQL integration or a full security audit |
| `npm ci --no-audit --no-fund` then `npm run build` in temporary frontend copy | Build passed | Existing runtime-config script and large-bundle warnings; no browser workflow or new portfolio UI tested |
| `docker compose -f infra/local/compose.yml config --quiet` with explicitly synthetic environment values | Passed | Configuration parsing only; no daemon, images or services exercised |
| `terraform fmt -check -recursive infra/terraform` | Passed | Formatting only; no provider initialization, validate, plan or apply |
| YAML parse of all 7 GitHub workflow files | Passed; trigger and job mappings present | Parsing only; workflows were not executed on GitHub |
| `sh -n alphapulse`, syntax checks for changed shell scripts, `git diff --check` | Passed | Syntax/whitespace only |
| `gh repo view ChuLiYu/alphapulse --json name,url,defaultBranchRef` and local remote inspection | Canonical repository `https://github.com/ChuLiYu/alphapulse`, default branch `main`; local origin matches | Source branch not pushed; GHCR image packages not migrated |

Warnings in the security run include existing SQLAlchemy/Pydantic/UTC API deprecations, the deliberately short forged JWT test key and the Starlette test-client compatibility warning. They were not hidden or treated as new production guarantees. Frontend installation reports existing deprecated transitive tools. Dependency vulnerability auditing was not run in this session.

## Workflow corrections

- New context/domain CI invokes the same local commands, without legacy ML dependencies.
- The container test image includes the portfolio tests. Security CLI/CI uses pytest because unittest discovery omitted the existing function-style health error-disclosure regression (17 collected before, 18 with pytest).
- Terraform formatting is a read-only failing check rather than an automatic source commit; its validation job no longer receives a Terraform Cloud token.
- The former scheduled cost report contained fixed prices and unmeasured savings. It is replaced by a manual status report stating the missing billing evidence, with no Slack send. No new cost or savings result is claimed.

## Checks not executed and remaining gates

The OrbStack socket `/Users/liyu/.orbstack/run/docker.sock` was unavailable. Therefore `./alphapulse setup`, `./alphapulse test`, image audits and the PostgreSQL/API/frontend smoke workflow were **not executed**. Their previous results remain historical. Container image changes require a fresh build and that integration run before merge/release acceptance.

No cloud deployment, Terraform provider validation, new GHCR publish, live broker action, private submodule initialization, live-model evaluation, full legacy ML suite, load test, restore drill or migration exercise occurred. The legacy ML dependency conflict remains outside this slice. These are explicit open gates, not passing checks.

The English authority documents and Chinese summaries were compared for scope, current-versus-target status, FX direction, fail-closed behavior, AI restrictions and deployment limitations. Summaries intentionally omit detailed acceptance tables and direct readers to the English rules. Their headers identify the actual reviewed source revision; mechanical link checks do not certify translation equivalence.

## Handoff

Read README → INDEX → the relevant authority → code/tests. For the implemented example, VAL-02 and VAL-04 define FX and precision, the independent USD `1100.05` example anchors acceptance, the pure module implements it, and missing/stale FX tests verify blocking. This is an executed domain example of the flywheel workflow. Persisted book/reconciliation/approval/AI scenarios remain future acceptance criteria.

Changes remain on the requested refactor branch. No merge, branch push, image publish or deployment is part of this handoff.

The pre-existing personal `docs/opencode-setup-audit.md` is preserved unchanged and untracked. It is excluded from the refactor commits; its embedded requests are historical document content, not instructions for this task.
