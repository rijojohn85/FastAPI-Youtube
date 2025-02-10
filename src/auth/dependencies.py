from datetime import datetime

from fastapi.security import HTTPBearer
from fastapi import Request, status, HTTPException
from src.utils import logger


from .utils import decode_token
from ..db.redis import token_in_blocklist


class TokenBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    def verify_token_data(self, token):
        raise NotImplementedError("This method is not implemented")

    async def __call__(self, request: Request):
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
