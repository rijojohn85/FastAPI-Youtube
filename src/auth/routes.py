from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import datetime, timedelta

from starlette.responses import JSONResponse

from src.auth.schemas import CreateUserPayload, UserSchema
from ..db.models import User
from src.auth.service import UserService
from src.db.main import get_session
from src.utils import logger
from src.auth.schemas import UserLoginPayload
from .dependencies import (
    RefreshTokenBearer,
    AccessTokenBearer,
    get_current_user,  # type: ignore
    RoleChecker,
)
from .utils import create_access_token
from ..db.redis import add_jti_to_blocklist

auth_router = APIRouter()
user_service = UserService()
role_checker = RoleChecker(allowed_roles=["admin", "user"])


@auth_router.post(
    "/sign-up",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
)
async def sign_up(
    payload: CreateUserPayload, session: AsyncSession = Depends(get_session)
):
    try:
        user = await user_service.create_user(payload, session)
    except HTTPException as err:
        raise err
    except Exception as e:
        logger.error(str(e))
        raise e
    return user


@auth_router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    payload: UserLoginPayload, session: AsyncSession = Depends(get_session)
):
    try:
        login_data = await user_service.login_user(payload, session)
    except HTTPException as err:
        raise err
    except Exception as e:
        logger.error(str(e))
        raise e
    return login_data


@auth_router.get(
    "/refresh-token",
)
async def refresh_token(
    token_details: dict = Depends(RefreshTokenBearer()),
):
    expiry_timestamp = token_details["exp"]
    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(
            data=token_details["user"], expires_delta=timedelta(minutes=60)
        )
        return JSONResponse({"access_token": new_access_token})
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid or expired token, login again.",
    )


@auth_router.get("/me", response_model=UserSchema)
async def get_current_user(
    user=Depends(get_current_user), _: bool = Depends(role_checker)
):
    return user


@auth_router.get("/logout")
async def logout(token_details: dict = Depends(AccessTokenBearer())):
    jti = token_details["jti"]
    add_jti_to_blocklist(jti)
    return JSONResponse(
        {
            "message": "Successfully logged out.",
        },
        status_code=status.HTTP_200_OK,
    )
