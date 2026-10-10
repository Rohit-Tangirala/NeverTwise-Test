import pytest
from pydantic import ValidationError

from app.models import OrderCreate, ProductCreate


@pytest.mark.parametrize(
    "payload",
    [
        {"name": "", "price_cents": 1, "quantity": 1},
        {"name": "A", "price_cents": -1, "quantity": 1},
        {"name": "A", "price_cents": 1, "quantity": -1},
        {"name": "A", "price_cents": 1, "quantity": 0, "description": None},
    ],
)
def test_invalid_product_payloads_are_rejected(payload):
    with pytest.raises(ValidationError):
        ProductCreate.model_validate(payload)


def test_zero_or_negative_order_quantity_is_rejected():
    with pytest.raises(ValidationError):
        OrderCreate(product_id=1, quantity=0)
    with pytest.raises(ValidationError):
        OrderCreate(product_id=1, quantity=-1)


def test_missing_product_is_a_not_found_response(client):
    response = client.get("/api/products/999999")
    assert response.status_code == 404
