import { useEffect, useState } from "react";
import { getItems, addItem, updateItem, deleteItem, lookupBarcode } from "./api";

export default function App() {
  const [items, setItems] = useState([]);
  const [form, setForm] = useState({ product_name: "", brand: "", price: "", quantity: "" });
  const [barcode, setBarcode] = useState("");

  const load = () => getItems().then(setItems);
  useEffect(load, []);

  const handleAdd = async (e) => {
    e.preventDefault();
    if (!form.product_name) return;
    await addItem({ ...form, price: +form.price || 0, quantity: +form.quantity || 0 });
    setForm({ product_name: "", brand: "", price: "", quantity: "" });
    load();
  };

  const handleUpdate = async (id, field, value) => {
    await updateItem(id, { [field]: +value || 0 });
    load();
  };

  const handleDelete = async (id) => {
    await deleteItem(id);
    load();
  };

  const handleLookup = async () => {
    const product = await lookupBarcode(barcode);
    if (!product) return alert("Product not found");
    setForm({ ...form, product_name: product.product_name, brand: product.brand });
  };

  return (
    <div style={{ maxWidth: 700, margin: "2rem auto", fontFamily: "sans-serif" }}>
      <h1>Inventory Admin</h1>

      <h2>Add Item</h2>
      <form onSubmit={handleAdd}>
        <input placeholder="Name" value={form.product_name}
          onChange={(e) => setForm({ ...form, product_name: e.target.value })} />
        <input placeholder="Brand" value={form.brand}
          onChange={(e) => setForm({ ...form, brand: e.target.value })} />
        <input placeholder="Price" value={form.price}
          onChange={(e) => setForm({ ...form, price: e.target.value })} />
        <input placeholder="Qty" value={form.quantity}
          onChange={(e) => setForm({ ...form, quantity: e.target.value })} />
        <button type="submit">Add</button>
      </form>

      <h2>Find on OpenFoodFacts</h2>
      <input placeholder="Barcode" value={barcode} onChange={(e) => setBarcode(e.target.value)} />
      <button onClick={handleLookup}>Lookup & fill form</button>

      <h2>Items</h2>
      <table border="1" cellPadding="6">
        <thead>
          <tr><th>Name</th><th>Brand</th><th>Price</th><th>Qty</th><th></th></tr>
        </thead>
        <tbody>
          {items.map((item) => (
            <tr key={item.id}>
              <td>{item.product_name}</td>
              <td>{item.brand}</td>
              <td>
                <input type="number" defaultValue={item.price} style={{ width: 70 }}
                  onBlur={(e) => handleUpdate(item.id, "price", e.target.value)} />
              </td>
              <td>
                <input type="number" defaultValue={item.quantity} style={{ width: 60 }}
                  onBlur={(e) => handleUpdate(item.id, "quantity", e.target.value)} />
              </td>
              <td><button onClick={() => handleDelete(item.id)}>Delete</button></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}