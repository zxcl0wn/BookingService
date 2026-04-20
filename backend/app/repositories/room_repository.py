from sqlalchemy.ext.asyncio import AsyncSession
from ..models import Room, Booking
from sqlalchemy import select

class RoomRepository:
    def __init__(self, db: AsyncSession):
        self.db = db


    async def get_all(self) -> list[Room]:
        result = await self.db.execute(select(Room))
        return result.scalars().all()


    async def get_by_id(self, room_id: int) -> Room|None:
        return await self.db.get(Room, room_id)


    async def create(self, room: dict) -> Room:
        new_room = Room(**room)
        self.db.add(new_room)
        await self.db.commit()
        await self.db.refresh(new_room)
        return new_room


    async def update(self, room_id: int, room_data: dict) -> Room|None:
        room = await self.db.get(Room, room_id)
        if room:
            for key, value in room_data.items():
                if value is not None:
                    setattr(room, key, value)
            await self.db.commit()
            await self.db.refresh(room)
            return room
        return None


    async def delete(self, room_id: int) -> Room|None:
        room = await self.db.get(Room, room_id)
        if room:
            await self.db.delete(room)
            await self.db.commit()
            return room
        return None


    async def is_booking_exist_by_room_id(self, room_id) -> bool:
        bookings = await self.db.execute(
            select(Booking).where(Booking.room_id==room_id).limit(1)
        )
        if bookings.scalar_one_or_none() is not None:
            return True
        return False