# Architecture

ShopLite is a small FastAPI application with explicit boundaries:

- `app/core` owns environment-backed settings.
- `app/db` owns SQLite connections and schema initialization.
- `app/services` owns product and order business rules, including an atomic `BEGIN IMMEDIATE` stock reservation.
- `app/api` translates domain errors into HTTP responses.
- `tests` verifies behavior without relying on test order.
- `scenarios` describes controlled changes for NeverTwice evaluation.

The application deliberately has no dependency on NeverTwice. The adapter and scenario runner invoke the installed `nt` executable only when it is available.
