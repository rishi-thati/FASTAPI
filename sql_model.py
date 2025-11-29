# ...existing code...
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel  
from sql_model import SQLModel, create_engine

DATABASE_URL = "sqlite:///./test.db"
# ...existing code...

from typing import Optional, List
from sqlmodel import Field, Session, select
from sqlmodel import SQLModel as _SQLModel, create_engine as _create_engine

# Use the real sqlmodel package (name differs from this file: sql_model.py)
SQLModel = _SQLModel
create_engine = _create_engine

# Engine with SQLite-specific option for use in threaded apps (FastAPI)
engine = create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})

class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    price: float = 0.0

class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: Optional[float] = 0.0

app = FastAPI(title="Simple SQLModel CRUD")

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/items/", response_model=Item, status_code=201)
def create_item(item_in: ItemCreate):
    item = Item.from_orm(item_in) if hasattr(Item, "from_orm") else Item(**item_in.dict())
    with Session(engine) as session:
        session.add(item)
        session.commit()
        session.refresh(item)
        return item

@app.get("/items/", response_model=List[Item])
def read_items():
    with Session(engine) as session:
        statement = select(Item)
        results = session.exec(statement).all()
        return results

@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int):
    with Session(engine) as session:
        item = session.get(Item, item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        return item

@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item_in: ItemCreate):
    with Session(engine) as session:
        item = session.get(Item, item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        item_data = item_in.dict(exclude_unset=True)
        for key, value in item_data.items():
            setattr(item, key, value)
        session.add(item)
        session.commit()
        session.refresh(item)
        return item

@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int):
    with Session(engine) as session:
        item = session.get(Item, item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        session.delete(item)
        session.commit()
        return None