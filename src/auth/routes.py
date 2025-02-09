from http.client import HTTPException

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.schemas import CreateUserPayload
from src.auth.models import User
from src.auth.service import UserService
from src.db.main import get_session
from src.utils import logger


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
    except HTTPException as err:
        raise err
    except Exception as e:
        logger.error(str(e))
        raise e
    return user
