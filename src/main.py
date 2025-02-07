from fastapi import FastAPI

from src.books.routes import books_router

version = "v1"
app = FastAPI(
    title="Books API",
    description="REST API for book review web service",
    version=version,
)

app.include_router(prefix=f"/api/{version}/books",router=books_router,tags=["books"])

