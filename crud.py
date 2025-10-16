from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

user_details = {}
user_count = 1

class User(BaseModel):
    name: str
    age: int
    phone: int
    email: str

def create_user(user: User):
    global user_count
    user_details[user_count] = user
    user_count += 1
    return user

def get_all_users():
    if not user_details:
        raise HTTPException(status_code=404, detail="No users found")  
    else:
        return user_details
    
def create_new_user(user: User):
    return create_user(user)

def get_single_user(user_id: int):
    if not user_details:
        raise HTTPException(status_code=404, detail="No users found")  
    return user_details.get(user_id, "User not found")

def update_user(user_id: int, user: User):
    if user_id not in user_details:
        raise HTTPException(status_code=404, detail="User not found")
    user_details[user_id] = user
    return user

def delete_user(user_id: int):
    if user_id not in user_details:
        raise HTTPException(status_code=404, detail="User not found")
    del user_details[user_id]
    return {"message": "User deleted successfully"}