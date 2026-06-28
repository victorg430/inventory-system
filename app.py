from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

inventory = [
    {"id": 1, "product_name": "Almond Milk", "brands": "Silk", "barcode": "0041196896005", "quantity": 50, "price": 4.99, "category": "Beverages"},
    {"id": 2, "product_name": "Cheerios", "brands": "General Mills", "barcode": "016000275287", "quantity": 120, "price": 3.49, "category": "Cereals"},
    {"id": 3, "product_name": "Coca-Cola", "brands": "Coca-Cola", "barcode": "070038594581", "quantity": 200, "price": 1.99, "category": "Beverages"},
]
next_id = 4

def find_item(item_id):
    return next((i for i in inventory if i["id"] == item_id), None)

@app.get("/inventory")
def get_all():
    return jsonify(inventory), 200

@app.get("/inventory/<int:item_id>")
def get_one(item_id):
    item = find_item(item_id)
    return jsonify(item) if item else (jsonify({"error": "Not found"}), 404)

@app.post("/inventory")
def create_item():
    global next_id
    data = request.get_json()
    if not data or "product_name" not in data:
        return jsonify({"error": "product_name required"}), 400
    item = {"id": next_id, "product_name": data["product_name"], "brands": data.get("brands", ""), "barcode": data.get("barcode", ""), "quantity": data.get("quantity", 0), "price": data.get("price", 0.0), "category": data.get("category", "Uncategorized")}
    inventory.append(item)
    next_id += 1
    return jsonify(item), 201

@app.patch("/inventory/<int:item_id>")
def update_item(item_id):
    item = find_item(item_id)
    if not item:
        return jsonify({"error": "Not found"}), 404
    data = request.get_json()
    for key in {"product_name", "brands", "barcode", "quantity", "price", "category"}:
        if key in data:
            item[key] = data[key]
    return jsonify(item), 200

@app.delete("/inventory/<int:item_id>")
def delete_item(item_id):
    item = find_item(item_id)
    if not item:
        return jsonify({"error": "Not found"}), 404
    inventory.remove(item)
    return jsonify({"message": f"Item {item_id} deleted"}), 200

@app.get("/fetch-product")
def fetch_product():
    global next_id
    barcode = request.args.get("barcode")
    name = request.args.get("name")
    auto_add = request.args.get("add") == "true"

    if barcode:
        data = requests.get(f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json", timeout=8).json()
        product = data.get("product") if data.get("status") == 1 else None
    elif name:
        results = requests.get("https://world.openfoodfacts.org/cgi/search.pl", params={"search_terms": name, "json": 1, "page_size": 1}, timeout=8).json()
        product = results.get("products", [None])[0]
    else:
        return jsonify({"error": "Provide ?barcode= or ?name="}), 400

    if not product:
        return jsonify({"error": "Product not found"}), 404

    result = {"barcode": product.get("code", ""), "product_name": product.get("product_name", "Unknown"), "brands": product.get("brands", ""), "category": product.get("categories", "").split(",")[0].strip()}

    if auto_add:
        item = {**result, "id": next_id, "quantity": 0, "price": 0.0}
        inventory.append(item)
        next_id += 1
        return jsonify({"message": "Added", "item": item}), 201

    return jsonify(result), 200

if __name__ == "__main__":
    app.run(debug=True)