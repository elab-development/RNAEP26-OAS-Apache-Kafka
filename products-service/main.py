from fastapi import FastAPI, HTTPException
from typing import List
from models import Product

app = FastAPI(title="Products Service")

products_db = {
    1: Product(id=1, name="Laptop", price=1500.0, quantity=10),
    2: Product(id=2, name="Mouse", price=25.0, quantity=50)
}

@app.get("/products")
def get_products():
    return products_db

@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int):
    # Direktna i brza provera da li ključ postoji u rečniku
    if product_id in products_db:
        return products_db[product_id]
        
    raise HTTPException(status_code=404, detail="Product not found")

@app.put("/products/{product_id}/reduce", response_model=Product)
def reduce_quantity(product_id: int, quantity: int):
    # Prvo proveravamo da li proizvod postoji
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")
    
    product = products_db[product_id]
    
    if product.quantity < quantity:
        raise HTTPException(status_code=400, detail="Not enough stock")
        
    # Smanjujemo količinu i vraćamo proizvod
    product.quantity -= quantity
    return product