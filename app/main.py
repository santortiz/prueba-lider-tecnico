import os
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routers.router import router

def lifespan():
    @asynccontextmanager
    async def lifespan_context(app: FastAPI):
        port = int(os.environ.get("PORT", 8000))
        host = os.environ.get("HOST", "localhost")
        print(f"API is starting on http://{host}:{port}")
        yield
        print("API is shutting down")
    return lifespan_context

app = FastAPI(title="Restaurant Reservation System", lifespan=lifespan())


app.include_router(router)

