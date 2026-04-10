from fastapi import HTTPException, status
from ..repositories import TagRepository
from sqlalchemy.orm import Session
from ..schemas.tag_schema import TagCreate, TagUpdate, TagResponse


class TagService:
    def __init__(self, db: Session):
        self.db = TagRepository(db)

    def get_all(self) -> list[TagResponse]:
        tags = self.db.get_all()
        return [TagResponse.model_validate(tag) for tag in tags]

    def get_by_id(self, tag_id: int) -> TagResponse:
        tag = self.db.get_by_id(tag_id)
        if not tag:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
        return TagResponse.model_validate(tag)

    def create(self, tag: TagCreate) -> TagResponse:
        new_tag = self.db.create(tag.model_dump())
        return TagResponse.model_validate(new_tag)

    def update(self, tag_id: int, tag_data: TagUpdate) -> TagResponse:
        tag = self.db.update(tag_id, tag_data.model_dump())
        if not tag:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
        return TagResponse.model_validate(tag)

    def delete(self, tag_id: int) -> TagResponse:
        tag = self.db.delete(tag_id)
        if not tag:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
        return TagResponse.model_validate(tag)