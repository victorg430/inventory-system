import { useState, useEffect } from "react"

function App() {
  const [inventory, setInventory] = useState([])

  useEffect(() => {
    fetch("http://127.0.0.1:5000/inventory")
      .then(res => res.json())
      .then(data => setInventory(data))
  }, [])

  return (
    <div>
      <h1>Inventory System</h1>
      {inventory.map(item => (
        <div key={item.id}>
          <h3>{item.product_name}</h3>
          <p>Brand: {item.brand}</p>
          <p>Price: ${item.price}</p>
        </div>
      ))}
    </div>
  )
}

export default App
