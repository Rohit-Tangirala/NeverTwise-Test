import logging

from fastapi import FastAPI

from app.api.routes import router
from app.core.config import get_settings
from app.db.database import initialize_database

settings = get_settings()
logging.basicConfig(level=settings.log_level, format="%(levelname)s %(name)s %(message)s")
initialize_database(settings)

app = FastAPI(title=settings.app_name, version="1.0.0")
app.include_router(router, prefix="/api")
