from fastapi import FastAPI, HTTPException
app = FastAPI()

#Get method
@app.get("/")
def root_url():
    return {"message":"Hello World!"}

#Get method with path parameter
@app.get("/sub")
def internal_url():
    return {"message":"hi"}

users = {
    1:{"name":"rishi"},
    2:{"name":"siddarth"}
}

@app.get("/user/{user_id}")
def get_users(user_id:int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="user id not found")
    return users[user_id]

