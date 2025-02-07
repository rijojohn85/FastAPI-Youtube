from fastapi import FastAPI

from src.books.routes import books_router

app = FastAPI()

app.include_router(prefix="/books",router=books_router)

