from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import TagRoom


class TagRoomRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_tags(self, room_id: int, tag_ids: list[int]) -> None:
        for tag_id in tag_ids:
            result = await self.db.execute(
                select(TagRoom).where(
                    TagRoom.room_id==room_id,
                    TagRoom.tag_id==tag_id
                )
            )
            existing = result.scalar_one_or_none()
            if not existing:
                self.db.add(TagRoom(room_id=room_id, tag_id=tag_id))
        await self.db.commit()


    async def delete_tags(self, room_id: int, tag_ids: list[int]) -> None:
        await self.db.execute(
            delete(TagRoom).where(
                TagRoom.room_id == room_id,
                TagRoom.tag_id.in_(tag_ids)
            )
        )
        await self.db.commit()