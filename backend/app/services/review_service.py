from fastapi import HTTPException, status
from ..repositories import ReviewRepository, UserRepository, RoomRepository, BookingRepository
from sqlalchemy.orm import Session
from ..schemas.review_schema import ReviewCreate, ReviewUpdate, ReviewResponse
import datetime


class ReviewService:
    def __init__(self, db: Session):
        self.db = db
        self.review_repository = ReviewRepository(db)
        self.user_repository = UserRepository(db)
        self.room_repository = RoomRepository(db)
        self.booking_repository = BookingRepository(db)

    def get_all(self) -> list[ReviewResponse]:
        reviews = self.review_repository.get_all()
        return [ReviewResponse.model_validate(review) for review in reviews]  # TODO: проверить ReviewResponse.model_validate(review, many=True)

    def get_by_id(self, review_id: int) -> ReviewResponse:
        review = self.review_repository.get_by_id(review_id)
        if not review:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
        return ReviewResponse.model_validate(review)

    def create(self, review: ReviewCreate, booking_id: int, current_user_id: int) -> ReviewResponse:
        booking = self.booking_repository.get_by_id(booking_id)
        if not booking:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
        print(f'{booking.check_out = }')
        print(f'{datetime.datetime.now(datetime.UTC) = }')
        if booking.check_out < datetime.datetime.now(datetime.UTC):
            raise HTTPException(400, "Stay not finished")
        if booking.user_id != current_user_id:
            raise HTTPException(400, "User is not the owner of this booking")

        existing = self.review_repository.get_by_booking_code(review.booking_code)
        if existing:
            raise HTTPException(400, "Review already exists")

        new_review = self.review_repository.create(review.model_dump())
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
    