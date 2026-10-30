# Development

[Context router](INDEX.md) is the entry point. Use English for code-facing documentation; the [Chinese guide](zh-TW/overview.md) is an orientation companion.

## Dependency-free domain and context work

Python 3.12 matches the existing runtime. No package installation is needed for these commands:

```sh
python3 scripts/verify_context.py
python3 -m unittest discover -s tests/context -v
PYTHONPATH=src python3 -m unittest discover -s tests/portfolio -v
PYTHONPATH=src python3 -m alphapulse.portfolio.demo
PYTHONPATH=src python3 -m unittest discover -s tests/agent_poc -v
```

## Existing containerized core

Start OrbStack with its Docker context available, then run:

```sh
./alphapulse setup
./alphapulse up
./alphapulse test
./alphapulse audit
./alphapulse down
```

`setup` creates private `.env.orbstack.local` settings and builds images. `down` preserves database/model volumes. Ports are loopback-only; defaults are API 8000 and frontend 3000. Do not commit generated settings. The command keeps the `alphapulse-local` project and existing named volumes stable across the repository rename; no automatic volume deletion/migration is needed.

`./alphapulse agent` starts the separate containerized Ollama monitoring PoC and may download a model. It uses synthetic crypto fixtures and is not the new investment assistant. [Existing detailed local instructions](local/README.zh-TW.md) and [prior verification](local/VERIFICATION.zh-TW.md) retain their scope.

## Actual version authorities

- API/test images: `infra/local/requirements-api.txt`, `infra/local/requirements-test.txt`, and Dockerfiles.
- Frontend: `frontend/package.json` and `frontend/package-lock.json`; use `npm ci`, not an unconstrained install.
- Full historical ML environment: root/training/Airflow requirements and `src/setup.py`; dependency compatibility remains separate from the local core.
- Future Java implementation must add its own build/wrapper and pinned supported versions before any service is described as available.

Do not initialize the optional private submodule for ordinary work. The public core and new domain checks must remain independent of private content. Cloud workflows are not a local development requirement.

## Change workflow

Locate the relevant authority in INDEX, record unresolved business choices, change the smallest complete slice, synchronize rules/contracts/evidence, run scoped tests, and inspect `git diff --check`. Follow [testing](TESTING.md) for the difference between pure-domain, API, DB and operating evidence.
