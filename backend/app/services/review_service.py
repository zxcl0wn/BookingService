from fastapi import HTTPException, status
from ..repositories import ReviewRepository, UserRepository, RoomRepository
from sqlalchemy.orm import Session
from ..schemas.review_schema import ReviewCreate, ReviewUpdate, ReviewResponse


class ReviewService:
    def __init__(self, db: Session):
        self.db = db
        self.review_repository = ReviewRepository(db)
        self.user_repository = UserRepository(db)
        self.room_repository = RoomRepository(db)

    def get_all(self) -> list[ReviewResponse]:
        reviews = self.review_repository.get_all()
        return [ReviewResponse.model_validate(review) for review in reviews]  # TODO: проверить ReviewResponse.model_validate(review, many=True)

    def get_by_id(self, review_id: int) -> ReviewResponse:
        review = self.review_repository.get_by_id(review_id)
        if not review:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
        return ReviewResponse.model_validate(review)

    def create(self, review: ReviewCreate) -> ReviewResponse:
        user = self.user_repository.create(review.model_dump())
        room = self.room_repository.create(review.model_dump())
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        if not room:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")

        new_review = self.review_repository.create(review.model_dump())
        room.rating = self.review_repository.avg_rating()
        self.db.commit()
        return ReviewResponse.model_validate(new_review)

    def update(self, review_id: int, review_data: ReviewUpdate) -> ReviewResponse:
        review = self.review_repository.update(review_id, review_data.model_dump())
        if not review:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
        return ReviewResponse.model_validate(review)

    def delete(self, review_id: int) -> ReviewResponse:
        review = self.review_repository.delete(review_id)
        if not review:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
        return ReviewResponse.model_validate(review)
    