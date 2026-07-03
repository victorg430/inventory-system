import requests

API = "http://127.0.0.1:5000/inventory"


def view_all():
    for item in requests.get(API).json():
        print(item)


def view_one():
    resp = requests.get(f"{API}/{input('Item ID: ')}")
    print(resp.json() if resp.status_code == 200 else "Item not found.")


def add_item():
    name = input("Product name: ")
    brand = input("Brand: ")
    try:
        price = float(input("Price: "))
        quantity = int(input("Quantity: "))
    except ValueError:
        print("Price/quantity must be numeric.")
        return
    payload = {"product_name": name, "brand": brand, "price": price, "quantity": quantity}
    print(requests.post(API, json=payload).json())


def update_item():
    item_id = input("Item ID to update: ")
    field = input("Field to update (price/quantity): ")
    if field not in ("price", "quantity"):
        print("Only price or quantity can be updated.")
        return
    try:
        value = float(input(f"New {field}: ")) if field == "price" else int(input(f"New {field}: "))
    except ValueError:
        print("Invalid value.")
        return
    resp = requests.patch(f"{API}/{item_id}", json={field: value})
    print(resp.json() if resp.status_code == 200 else "Item not found.")


def delete_item():
    print(requests.delete(f"{API}/{input('Item ID to delete: ')}").json())


def find_on_api():
    barcode = input("Barcode (blank to search by name): ").strip()
    resp = requests.get(f"{API}/lookup/barcode/{barcode}") if barcode \
        else requests.get(f"{API}/lookup/name/{input('Product name: ')}")

    if resp.status_code != 200:
        print("Product not found.")
        return
    print(resp.json())

    if barcode and input("Add to inventory? (y/n): ").lower() == "y":
        price = input("Price: ") or 0
        quantity = input("Quantity: ") or 0
        requests.post(f"{API}/fetch/{barcode}", json={"price": float(price), "quantity": int(quantity)})
        print("Added.")


MENU = {
    "1": ("View all items", view_all),
    "2": ("View one item", view_one),
    "3": ("Add new item", add_item),
    "4": ("Update price/quantity", update_item),
    "5": ("Delete item", delete_item),
    "6": ("Find item on OpenFoodFacts", find_on_api),
    "0": ("Exit", None),
}


def main():
    while True:
        print("\n--- Inventory CLI ---")
        for key, (label, _) in MENU.items():
            print(f"{key}. {label}")
        choice = input("Choose an option: ").strip()

        if choice == "0":
            break
        action = MENU.get(choice)
        if not action:
            print("Invalid option.")
            continue
        try:
            action[1]()
        except requests.ConnectionError:
            print("Could not reach the API. Is the Flask server running?")


if __name__ == "__main__":
    main()