from fastapi import FastAPI, status

from src.auth.routes import auth_router
from src.books.routes import books_router
from src.reviews.routes import reviews_router
from contextlib import asynccontextmanager
from src.db.main import init_db
from src.errors import InvlaidToken, create_exception_handler


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

app.add_exception_handler(
    InvlaidToken,
    create_exception_handler(
        status_code=status.HTTP_401_UNAUTHORIZED,
        initial_detail={
            "message": "Invalid or Expired Token",
            "error_code": "invalid_or_expired_token",
        },
    ),
)

app.include_router(prefix=f"/api/{version}/books", router=books_router, tags=["books"])
app.include_router(prefix=f"/api/{version}/auth", router=auth_router, tags=["auth"])
app.include_router(
    prefix=f"/api/{version}/reviews", router=reviews_router, tags=["reviews"]
)
