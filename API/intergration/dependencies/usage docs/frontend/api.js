const BASE = "http://127.0.0.1:5000/inventory";

export const getItems = () => fetch(BASE).then((r) => r.json());

export const addItem = (item) =>
  fetch(BASE, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(item),
  }).then((r) => r.json());

export const updateItem = (id, fields) =>
  fetch(`${BASE}/${id}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(fields),
  }).then((r) => r.json());

export const deleteItem = (id) =>
  fetch(`${BASE}/${id}`, { method: "DELETE" }).then((r) => r.json());

export const lookupBarcode = (barcode) =>
  fetch(`${BASE}/lookup/barcode/${barcode}`).then((r) => (r.ok ? r.json() : null));