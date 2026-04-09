from sqlalchemy.orm import Session
from ..models import Tag


class TagRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Tag]:
        return self.db.query(Tag).all()

    def get_by_id(self, tag_id: int) -> Tag|None:
        return self.db.get(Tag, tag_id)

    def create(self, tag: dict) -> Tag:
        new_tag = Tag(**tag)
        self.db.add(new_tag)
        self.db.commit()
        self.db.refresh(new_tag)
        return new_tag

    def update(self, tag_id: int, tag_data: dict) -> Tag|None:
        tag = self.db.get(Tag, tag_id)
        if tag:
            for key, value in tag_data.items():
                if value is not None:
                    setattr(tag, key, value)
            self.db.commit()
            self.db.refresh(tag)
            return tag
        return None

    def delete(self, tag_id: int) -> Tag|None:
        tag = self.db.get(Tag, tag_id)
        if tag:
            self.db.delete(tag)
            self.db.commit()
            return tag
        return None