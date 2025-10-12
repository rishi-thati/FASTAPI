from fastapi import FastAPI, HTTPException
app = FastAPI(title="User Management API")

users = {
    1: {
        "name": "rishi",
        "orders":{
          1: {"item": "laptop", "price": 50000, "order_id": 101},
          2: {"item": "mobile", "price": 20000, "order_id": 102}
    }
},
    2: {
        "name": "siddarth",
        "orders":{
          1: {"item": "tablet", "price": 30000, "order_id": 201},
          2: {"item": "smartwatch", "price": 15000, "order_id": 202}
    }
}
}

#Get method
@app.get("/user/{user_id}/order/{order_id}")
def user_root(user_id: int, order_id: int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="user id not found")
    if order_id not in users[user_id]["orders"]:
        raise HTTPException(status_code=404, detail="order id not found")
    return users[user_id]["orders"][order_id]