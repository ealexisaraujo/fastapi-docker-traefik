from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Body, FastAPI, Path, Query

from app.db import Location, Person, database


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not database.is_connected:
        await database.connect()

    try:
        yield
    finally:
        if database.is_connected:
            await database.disconnect()


app = FastAPI(title="FastAPI, Docker, and Traefik", lifespan=lifespan)


@app.get("/")
async def read_root():
    return {"hello": "world"}


@app.post("/person/new")
async def create_person(person: Annotated[Person, Body()]):
    return person


@app.get("/person/detail")
async def show_person(
    age: Annotated[
        str,
        Query(
            title="Person's age",
            description="The age of the person you are looking for",
            examples=["25"],
        ),
    ],
    name: Annotated[
        str | None,
        Query(
            min_length=3,
            max_length=10,
            title="Person's name",
            description="The name of the person you are looking for",
            examples=["John"],
        ),
    ] = None,
):
    return {"name": name, "age": age}


@app.get("/person/detail/{person_id}")
async def show_person_detail(
    person_id: Annotated[
        int,
        Path(
            gt=0,
            title="Person ID",
            description="The ID of the person to show",
            examples=[1],
        ),
    ],
):
    return {"id": person_id}


# Validations: Request Body
@app.put("/person/{person_id}")
async def update_person(
    person_id: Annotated[
        int,
        Path(
            gt=0,
            title="Person ID",
            description="The ID of the person to update",
            examples=[1],
        ),
    ],
    person: Annotated[
        Person,
        Body(
            title="Person",
            description="The person to update",
        ),
    ],
    location: Annotated[Location, Body()],
):
    results = person.model_dump()
    results.update(location.model_dump())
    return results
