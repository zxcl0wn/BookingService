from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import Tag


class TagRepository:
    def __init__(self, db: AsyncSession):
        self.db = db


    async def get_all(self) -> list[Tag]:
        result = await self.db.execute(select(Tag))
        return result.scalars().all()


    async def get_by_id(self, tag_id: int) -> Tag|None:
        return await self.db.get(Tag, tag_id)


    async def create(self, tag: dict) -> Tag:
        new_tag = Tag(**tag)
        self.db.add(new_tag)
        await self.db.commit()
        await self.db.refresh(new_tag)
        return new_tag


    async def update(self, tag_id: int, tag_data: dict) -> Tag|None:
        tag = await self.db.get(Tag, tag_id)
        if tag:
            for key, value in tag_data.items():
                if value is not None:
                    setattr(tag, key, value)
            await self.db.commit()
            await self.db.refresh(tag)
            return tag
        return None


    async def delete(self, tag_id: int) -> Tag|None:
        tag = await self.db.get(Tag, tag_id)
        if tag:
            await self.db.delete(tag)
            await self.db.commit()
            return tag
        return None