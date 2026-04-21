from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..repositories import BookingRepository, UserRepository, RoomRepository
from ..schemas.booking_schema import BookingResponse, BookingCreate, BookingUpdate


class BookingService:
    def __init__(self, db: AsyncSession):
        self.booking_repository = BookingRepository(db)
        self.user_repository = UserRepository(db)
        self.room_repository = RoomRepository(db)


    async def get_all(self) -> list[BookingResponse]:
        bookings = await self.booking_repository.get_all()
        return [BookingResponse.model_validate(booking) for booking in bookings]


    async def get_by_id(self, booking_id: int) -> BookingResponse:
        booking = await self.booking_repository.get_by_id(booking_id)
        if not booking:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Booking not found")
        return BookingResponse.model_validate(booking)


    async def create(self,
               booking: BookingCreate,
               room_id: int,
               current_user_id: int,
               ) -> BookingResponse:
        room = await self.room_repository.get_by_id(room_id)
        user = await self.user_repository.get_by_id(current_user_id)
        room_owner = await self.user_repository.get_by_id(room.owner_id)
        if not room:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Room not found")
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User not found")
        if room_owner.id == current_user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="The owner cannot write to create a reservation for his room.")

        booking_data = booking.model_dump()
        booking_data['user_id'] = current_user_id
        booking_data['room_id'] = room_id
        new_booking = await self.booking_repository.create(booking_data)  # TODO: Проверка дат
        return BookingResponse.model_validate(new_booking)


    async def update(self, booking_id: int, booking_data: BookingUpdate, current_user_id: int) -> BookingResponse|None:
        booking = await self.booking_repository.get_by_id(booking_id)
        if not booking:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
        if current_user_id != booking.user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not the owner of this room")

        updated_booking = await self.booking_repository.update(booking_id, booking_data.model_dump())
        return BookingResponse.model_validate(updated_booking)


    async def delete(self, booking_id: int, current_user_id: int) -> BookingResponse:  # TODO: лишний запрос в БД
        booking = await self.booking_repository.get_by_id(booking_id)
        if not booking:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
        if current_user_id != booking.user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not the owner of this room")

        deleted_booking = await self.booking_repository.delete(booking_id)
        return BookingResponse.model_validate(deleted_booking)


    async def get_booking_by_booking_code(self, booking_code: str) -> BookingResponse|None:
        booking = await self.booking_repository.get_booking_by_booking_code(booking_code)
        if not booking:
            return None
        return BookingResponse.model_validate(booking)
