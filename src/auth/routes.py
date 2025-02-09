from http.client import HTTPException

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.schemas import CreateUserPayload
from src.auth.models import User
from src.auth.service import UserService
from src.db.main import get_session

auth_router = APIRouter()
user_service = UserService()


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
    except HTTPException:
        raise
    except Exception as e:
        raise e
    return user
