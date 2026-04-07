from fastapi import FastAPI
from .database import init_db


app = FastAPI()

@app.get("/")
async def test():
    return {
        "status": "OK"
    }


@app.on_event("startup")
async def startup():
    init_db()
