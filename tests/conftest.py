import sqlite3

import pytest
from fastapi.testclient import TestClient

from app.core.config import Settings, get_settings
from app.db.database import initialize_database
from app.main import app


@pytest.fixture
def client(tmp_path, monkeypatch):
    settings = Settings(database_url=f"sqlite:///{tmp_path / 'test.db'}")
    initialize_database(settings)
    app.dependency_overrides[get_settings] = lambda: settings
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def connection(tmp_path):
    connection = sqlite3.connect(tmp_path / "unit.db")
    connection.row_factory = sqlite3.Row
    connection.executescript("""
    CREATE TABLE products (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL,
    description TEXT NOT NULL, price_cents INTEGER NOT NULL, quantity INTEGER NOT NULL);
    CREATE TABLE orders (id INTEGER PRIMARY KEY AUTOINCREMENT, product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL, total_cents INTEGER NOT NULL);
    """)
    yield connection
    connection.close()
