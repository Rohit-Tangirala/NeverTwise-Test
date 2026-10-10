import sqlite3
from collections.abc import Generator

from app.core.config import Settings, ensure_database_parent

SCHEMA = """
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    price_cents INTEGER NOT NULL CHECK (price_cents >= 0),
    quantity INTEGER NOT NULL CHECK (quantity >= 0)
);
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    total_cents INTEGER NOT NULL CHECK (total_cents >= 0),
    FOREIGN KEY(product_id) REFERENCES products(id)
);
"""


def connect(settings: Settings) -> sqlite3.Connection:
    ensure_database_parent(settings)
    connection = sqlite3.connect(settings.database_path, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database(settings: Settings) -> None:
    with connect(settings) as connection:
        connection.executescript(SCHEMA)


def connection_for(settings: Settings) -> Generator[sqlite3.Connection, None, None]:
    connection = connect(settings)
    try:
        yield connection
    finally:
        connection.close()
