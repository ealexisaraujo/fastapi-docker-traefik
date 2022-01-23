from typing import Optional
from fastapi import Body, FastAPI, Query
from app.db import database, Person

app = FastAPI(title="FastAPI, Docker, and Traefik")


@app.get("/")
async def read_root():
    return {"hello": "world"}

@app.on_event("startup")
async def startup_event():
  if not database.is_connected:
    await database.connect()

@app.on_event("shutdown")
async def shutdown_event():
  if database.is_connected:
    await database.disconnect()

@app.post("/person/new")
async def create_person(person: Person = Body(...)):
    return person

@app.get("/person/detail")
async def show_person(
    name: Optional[str] = Query(None, min_length=3, max_length=10), 
    age: str = Query(...)
    ):
    return {"name": name, "age": age}
