from fastapi import HTTPException, status
from ..repositories import BookingRepository, UserRepository, RoomRepository
from sqlalchemy.orm import Session
from ..schemas.booking_schema import BookingResponse, BookingCreate, BookingUpdate


class BookingService:
    def __init__(self, db: Session):
        self.booking_repository = BookingRepository(db)
        self.user_repository = UserRepository(db)
        self.room_repository = RoomRepository(db)


    def get_all(self) -> list[BookingResponse]:
        bookings = self.booking_repository.get_all()
        return [BookingResponse.model_validate(booking) for booking in bookings]


    def get_by_id(self, booking_id: int) -> BookingResponse:
        booking = self.booking_repository.get_by_id(booking_id)
        if not booking:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Booking not found")
        return BookingResponse.model_validate(booking)


    def create(self, booking: BookingCreate) -> BookingResponse:
        room = self.room_repository.get_by_id(booking.room_id)
        user = self.user_repository.get_by_id(booking.user_id)
        if not room:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Room not found")
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User not found")

        new_booking = self.booking_repository.create(booking.model_dump())  # TODO: Проверка дат
        return BookingResponse.model_validate(new_booking)


    def update(self, booking_id: int, booking_data: BookingUpdate) -> BookingResponse|None:
        booking = self.booking_repository.update(booking_id, booking_data.model_dump())
        if not booking:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
        return BookingResponse.model_validate(booking)


    def delete(self, booking_id: int) -> BookingResponse:
        booking = self.booking_repository.delete(booking_id)
        if not booking:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
        return BookingResponse.model_validate(booking)
