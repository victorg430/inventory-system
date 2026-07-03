from unittest.mock import patch, Mock
import requests
from external_api import fetch_by_barcode, fetch_by_name


@patch("external_api.requests.get")
def test_fetch_by_barcode_success(mock_get):
    mock_resp = Mock()
    mock_resp.json.return_value = {
        "status": 1,
        "product": {"product_name": "Almond Milk", "brands": "Silk", "ingredients_text": "water, almonds"},
    }
    mock_get.return_value = mock_resp

    result = fetch_by_barcode("123")
    assert result["product_name"] == "Almond Milk"
    assert result["brand"] == "Silk"


@patch("external_api.requests.get")
def test_fetch_by_barcode_not_found(mock_get):
    mock_resp = Mock()
    mock_resp.json.return_value = {"status": 0}
    mock_get.return_value = mock_resp

    result = fetch_by_barcode("000")
    assert result is None


@patch("external_api.requests.get")
def test_fetch_by_barcode_request_fails(mock_get):
    mock_get.side_effect = requests.RequestException("network error")
    result = fetch_by_barcode("123")
    assert result is None


@patch("external_api.requests.get")
def test_fetch_by_name_success(mock_get):
    mock_resp = Mock()
    mock_resp.json.return_value = {
        "products": [{"product_name": "Oat Milk", "brands": "Oatly", "ingredients_text": "oats, water"}]
    }
    mock_get.return_value = mock_resp

    result = fetch_by_name("oat milk")
    assert result["product_name"] == "Oat Milk"


@patch("external_api.requests.get")
def test_fetch_by_name_no_results(mock_get):
    mock_resp = Mock()
    mock_resp.json.return_value = {"products": []}
    mock_get.return_value = mock_resp

    result = fetch_by_name("nonexistent")
    assert result is None