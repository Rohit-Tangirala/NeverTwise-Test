# Operations

Run the API locally with `uvicorn app.main:app --reload`, or with `docker compose up --build`. The health endpoint is `GET /api/health`. SQLite is selected with `SHOPLITE_DATABASE_URL` and is initialized during application startup.

NeverTwice integration is capability-driven. `scripts/nt_adapter.py` checks whether `nt` is on `PATH`, captures stdout, stderr, and exit code, and only extracts a verdict when the command output explicitly contains `SAFE`, `WARN`, or `BLOCK`. A successful process exit alone is not treated as detection evidence.
