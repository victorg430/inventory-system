import argparse, sys, requests, json

BASE = "http://127.0.0.1:5000"

def show(resp):
    print(json.dumps(resp.json(), indent=2))

def cmd_list(_):
    show(requests.get(f"{BASE}/inventory"))

def cmd_get(args):
    show(requests.get(f"{BASE}/inventory/{args.id}"))

def cmd_add(_):
    name = input("Product name: ").strip()
    if not name:
        print("Name required."); sys.exit(1)
    show(requests.post(f"{BASE}/inventory", json={
        "product_name": name,
        "brands": input("Brand: ").strip(),
        "category": input("Category: ").strip(),
        "barcode": input("Barcode: ").strip(),
        "quantity": int(input("Quantity [0]: ").strip() or 0),
        "price": float(input("Price [0.00]: ").strip() or 0),
    }))

def cmd_update(args):
    fields = {}
    for key, label in [("product_name","Name"),("brands","Brand"),("category","Category"),("barcode","Barcode")]:
        val = input(f"{label}: ").strip()
        if val: fields[key] = val
    qty = input("Quantity: ").strip()
    if qty: fields["quantity"] = int(qty)
    price = input("Price: ").strip()
    if price: fields["price"] = float(price)
    show(requests.patch(f"{BASE}/inventory/{args.id}", json=fields))

def cmd_delete(args):
    if input(f"Delete item {args.id}? (yes/no): ").strip() == "yes":
        show(requests.delete(f"{BASE}/inventory/{args.id}"))

def cmd_fetch(args):
    if not args.barcode and not args.name:
        print("Need --barcode or --name"); sys.exit(1)
    params = {"barcode": args.barcode} if args.barcode else {"name": args.name}
    if args.add: params["add"] = "true"
    show(requests.get(f"{BASE}/fetch-product", params=params))

parser = argparse.ArgumentParser()
sub = parser.add_subparsers(dest="command")
sub.add_parser("list")
sub.add_parser("add")
for cmd in ("get", "update", "delete"):
    sub.add_parser(cmd).add_argument("id", type=int)
p = sub.add_parser("fetch")
p.add_argument("--barcode"); p.add_argument("--name"); p.add_argument("--add", action="store_true")

args = parser.parse_args()
if not args.command:
    parser.print_help(); sys.exit(0)

try:
    {"list": cmd_list, "get": cmd_get, "add": cmd_add, "update": cmd_update, "delete": cmd_delete, "fetch": cmd_fetch}[args.command](args)
except requests.exceptions.ConnectionError:
    print("Start the server first: python app.py")