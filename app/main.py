import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.routers.router import router
from app.database import create_tables_if_not_exist

def lifespan():
    @asynccontextmanager
    async def lifespan_context(app: FastAPI):
        # Crear tablas automáticamente si no existen
        create_tables_if_not_exist()

        # Mensaje de inicio
        port = int(os.environ.get("PORT", 8000))
        host = os.environ.get("HOST", "localhost")
        print(f"API is started. Get docs on http://{host}:{port}/docs")

        yield

        # Mensaje de cierre
        print("API is shutting down")

    return lifespan_context

app = FastAPI(
    title="Restaurant Reservation System",
    lifespan=lifespan()
)

app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
