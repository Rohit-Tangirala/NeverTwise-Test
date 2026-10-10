# Validation Report

Date: 2026-10-10

## Results

- Dependency installation: passed with `python -m pip install -r requirements.txt`.
- Python syntax compilation: passed with `python -m compileall -q app scripts tests`.
- Automated tests: 15 passed with `python -m pytest -q`.
- Application coverage: 94% with `python -m pytest -q --cov=app --cov-report=term-missing`.
- Ruff lint: passed with `ruff check app tests scripts`.
- Ruff formatting: passed with `ruff format --check app tests scripts`.
- Scenario manifest: 27 scenarios parsed and listed by `python scripts/run_scenario.py --list`.
- Runner safety gate: `SAFE-001` correctly reported `SKIPPED` without `--allow-modify`.
- API smoke behavior: health, product creation, order creation, stock decrement, and oversell rejection are covered by passing integration tests.

## NeverTwice Integration

The local environment did not expose an `nt` executable. NeverTwice-specific detection runs are therefore `NOT EVALUABLE`, not passed. The adapter records command availability, stdout, stderr, exit code, and explicit verdict text when the executable is installed.

## Warnings

The test suite emits one upstream Starlette/httpx deprecation warning from the installed dependency combination. It does not affect test results.

## Reproduction

```powershell
python -m pip install -r requirements.txt
python -m pytest -q
ruff check app tests scripts
ruff format --check app tests scripts
python scripts/run_scenario.py --list
```
