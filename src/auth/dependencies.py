from datetime import datetime
from typing import Any, List

from fastapi.security import HTTPBearer
from fastapi import Request, status, HTTPException, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from ..db.models import User
from src.utils import logger
from src.db.main import get_session
from src.auth.service import UserService


from .utils import decode_token
from ..db.redis import token_in_blocklist

user_service = UserService()


class TokenBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    def verify_token_data(self, token_data: dict):  # pyright: ignore
        raise NotImplementedError("This method is not implemented")

    async def __call__(self, request: Request) -> dict[Any, Any]:  # type: ignore
        authorization = request.headers.get("Authorization")
        if not authorization:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization header is missing",
            )
        scheme, token = authorization.split()
        if not scheme.lower() == "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization header must start with 'Bearer'",
            )
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token is missing",
            )
        try:
            user_data = decode_token(token)
        except Exception as e:
            logger.error(e)
            raise e
        if not user_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token is invalid or expired",
            )
        if token_in_blocklist(user_data["jti"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token is invalid or expired. Please log in again.",
            )

        self.verify_token_data(user_data)
        return user_data


class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Please provide an access token",
            )
        if datetime.fromtimestamp(token_data["exp"]) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"message": "Token is expired", "type": "TokenExpiration"},
            )


class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Please provide an refresh token",
            )
        if datetime.fromtimestamp(token_data["exp"]) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"message": "Token is expired", "type": "TokenExpiration"},
            )


async def get_current_user(
    token_details: dict = Depends(AccessTokenBearer()),
    session: AsyncSession = Depends(get_session),
) -> User:
    username = token_details["user"]["username"]
    user: User | None = await user_service.get_user_by_username(
        username, session=session
    )
    return user  # type: ignore


class RoleChecker:
    def __init__(self, allowed_roles: List[str]) -> None:
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)) -> bool:
        if current_user.role in self.allowed_roles:
            return True

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User role does not have permission for this end point",
        )
