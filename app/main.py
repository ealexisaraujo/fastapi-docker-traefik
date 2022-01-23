from fastapi import FastAPI

app = FastAPI(title="FastAPI, Docker, and Traefik")


@app.get("/")
async def read_root():
    return {"hello": "world"}

@app.post("/person/new")
async def create_person(name: str, age: int):
    return {"name": name, "age": age}
