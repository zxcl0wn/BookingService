from sqlalchemy.ext.asyncio import AsyncSession
from ..models import Room, Booking, Review
from sqlalchemy import select, func


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


    async def update(self, room: Room, room_data: dict) -> Room:
        for key, value in room_data.items():
            if value is not None:
                setattr(room, key, value)
        await self.db.commit()
        await self.db.refresh(room)
        return room


    async def delete(self, room: Room) -> Room:
        await self.db.delete(room)
        await self.db.commit()
        return room


    async def is_booking_exist_by_room_id(self, room_id) -> bool:
        bookings = await self.db.execute(
            select(Booking).where(Booking.room_id==room_id).limit(1)
        )
        if bookings.scalar_one_or_none() is not None:
            return True
        return False


    async def avg_rating(self, room_id: int) -> None:
        room = await self.db.get(Room, room_id)

        sum_rating = await self.db.execute(
            select(func.sum(Review.rating)).where(Review.room_id==room_id)
        )
        count_result = await self.db.execute(
            select(func.count(Review.id)).where(Review.room_id == room_id)
        )
        sum_rating = sum_rating.scalar()
        count = count_result.scalar()
        room.rating = sum_rating / count if count else 0
        await self.db.commit()
