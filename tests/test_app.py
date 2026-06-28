import pytest
from unittest.mock import patch, MagicMock
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import app as app_module
from app import app

SEED = [
    {"id": 1, "product_name": "Almond Milk", "brands": "Silk", "barcode": "111", "quantity": 50, "price": 4.99, "category": "Beverages"},
    {"id": 2, "product_name": "Cheerios", "brands": "GM", "barcode": "222", "quantity": 20, "price": 3.49, "category": "Cereals"},
]
MOCK = {"status": 1, "product": {"code": "111", "product_name": "Almond Milk", "brands": "Silk", "ingredients_text": "", "categories": "Beverages"}}

@pytest.fixture(autouse=True)
def reset():
    app_module.inventory.clear()
    app_module.inventory.extend([dict(i) for i in SEED])
    app_module.next_id = 3

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c

def test_get_all(client):
    assert len(client.get("/inventory").get_json()) == 2

def test_get_one(client):
    assert client.get("/inventory/1").get_json()["product_name"] == "Almond Milk"

def test_get_one_not_found(client):
    assert client.get("/inventory/99").status_code == 404

def test_create(client):
    r = client.post("/inventory", json={"product_name": "Oat Milk"})
    assert r.status_code == 201 and r.get_json()["id"] == 3

def test_create_missing_name(client):
    assert client.post("/inventory", json={"brands": "X"}).status_code == 400

def test_create_defaults(client):
    d = client.post("/inventory", json={"product_name": "Test"}).get_json()
    assert d["quantity"] == 0 and d["price"] == 0.0

def test_update(client):
    client.patch("/inventory/1", json={"price": 9.99})
    assert client.get("/inventory/1").get_json()["price"] == 9.99

def test_update_not_found(client):
    assert client.patch("/inventory/99", json={"price": 1}).status_code == 404

def test_update_ignores_unknown(client):
    client.patch("/inventory/1", json={"hacked": "bad"})
    assert "hacked" not in client.get("/inventory/1").get_json()

def test_delete(client):
    client.delete("/inventory/1")
    assert client.get("/inventory/1").status_code == 404

def test_delete_not_found(client):
    assert client.delete("/inventory/99").status_code == 404

def test_fetch_no_params(client):
    assert client.get("/fetch-product").status_code == 400

@patch("app.requests.get")
def test_fetch_by_barcode(mock_get, client):
    mock_get.return_value = MagicMock(json=lambda: MOCK)
    assert client.get("/fetch-product?barcode=111").status_code == 200

@patch("app.requests.get")
def test_fetch_not_found(mock_get, client):
    mock_get.return_value = MagicMock(json=lambda: {"status": 0})
    assert client.get("/fetch-product?barcode=000").status_code == 404

@patch("app.requests.get")
def test_fetch_and_add(mock_get, client):
    mock_get.return_value = MagicMock(json=lambda: MOCK)
    r = client.get("/fetch-product?barcode=111&add=true")
    assert r.status_code == 201 and len(app_module.inventory) == 3