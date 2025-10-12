from fastapi import FastAPI
app = FastAPI()

#Get method
@app.get("/")
def root_url():
    return {"message":"Hello World!"}

#Get method with parameters
@app.get("/sub")
def internal_url():
    return {"message":"hi"}
