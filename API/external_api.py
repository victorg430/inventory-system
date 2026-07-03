import requests

BASE_URL = "https://world.openfoodfacts.org"


def fetch_by_barcode(barcode):
    try:
        resp = requests.get(f"{BASE_URL}/api/v2/product/{barcode}.json", timeout=5)
        data = resp.json()
    except requests.RequestException:
        return None

    if data.get("status") != 1:
        return None

    p = data.get("product", {})
    return {"product_name": p.get("product_name", "Unknown"),
            "brand": p.get("brands", ""), "ingredients_text": p.get("ingredients_text", "")}


def fetch_by_name(name):
    params = {"search_terms": name, "search_simple": 1, "json": 1, "page_size": 1}
    try:
        resp = requests.get(f"{BASE_URL}/cgi/search.pl", params=params, timeout=5)
        products = resp.json().get("products", [])
    except requests.RequestException:
        return None

    if not products:
        return None

    p = products[0]
    return {"product_name": p.get("product_name", "Unknown"),
            "brand": p.get("brands", ""), "ingredients_text": p.get("ingredients_text", "")}