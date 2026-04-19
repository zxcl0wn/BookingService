from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..repositories import RoomRepository, TagRepository, TagRoomRepository
from ..schemas.room_schema import RoomUpdate, RoomCreate, RoomResponse


class RoomService:
    def __init__(self, db: AsyncSession):
        self.room_repository = RoomRepository(db)
        self.tag_repository = TagRepository(db)
        self.tag_room_repository = TagRoomRepository(db)


    def get_all(self) -> list[RoomResponse]:
        rooms = self.room_repository.get_all()
        return [RoomResponse.model_validate(room) for room in rooms]


    def get_by_id(self, room_id: int) -> RoomResponse:
        room = self.room_repository.get_by_id(room_id)
        if not room:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
        return RoomResponse.model_validate(room)


    def create(self, room: RoomCreate, owner_id: int) -> RoomResponse:
        data = room.model_dump()
        data["owner_id"] = owner_id
        new_room = self.room_repository.create(data)
        return RoomResponse.model_validate(new_room)


    def update(self, room_id: int, room_data: RoomUpdate, current_user_id: int) -> RoomResponse:
        room = self.room_repository.get_by_id(room_id)
        if not room:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
        if room.owner_id != current_user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not the owner of this room")

        updated_room = self.room_repository.update(room_id, room_data.model_dump())
        return RoomResponse.model_validate(updated_room)


    def delete(self, room_id: int, current_user_id: int) -> RoomResponse:
        room = self.room_repository.get_by_id(room_id)
        if not room:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
        if room.owner_id != current_user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not the owner of this room")

        deleted_room = self.room_repository.delete(room_id)
        return RoomResponse.model_validate(deleted_room)


    def add_tags(self, room_id: int, tag_ids: list[int], current_user_id: int) -> RoomResponse:
        room = self.room_repository.get_by_id(room_id)
        if not room:
            raise HTTPException(status_code=404, detail="Room not found")
        if current_user_id != room.owner_id:
            raise HTTPException(status_code=403, detail="You are not the owner of this room")

        for tag_id in tag_ids:
            tag = self.tag_repository.get_by_id(tag_id)
            if not tag:
                raise HTTPException(status_code=404, detail=f"Tag {tag_id} not found")

        self.tag_room_repository.add_tags(room_id, tag_ids)
        room = self.room_repository.get_by_id(room_id)
        return RoomResponse.model_validate(room)


    def delete_tags(self, room_id: int, tag_ids: list[int], current_user_id: int) -> RoomResponse:
        room = self.room_repository.get_by_id(room_id)
        if not room:
            raise HTTPException(status_code=404, detail="Room not found")
        if current_user_id != room.owner_id:
            raise HTTPException(status_code=403, detail="You are not the owner of this room")

        for tag_id in tag_ids:
            tag = self.tag_repository.get_by_id(tag_id)
            if not tag:
                raise HTTPException(status_code=404, detail=f"Tag {tag_id} not found")

        self.tag_room_repository.delete_tags(room_id, tag_ids)
        room = self.room_repository.get_by_id(room_id)
        return RoomResponse.model_validate(room)
