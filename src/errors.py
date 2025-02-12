from typing import Any, Callable
from fastapi.requests import Request
from fastapi.responses import JSONResponse


class BookExceptions(Exception):
    """Base class for all custom errors"""

    pass


class InvlaidToken(BookExceptions):
    """User has provided an invalid or expired token"""

    pass


def create_exception_handler(
    status_code: int, initial_detail: Any
) -> Callable[[Request, Exception], JSONResponse]:
    async def exception_handler(request: Request, exception: BookExceptions):
        return JSONResponse(content=initial_detail, status_code=status_code)

    return exception_handler  # type: ignore
