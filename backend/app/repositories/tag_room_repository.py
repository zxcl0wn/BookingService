from sqlalchemy.orm import Session
from ..models import TagRoom


class TagRoomRepository:
    def __init__(self, db: Session):
        self.db = db

    def add_tags(self, room_id: int, tag_ids: list[int]) -> None:
        for tag_id in tag_ids:
            existing = self.db.query(TagRoom).filter(
                TagRoom.room_id == room_id,
                TagRoom.tag_id == tag_id
            ).first()
            if not existing:
                self.db.add(TagRoom(room_id=room_id, tag_id=tag_id))
        self.db.commit()


    def delete_tags(self, room_id: int, tag_ids: list[int]) -> None:
        self.db.query(TagRoom).filter(
            TagRoom.room_id==room_id,
            TagRoom.tag_id.in_(tag_ids)
        ).delete()
        self.db.commit()