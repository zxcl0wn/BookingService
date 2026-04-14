from fastapi import FastAPI
from .database import init_db
from .routes.booking_route import router as booking_router
from .routes.room_route import router as room_router
from .routes.review_route import router as review_router
from .routes.tag_route import router as tag_router
from .routes.user_route import router as user_router
from .auth.routes.auth_router import router as auth_router


app = FastAPI()

@app.get("/")
async def test():
    return {
        "status": "OK"
    }

app.include_router(booking_router)
app.include_router(room_router)
app.include_router(review_router)
app.include_router(tag_router)
app.include_router(user_router)
app.include_router(auth_router)


@app.on_event("startup")
async def startup():
    init_db()
