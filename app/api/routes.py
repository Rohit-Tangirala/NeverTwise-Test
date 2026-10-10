import logging
import sqlite3
from collections.abc import Generator

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.config import Settings, get_settings
from app.db.database import connection_for
from app.models import Order, OrderCreate, Product, ProductCreate, ProductUpdate
from app.services.shop import (
    InsufficientInventory,
    ProductNotFound,
    create_order,
    create_product,
    get_product,
    list_products,
    update_product,
)

logger = logging.getLogger(__name__)
router = APIRouter()


def get_connection(
    settings: Settings = Depends(get_settings),
) -> Generator[sqlite3.Connection, None, None]:
    yield from connection_for(settings)


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/products", response_model=Product, status_code=status.HTTP_201_CREATED)
def post_product(
    payload: ProductCreate, connection: sqlite3.Connection = Depends(get_connection)
) -> Product:
    logger.info("creating product", extra={"product_name": payload.name})
    return create_product(connection, payload)


@router.get("/products", response_model=list[Product])
def get_products(connection: sqlite3.Connection = Depends(get_connection)) -> list[Product]:
    return list_products(connection)


@router.get("/products/{product_id}", response_model=Product)
def get_one_product(
    product_id: int, connection: sqlite3.Connection = Depends(get_connection)
) -> Product:
    try:
        return get_product(connection, product_id)
    except ProductNotFound as error:
        raise HTTPException(status_code=error.status_code, detail=str(error)) from error


@router.patch("/products/{product_id}", response_model=Product)
def patch_product(
    product_id: int,
    payload: ProductUpdate,
    connection: sqlite3.Connection = Depends(get_connection),
) -> Product:
    try:
        return update_product(connection, product_id, payload)
    except ProductNotFound as error:
        raise HTTPException(status_code=error.status_code, detail=str(error)) from error


@router.post("/orders", response_model=Order, status_code=status.HTTP_201_CREATED)
def post_order(
    payload: OrderCreate, connection: sqlite3.Connection = Depends(get_connection)
) -> Order:
    try:
        return create_order(connection, payload)
    except (ProductNotFound, InsufficientInventory) as error:
        raise HTTPException(status_code=error.status_code, detail=str(error)) from error
