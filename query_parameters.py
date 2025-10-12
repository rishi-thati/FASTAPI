from fastapi import FastAPI
from typing import Optional

app = FastAPI()

products = [
    {"id": 1, "name": "Laptop", "category": "Electronics", "price": 50000},
    {"id": 2, "name": "Mobile", "category": "Electronics", "price": 20000},
    {"id": 3, "name": "Pen", "category": "Stationary", "price": 100},
    {"id": 4, "name": "Notebook", "category": "Stationary", "price": 200}
]


@app.get("/products/")
def get_products(category: Optional[str] = None, max_price: Optional[float] = None):
    filtered_products = products
    if category:
        filtered_products = [product for product in filtered_products if product["category"].lower() == category.lower()]
    if max_price is not None:
        filtered_products = [product for product in filtered_products if product["price"] <= max_price]
    return filtered_products