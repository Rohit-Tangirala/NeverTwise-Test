import os
from functools import lru_cache
from pathlib import Path

from pydantic import BaseModel, Field


class Settings(BaseModel):
    app_name: str = "ShopLite"
    environment: str = "test"
    database_url: str = Field(default="sqlite:///./shoplite.db")
    log_level: str = "INFO"

    @property
    def database_path(self) -> str:
        prefix = "sqlite:///"
        if self.database_url.startswith(prefix):
            return self.database_url[len(prefix) :]
        return self.database_url


@lru_cache
def get_settings() -> Settings:
    return Settings(
        app_name=os.getenv("SHOPLITE_APP_NAME", "ShopLite"),
        environment=os.getenv("SHOPLITE_ENVIRONMENT", "test"),
        database_url=os.getenv("SHOPLITE_DATABASE_URL", "sqlite:///./shoplite.db"),
        log_level=os.getenv("SHOPLITE_LOG_LEVEL", "INFO"),
    )


def ensure_database_parent(settings: Settings) -> None:
    path = Path(settings.database_path)
    if str(path) != ":memory:":
        path.parent.mkdir(parents=True, exist_ok=True)
