import pytest
from unittest.mock import patch
import app as app_module


@pytest.fixture
def client():
    app_module.app.config["TESTING"] = True
    app_module.inventory.clear()
    app_module.inventory.append({
        "id": 1, "product_name": "Almond Milk", "brand": "Silk",
        "barcode": "123", "ingredients_text": "water, almonds",
        "price": 3.99, "quantity": 25,
    })
    app_module.next_id = 2
    with app_module.app.test_client() as client:
        yield client


def test_get_all_items(client):
    resp = client.get("/inventory")
    assert resp.status_code == 200
    assert len(resp.get_json()) == 1


def test_get_single_item(client):
    resp = client.get("/inventory/1")
    assert resp.status_code == 200
    assert resp.get_json()["product_name"] == "Almond Milk"


def test_get_single_item_not_found(client):
    resp = client.get("/inventory/999")
    assert resp.status_code == 404


def test_add_item(client):
    payload = {"product_name": "Oat Milk", "brand": "Oatly", "price": 4.5, "quantity": 10}
    resp = client.post("/inventory", json=payload)
    assert resp.status_code == 201
    assert resp.get_json()["product_name"] == "Oat Milk"
    assert len(app_module.inventory) == 2


def test_add_item_missing_name(client):
    resp = client.post("/inventory", json={"brand": "Oatly"})
    assert resp.status_code == 400


def test_update_item(client):
    resp = client.patch("/inventory/1", json={"price": 5.99, "quantity": 30})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["price"] == 5.99
    assert data["quantity"] == 30


def test_update_item_not_found(client):
    resp = client.patch("/inventory/999", json={"price": 1})
    assert resp.status_code == 404


def test_delete_item(client):
    resp = client.delete("/inventory/1")
    assert resp.status_code == 200
    assert len(app_module.inventory) == 0


def test_delete_item_not_found(client):
    resp = client.delete("/inventory/999")
    assert resp.status_code == 404


@patch("app.fetch_by_barcode")
def test_lookup_barcode(mock_fetch, client):
    mock_fetch.return_value = {"product_name": "Oat Milk", "brand": "Oatly", "ingredients_text": "oats, water"}
    resp = client.get("/inventory/lookup/barcode/456")
    assert resp.status_code == 200
    assert resp.get_json()["product_name"] == "Oat Milk"


@patch("app.fetch_by_barcode")
def test_lookup_barcode_not_found(mock_fetch, client):
    mock_fetch.return_value = None
    resp = client.get("/inventory/lookup/barcode/000")
    assert resp.status_code == 404


@patch("app.fetch_by_barcode")
def test_fetch_and_add(mock_fetch, client):
    mock_fetch.return_value = {"product_name": "Oat Milk", "brand": "Oatly", "ingredients_text": "oats, water"}
    resp = client.post("/inventory/fetch/456", json={"price": 4.5, "quantity": 12})
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["product_name"] == "Oat Milk"
    assert data["price"] == 4.5
    assert len(app_module.inventory) == 2