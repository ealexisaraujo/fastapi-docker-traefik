from typing import Optional

from fastapi import Body, FastAPI, Path, Query

from app.db import Location, Person, database

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
    name: Optional[str] = Query(
        None,
        min_length=3,
        max_length=10,
        title="Person's name",
        description="The name of the person you are looking for",
        example={
            "name": "John",
        },
    ),
    age: str = Query(
        ...,
        title="Person's age",
        description="The age of the person you are looking for",
        example={"age": "25"},
    ),
):
    return {"name": name, "age": age}


@app.get("/person/detail/{person_id}")
async def show_person_detail(
    person_id: int = Path(
        ...,
        gt=0,
        title="Person ID",
        description="The ID of the person to show",
        example={"person_id": 1},
    )
):
    return {"id": person_id}


# Validations: Request Body
@app.put("/person/{person_id}")
async def update_person(
    person_id: int = Path(
        ...,
        gt=0,
        title="Person ID",
        description="The ID of the person to update",
        example={"person_id": 1},
    ),
    person: Person = Body(
        ...,
        title="Person",
        description="The person to update",
    ),
    location: Location = Body(...),
):
    results = person.dict()
    results.update(location.dict())
    return results
