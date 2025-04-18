from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi_cors import CORS
from app.core.database import init_db
from app.api.routers import users as user_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)
CORS(app)

app.include_router(
    user_router.router,
    prefix="/users",
    tags=["Users"]
)

@app.get("/", tags=["Root"])
async def read_root() -> dict:
    return {"message": "Welcome to your beanie powered app!"}
