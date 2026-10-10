def test_confirmed_oversell_regression(client):
    product_id = client.post(
        "/api/products", json={"name": "Limited Edition", "price_cents": 1200, "quantity": 2}
    ).json()["id"]
    first = client.post("/api/orders", json={"product_id": product_id, "quantity": 2})
    second = client.post("/api/orders", json={"product_id": product_id, "quantity": 1})
    assert first.status_code == 201
    assert second.status_code == 409
    assert client.get(f"/api/products/{product_id}").json()["quantity"] == 0
