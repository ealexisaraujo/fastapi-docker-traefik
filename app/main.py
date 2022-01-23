from fastapi import FastAPI

app = FastAPI(title="FastAPI, Docker, and Traefik")


@app.get("/")
async def read_root():
    return {"hello": "world"}