from sqlalchemy.orm import Session
from ..models import Room


class RoomRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Room]:
        return self.db.query(Room).all()

    def get_by_id(self, room_id: int) -> Room|None:
        return self.db.get(Room, room_id)

    def create(self, room: dict) -> Room:
        new_room = Room(**room)
        self.db.add(new_room)
        self.db.commit()
        self.db.refresh(room)
        return new_room

    def update(self, room_id: int, room_data: dict) -> Room|None:
        room = self.db.get(Room, room_id)
        if room:
            for key, value in room_data.items():
                if value is not None:
                    setattr(room, key, value)
            self.db.commit()
            self.db.refresh(room)
            return room
        return None

    def delete(self, room_id: int) -> Room|None:
        room = self.db.get(Room, room_id)
        if room:
            self.db.delete(room)
            self.db.commit()
            return room
        return None