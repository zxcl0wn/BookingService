import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.util import await_only

from ..models import Booking, User, Room
from sqlalchemy import select


class BookingRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db


    async def get_all(self) -> list[Booking]:
        result = await self.db.execute(select(Booking))
        return result.scalars().all()


    async def get_by_id(self, booking_id: int) -> Booking|None:
        return await self.db.get(Booking, booking_id)


    async def create(self, booking: dict) -> Booking:
        new_booking = Booking(**booking)
        self.db.add(new_booking)
        await self.db.commit()
        await self.db.refresh(new_booking)
        return new_booking


    async def update(self, booking: Booking, booking_data: dict) -> Booking:
        for key, value in booking_data.items():
            if value is not None:
                setattr(booking, key, value)
        await self.db.commit()
        await self.db.refresh(booking)
        return booking


    async def delete(self, booking: Booking) -> Booking:
        await self.db.delete(booking)
        await self.db.commit()
        return booking


    async def get_booking_by_booking_code(self, booking_code: str) -> Booking|None:
        booking = await self.db.execute(
            select(Booking).where(Booking.booking_code==booking_code)
        )
        return booking.scalars().one_or_none()


    async def get_room_owner_by_booking_id(self, booking_id: int) -> Booking|None:
        booking = await self.db.get(Booking, booking_id)
        print(f'{booking = }')
        room = await self.db.execute(
            select(Room).where(Room.id==booking.room_id)
        )
        print(f'{room = }')
        owner = await self.db.execute(
            select(User).where(User.id==room.scalars().one().owner_id)
        )
        print(f'{owner = }')
        return owner.scalars().one_or_none()


    async def check_availability(self,
        room_id: int,
        check_in: datetime.datetime,
        check_out: datetime.datetime,
        exclude_booking_id: int = None
    ) -> bool:
        query = select(Booking).where(
            Booking.room_id==room_id,
            Booking.check_in<check_out,
            Booking.check_out>check_in
        )

        if exclude_booking_id:
            query = query.where(Booking.id != exclude_booking_id)
        result = await self.db.execute(query)
        conflicting_bookings = result.scalars().all()

        if len(conflicting_bookings)==0:
            return True
        return False
