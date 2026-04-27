from sqlalchemy.ext.asyncio import AsyncSession
from ..models import Review
from sqlalchemy import func, select


class ReviewRepository:
    def __init__(self, db: AsyncSession):
        self.db = db


    async def get_all(self) -> list[Review]:
        result = await self.db.execute(select(Review))
        return result.scalars().all()


    async def get_by_id(self, review_id: int) -> Review|None:
        return await self.db.get(Review, review_id)


    async def create(self, review: dict) -> Review:
        new_review = Review(**review)
        self.db.add(new_review)
        await self.db.commit()
        await self.db.refresh(new_review)
        return new_review


    async def update(self, review: Review, review_data: dict) -> Review:
        for key, value in review_data.items():
            if value is not None:
                setattr(review, key, value)
        await self.db.commit()
        await self.db.refresh(review)
        return review


    async def delete(self, review: Review) -> Review:
        await self.db.delete(review)
        await self.db.commit()
        return review


    async def get_by_booking_code(self, booking_code: str) -> Review|None:
        result = await self.db.execute(
            select(Review).where(Review.booking_code==booking_code)
        )
        return result.scalar_one_or_none()