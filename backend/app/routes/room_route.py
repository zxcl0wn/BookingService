from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas import RoomResponse, RoomCreate, RoomUpdate
from ..database import get_db
from ..services import RoomService
from ..auth.services.auth_services import get_current_user
from ..models import User


router = APIRouter(
    prefix="/rooms",
    tags=["Rooms"]
)

@router.get("/", response_model=list[RoomResponse])
async def get_rooms(db: AsyncSession = Depends(get_db)):
    service = RoomService(db)
    return await service.get_all()


@router.get("/{room_id}", response_model=RoomResponse)
async def get_room(room_id: int, db: AsyncSession = Depends(get_db)):
    service = RoomService(db)
    return await service.get_by_id(room_id)


@router.post("/", response_model=RoomResponse)
async def create_room(
        room: RoomCreate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    service = RoomService(db)
    return await service.create(room, owner_id=current_user.id)


@router.put("/{room_id}", response_model=RoomResponse)
async def put_room(
        room_id: int,
        room_data: RoomUpdate,
        db: AsyncSession = Depends(get_db),
        current_user_id: User = Depends(get_current_user),
):
    service = RoomService(db)
    return await service.update(room_id, room_data, current_user_id.id)


@router.delete("/{room_id}", response_model=RoomResponse)
async def delete_room(
        room_id: int,
        db: AsyncSession = Depends(get_db),
        current_user_id: User = Depends(get_current_user),
):
    service = RoomService(db)
    return await service.delete(room_id, current_user_id.id)


@router.post("/{room_id}/tags", response_model=RoomResponse)
async def add_tags(
        room_id: int,
        tag_ids: list[int],
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    service = RoomService(db)
    return await service.add_tags(room_id, tag_ids, current_user.id)


@router.delete("/{room_id}/tags", response_model=RoomResponse)
async def delete_tags(
        room_id: int,
        tag_ids: list[int],
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    service = RoomService(db)
    return await service.delete_tags(room_id, tag_ids, current_user.id)
