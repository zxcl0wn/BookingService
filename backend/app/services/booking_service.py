from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..repositories import BookingRepository, UserRepository, RoomRepository
from ..schemas.booking_schema import BookingResponse, BookingCreate, BookingUpdate
import datetime


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
        await self.date_valid_check(room_id, booking.check_in, booking.check_out)

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
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not the owner of this booking")
        await self.date_valid_check(booking.room_id, booking_data.check_in, booking.check_out, booking_id)

        updated_booking = await self.booking_repository.update(booking, booking_data.model_dump())
        return BookingResponse.model_validate(updated_booking)


    async def delete(self, booking_id: int, current_user_id: int) -> BookingResponse:
        booking = await self.booking_repository.get_by_id(booking_id)
        if not booking:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
        if current_user_id != booking.user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not the owner of this booking")

        await self.booking_repository.delete(booking)
        return BookingResponse.model_validate(booking)


    async def get_booking_by_booking_code(self, booking_code: str) -> BookingResponse|None:
        booking = await self.booking_repository.get_booking_by_booking_code(booking_code)
        if not booking:
            return None
        return BookingResponse.model_validate(booking)


    async def date_valid_check(self, room_id: int, check_in: datetime.datetime, check_out: datetime.datetime, exclude_booking_id: int=None) -> bool:
        # Проверка сроков. Начало: текущий день, конец: текущая дата+1 год
        current_date = datetime.datetime.now(datetime.UTC)
        last_date = current_date + datetime.timedelta(days=365)
        if check_in < current_date:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Check-in date must be after today")
        elif check_out > last_date:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Check-out date must be before last date")

        # Проверка на пересечение с другими бронями
        if not await self.booking_repository.check_availability(room_id, check_in, check_out, exclude_booking_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Room is not available for selected dates"
            )

        # Конец > Начало
        if check_out < check_in:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Check-out date must be after check-in date")

        return True