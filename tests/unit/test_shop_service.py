from app.models import OrderCreate, ProductCreate, ProductUpdate
from app.services.shop import InsufficientInventory, create_order, create_product, update_product


def test_update_product_preserves_unset_fields(connection):
    product = create_product(connection, ProductCreate(name="Desk", price_cents=2500, quantity=4))
    updated = update_product(connection, product.id, ProductUpdate(name="Standing Desk"))
    assert updated.name == "Standing Desk"
    assert updated.price_cents == 2500


def test_order_is_atomic_when_inventory_is_insufficient(connection):
    product = create_product(connection, ProductCreate(name="Cable", price_cents=500, quantity=1))
    try:
        create_order(connection, OrderCreate(product_id=product.id, quantity=2))
    except InsufficientInventory:
        pass
    assert (
        connection.execute("SELECT quantity FROM products WHERE id = ?", (product.id,)).fetchone()[
            0
        ]
        == 1
    )
