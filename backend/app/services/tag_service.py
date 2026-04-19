from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..repositories import TagRepository
from ..schemas.tag_schema import TagCreate, TagUpdate, TagResponse


class TagService:
    def __init__(self, db: AsyncSession):
        self.db = TagRepository(db)

    async def get_all(self) -> list[TagResponse]:
        tags = await self.db.get_all()
        return [TagResponse.model_validate(tag) for tag in tags]

    async def get_by_id(self, tag_id: int) -> TagResponse:
        tag = await self.db.get_by_id(tag_id)
        if not tag:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
        return TagResponse.model_validate(tag)

    async def create(self, tag: TagCreate) -> TagResponse:
        new_tag = await self.db.create(tag.model_dump())
        return TagResponse.model_validate(new_tag)

    async def update(self, tag_id: int, tag_data: TagUpdate) -> TagResponse:
        tag = await self.db.update(tag_id, tag_data.model_dump())
        if not tag:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
        return TagResponse.model_validate(tag)

    async def delete(self, tag_id: int) -> TagResponse:
        tag = await self.db.delete(tag_id)
        if not tag:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
        return TagResponse.model_validate(tag)
