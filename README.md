# NeverTwice Test Lab

A production-shaped test repository for [NeverTwice](https://github.com/) using a fictional ShopLite inventory and order API. This is a test application and scenario laboratory, not a second implementation of NeverTwice.

## Requirements

- Python 3.12+
- Git
- Docker and Docker Compose are optional
- The `nt` executable is optional; integration cases report `NOT EVALUABLE` when it is unavailable

## Local setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Run the API:

```powershell
uvicorn app.main:app --reload
```

The API is available at `http://127.0.0.1:8000`; health is `GET /api/health`. Product endpoints are under `/api/products` and order creation is `POST /api/orders`.

## Verification

```powershell
python -m pytest -q
ruff check app tests scripts
ruff format --check app tests scripts
python scripts/run_scenario.py --list
```

The test suite uses temporary SQLite databases. It covers unit, integration, edge-case, and regression behavior, including atomic stock reservation and oversell prevention.

## Scenario workflow

Scenario metadata lives in `scenarios/manifest.yaml`. Use a disposable branch or worktree for mutations. The runner refuses a dirty working tree and refuses mutations unless explicitly passed `--allow-modify`:

```powershell
python scripts/run_scenario.py SAFE-001
python scripts/run_scenario.py RISK-002 --allow-modify --report reports/risk-002.json
```

The first command is safely skipped because mutation is not authorized. The second captures application tests and `nt check`; it does not claim NeverTwice detected a defect merely because the command succeeded. See `docs/scenarios.md`.

## NeverTwice integration

`scripts/nt_adapter.py` supports capability detection and evidence capture for `nt check`, `nt hooks install`, and `nt watch` without inventing command-line options. Git hook and pre-push behavior should be exercised in an isolated clone where the installed NeverTwice version documents those commands. CI does not require secrets or the CLI; unavailable integration is reported rather than passed.

## CI and containers

GitHub Actions runs linting, formatting, all tests, manifest validation, and uploads reports. Run the container with `docker compose up --build`.

## Limitations

The runner intentionally does not apply arbitrary source mutations automatically. This avoids overwriting user work and keeps each defect reproducible and reviewable. Scenarios requiring a NeverTwice rule or external monitoring integration are marked `NOT EVALUABLE` when that capability is absent.

## License

MIT. See `LICENSE`.

## Publishing

After reviewing local results, initialize and publish manually:

```powershell
git init
git add .
git commit -m "Build NeverTwice test lab"
git branch -M main
git remote add origin https://github.com/<owner>/nevertwice-test-lab.git
git push -u origin main
```
