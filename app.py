from flask import Flask, jsonify, request
from flask_cors import CORS
from external_api import fetch_by_barcode, fetch_by_name

app = Flask(__name__)
CORS(app)

inventory = [
    {"id": 1, "product_name": "Almond Milk", "brand": "Silk", "barcode": "123",
     "ingredients_text": "water, almonds", "price": 3.99, "quantity": 25}
]
next_id = 2


def find_item(item_id):
    return next((i for i in inventory if i["id"] == item_id), None)


@app.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(inventory)


@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = find_item(item_id)
    return (jsonify(item), 200) if item else (jsonify({"error": "not found"}), 404)


@app.route("/inventory", methods=["POST"])
def add_item():
    global next_id
    data = request.get_json(silent=True) or {}
    if not data.get("product_name"):
        return jsonify({"error": "product_name is required"}), 400

    item = {"id": next_id, "product_name": data.get("product_name"),
            "brand": data.get("brand", ""), "barcode": data.get("barcode", ""),
            "ingredients_text": data.get("ingredients_text", ""),
            "price": data.get("price", 0.0), "quantity": data.get("quantity", 0)}
    inventory.append(item)
    next_id += 1
    return jsonify(item), 201


@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_item(item_id):
    item = find_item(item_id)
    if not item:
        return jsonify({"error": "not found"}), 404
    data = request.get_json(silent=True) or {}
    item.update({k: v for k, v in data.items() if k in item})
    return jsonify(item)


@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    item = find_item(item_id)
    if not item:
        return jsonify({"error": "not found"}), 404
    inventory.remove(item)
    return jsonify({"message": f"item {item_id} deleted"})


@app.route("/inventory/lookup/barcode/<barcode>", methods=["GET"])
def lookup_barcode(barcode):
    result = fetch_by_barcode(barcode)
    return (jsonify(result), 200) if result else (jsonify({"error": "not found"}), 404)


@app.route("/inventory/lookup/name/<name>", methods=["GET"])
def lookup_name(name):
    result = fetch_by_name(name)
    return (jsonify(result), 200) if result else (jsonify({"error": "not found"}), 404)


@app.route("/inventory/fetch/<barcode>", methods=["POST"])
def fetch_and_add(barcode):
    global next_id
    result = fetch_by_barcode(barcode)
    if not result:
        return jsonify({"error": "not found on OpenFoodFacts"}), 404

    data = request.get_json(silent=True) or {}
    item = {"id": next_id, "product_name": result["product_name"], "brand": result["brand"],
            "barcode": barcode, "ingredients_text": result["ingredients_text"],
            "price": data.get("price", 0.0), "quantity": data.get("quantity", 0)}
    inventory.append(item)
    next_id += 1
    return jsonify(item), 201


if __name__ == "__main__":
    app.run(debug=True)