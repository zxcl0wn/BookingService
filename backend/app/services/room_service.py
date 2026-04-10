from fastapi import HTTPException, status
from ..repositories import RoomRepository
from sqlalchemy.orm import Session
from ..schemas.room_schema import RoomUpdate, RoomCreate, RoomResponse


class RoomService:
    def __init__(self, db: Session):
        self.db = RoomRepository(db)

    def get_all(self) -> list[RoomResponse]:
        rooms = self.db.get_all()
        return [RoomResponse.model_validate(room) for room in rooms]

    def get_by_id(self, room_id: int) -> RoomResponse:
        room = self.db.get_by_id(room_id)
        if not room:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
        return RoomResponse.model_validate(room)

    def create(self, room: RoomCreate) -> RoomResponse:
        new_room = self.db.create(room.model_dump())
        return RoomResponse.model_validate(new_room)

    def update(self, room_id: int, room_data: RoomUpdate) -> RoomResponse:
        room = self.db.update(room_id, room_data.model_dump())
        if not room:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
        return RoomResponse.model_validate(room)

    def delete(self, room_id: int) -> RoomResponse:
        room = self.db.delete(room_id)
        if not room:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
        return RoomResponse.model_validate(room)
        