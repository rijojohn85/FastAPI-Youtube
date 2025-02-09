from fastapi import FastAPI

from src.auth.routes import auth_router
from src.books.routes import books_router
from contextlib import asynccontextmanager
from src.db.main import init_db


@asynccontextmanager
async def life_span(app: FastAPI):
    await init_db()
    print("server is running.")
    yield
    print("server has stopped.")


version = "v1"
app = FastAPI(
    title="Books API",
    description="REST API for book review web service",
    version=version,
    # lifespan=life_span,
)

app.include_router(prefix=f"/api/{version}/books", router=books_router, tags=["books"])
app.include_router(prefix=f"/api/{version}/auth", router=auth_router, tags=["auth"])
