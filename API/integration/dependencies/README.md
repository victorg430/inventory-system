# Inventory Management System

Flask REST API + CLI + React admin UI for store inventory, with product
lookup via the [OpenFoodFacts API](https://openfoodfacts.github.io/openfoodfacts-server/api/).

## Structure
```
app.py            # Flask REST API
external_api.py   # OpenFoodFacts integration
cli.py             # CLI frontend
frontend/          # React admin UI (Vite)
tests/              # Pytest suite
```

## Setup
```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python app.py                 # runs API on :5000
```

```bash
cd frontend && npm install && npm run dev   # runs UI on :5173
```

```bash
python cli.py                 # CLI (needs API running)
```

## API Endpoints
| Method | Route | Description |
|---|---|---|
| GET | `/inventory` | List all items |
| GET | `/inventory/<id>` | Get one item |
| POST | `/inventory` | Add item |
| PATCH | `/inventory/<id>` | Update item |
| DELETE | `/inventory/<id>` | Delete item |
| GET | `/inventory/lookup/barcode/<code>` | Look up product by barcode |
| GET | `/inventory/lookup/name/<name>` | Look up product by name |
| POST | `/inventory/fetch/<barcode>` | Fetch by barcode & add to inventory |

**Example:**
```bash
curl -X POST http://127.0.0.1:5000/inventory \
  -H "Content-Type: application/json" \
  -d '{"product_name": "Oat Milk", "brand": "Oatly", "price": 4.5, "quantity": 10}'
```

## CLI
```
1. View all items   4. Update price/quantity
2. View one item    5. Delete item
3. Add new item     6. Find item on OpenFoodFacts
```

## Tests
```bash
pytest tests/ -v
```
External calls are mocked, so tests run offline.

## Notes
Data is stored in-memory (`inventory` list in `app.py`) — resets on restart.