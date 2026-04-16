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


    def create(self,
               booking: BookingCreate,
               room_id: int,
               current_user_id: int,
               ) -> BookingResponse:
        room = self.room_repository.get_by_id(room_id)
        user = self.user_repository.get_by_id(current_user_id)
        if not room:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Room not found")
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User not found")

        booking_data = booking.model_dump()
        booking_data['user_id'] = current_user_id
        booking_data['room_id'] = room_id
        new_booking = self.booking_repository.create(booking_data)  # TODO: Проверка дат
        return BookingResponse.model_validate(new_booking)


    def update(self, booking_id: int, booking_data: BookingUpdate, current_user_id: int) -> BookingResponse|None:
        booking = self.booking_repository.get_by_id(booking_id)
        if not booking:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
        if current_user_id != booking.user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not the owner of this room")

        updated_booking = self.booking_repository.update(booking_id, booking_data.model_dump())
        return BookingResponse.model_validate(updated_booking)


    def delete(self, booking_id: int, current_user_id: int) -> BookingResponse:
        booking = self.booking_repository.get_by_id(booking_id)
        if not booking:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
        if current_user_id != booking.user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not the owner of this room")

        deleted_booking = self.booking_repository.delete(booking_id)
        return BookingResponse.model_validate(deleted_booking)
