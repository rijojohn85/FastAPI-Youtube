from src.db.models import Reviews
from sqlmodel.ext.asyncio.session import AsyncSession
from src.reviews.schemas import ReviewCreateSchema


class ReviewService:
    async def add_review_to_book(
        self,
        review_data: ReviewCreateSchema,
        session: AsyncSession,
    ) -> Reviews:
        try:
            review = Reviews(**review_data.model_dump())
            session.add(review)
            await session.commit()
            await session.refresh(review)
        except Exception as e:
            await session.rollback()
            raise e
        return review
