import requests

def fetch_by_barcode(barcode):
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    response = requests.get(url)
    data = response.json()
    if data.get("status") == 1:
        product = data["product"]
        return {
            "product_name": product.get("product_name", ""),
            "brand": product.get("brands", ""),
            "ingredients_text": product.get("ingredients_text", ""),
            "price": 0.0,
            "quantity": 0
        }
    return None

def fetch_by_name(name):
    url = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={name}&json=1"
    response = requests.get(url)
    data = response.json()
    products = data.get("products", [])
    if products:
        product = products[0]
        return {
            "product_name": product.get("product_name", ""),
            "brand": product.get("brands", ""),
            "ingredients_text": product.get("ingredients_text", ""),
            "price": 0.0,
            "quantity": 0
        }
    return None
