from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.util import await_only

from ..models import Booking
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


    async def update(self, booking_id: int, booking_data: dict) -> Booking|None:
        booking = await self.db.get(Booking, booking_id)
        if booking:
            for key, value in booking_data.items():
                if value is not None:
                    setattr(booking, key, value)
            await self.db.commit()
            await self.db.refresh(booking)
            return booking
        return None


    async def delete(self, booking_id) -> Booking|None:
        booking = await self.db.get(Booking, booking_id)
        if booking:
            await self.db.delete(booking)
            await self.db.commit()
            return booking
        return None