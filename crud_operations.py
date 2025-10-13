from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

user_details={}
count_id=1

class user(BaseModel):
    name: str
    age: int
    phone: int
    email: str

def create_user(user: user):
    global count_id
    user_details[count_id] = user
    count_id += 1
    return user

@app.get("/users")
def get_users():
    if not user_details:
        raise HTTPException(status_code=404, detail="No users found")
    return user_details

@app.get("/user/{user_id}")
def get_single_user(user_id: int):
    if not user_details:
        raise HTTPException(status_code=404, detail="No users found")  
    return user_details.get(user_id, "User not found")

@app.put("/user/{user_id}")
def update_user(user_id: int, user:user):
    if user_id not in user_details:
        raise HTTPException(status_code=404, detail="User not found")
    user_details[user_id] = user
    return user

@app.post("/create")
def create_new_user(user: user):
    return create_user(user)

@app.delete("/user/{user_id}")
def delete_user(user_id: int):
    if user_id not in user_details:
        raise HTTPException(status_code=404, detail="User not found")
    del user_details[user_id]
    return {"message": "User deleted successfully"}