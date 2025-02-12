from typing import Any
from src.reviews.schemas import (
    ReviewCreateSchema,
    ReviewPayloadSchema,
    ReviewResponseSchema,
)
from fastapi import APIRouter, status, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from src.auth.dependencies import AccessTokenBearer
from src.reviews.service import ReviewService
from src.utils import logger

review_service = ReviewService()


reviews_router = APIRouter()


@reviews_router.post(
    "/",
    response_model=ReviewResponseSchema,
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
)
async def create_review(
    payload: ReviewPayloadSchema,
    session: AsyncSession = Depends(get_session),
    access_token_bearer: dict[str, Any] = Depends(AccessTokenBearer()),
):
    user_uid = access_token_bearer["user"]["uid"]
    review = ReviewCreateSchema(**payload.model_dump(), user_uid=user_uid)
    try:
        updated_review = await review_service.add_review_to_book(
            review_data=review,
            session=session,
        )
    except Exception as e:
        logger.error(f"Error while creating review: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
    return updated_review
