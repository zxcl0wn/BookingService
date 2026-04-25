from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..repositories import ReviewRepository, UserRepository, RoomRepository, BookingRepository
from ..schemas.review_schema import ReviewCreate, ReviewUpdate, ReviewResponse
import datetime
from ..core.celery_tasks import send_booking_code


class ReviewService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.review_repository = ReviewRepository(db)
        self.user_repository = UserRepository(db)
        self.room_repository = RoomRepository(db)
        self.booking_repository = BookingRepository(db)


    async def get_all(self) -> list[ReviewResponse]:
        reviews = await self.review_repository.get_all()
        return [ReviewResponse.model_validate(review) for review in reviews]


    async def get_by_id(self, review_id: int) -> ReviewResponse:
        review = await self.review_repository.get_by_id(review_id)
        if not review:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
        return ReviewResponse.model_validate(review)


    async def request_review_code(self, booking_id: int, current_user_id: int) -> dict:
        # Проверка: существует ли бронирование
        booking = await self.booking_repository.get_by_id(booking_id)
        if not booking:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
        
        # Проверка: принадлежит ли бронирование пользователю
        if booking.user_id != current_user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="This is not your booking")
        
        # Проверка: закончилось ли проживание
        if booking.check_out > datetime.datetime.now(datetime.UTC):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Stay not finished yet")
        
        # Проверка: не является ли пользователь владельцем комнаты
        room = await self.room_repository.get_by_id(booking.room_id)
        if room.owner_id == current_user_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Owner cannot review own room")
        
        # Проверка: нет ли уже отзыва на это бронирование
        existing_review = await self.review_repository.get_by_booking_code(booking.booking_code)
        if existing_review:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Review already exists for this booking")

        # Проверка: есть ли у пользователя email
        user = await self.user_repository.get_by_id(current_user_id)
        if not user.email:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User has no email address")

        # Отправка кода на email
        send_booking_code.delay(
            to_email=user.email,
            booking_code=booking.booking_code
        )
        
        return {
            "message": "Verification code has been sent to your email",
            "email": user.email
        }


    async def create(self, review: ReviewCreate, room_id: int, current_user_id: int) -> ReviewResponse:
        user = await self.user_repository.get_by_id(current_user_id)

        booking = await self.booking_repository.get_booking_by_booking_code(review.booking_code)
        if not booking:  # Есть ли бронь
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
        if booking.check_out > datetime.datetime.now(datetime.UTC):  # Только после выезда
            raise HTTPException(400, "Stay not finished")
        if booking.user_id != current_user_id:   # Проверка на владельца брони
            raise HTTPException(400, "User is not the owner of this booking")
        owner = await self.booking_repository.get_room_owner_by_booking_id(booking.id)
        if current_user_id == owner.id:
            raise HTTPException(400, "The owner cannot write a review for himself.")

        existing = await self.review_repository.get_by_booking_code(review.booking_code)
        if existing:
            raise HTTPException(400, "Review already exists")

        review_data = review.model_dump()
        review_data["user_id"] = current_user_id
        review_data["room_id"] = room_id
        new_review = await self.review_repository.create(review_data)
        return ReviewResponse.model_validate(new_review)


    async def update(self, review_id: int, review_data: ReviewUpdate, current_user_id: int) -> ReviewResponse:
        review = await self.review_repository.get_by_id(review_id)
        if not review:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
        if current_user_id != review.user_id:
            raise HTTPException(400, "User is not the owner of this review")

        await self.review_repository.update(review, review_data.model_dump())
        return ReviewResponse.model_validate(review)


    async def delete(self, review_id: int,  current_user_id: int) -> ReviewResponse:
        review = await self.review_repository.get_by_id(review_id)
        if not review:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
        if current_user_id != review.user_id:
            raise HTTPException(400, "User is not the owner of this review")

        await self.review_repository.delete(review)
        return ReviewResponse.model_validate(review)
