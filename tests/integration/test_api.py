def test_product_order_flow(client):
    created = client.post(
        "/api/products", json={"name": "Keyboard", "price_cents": 4999, "quantity": 3}
    )
    assert created.status_code == 201
    product_id = created.json()["id"]

    order = client.post("/api/orders", json={"product_id": product_id, "quantity": 2})
    assert order.status_code == 201
    assert order.json()["total_cents"] == 9998
    assert client.get(f"/api/products/{product_id}").json()["quantity"] == 1


def test_overselling_is_rejected_without_mutating_stock(client):
    product_id = client.post(
        "/api/products", json={"name": "Mouse", "price_cents": 1000, "quantity": 1}
    ).json()["id"]
    response = client.post("/api/orders", json={"product_id": product_id, "quantity": 2})
    assert response.status_code == 409
    assert client.get(f"/api/products/{product_id}").json()["quantity"] == 1


def test_health_endpoint(client):
    assert client.get("/api/health").json() == {"status": "ok"}
