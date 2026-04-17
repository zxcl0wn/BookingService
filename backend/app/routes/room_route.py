from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
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
async def get_rooms(db: Session = Depends(get_db)):
    service = RoomService(db)
    return service.get_all()


@router.get("/{room_id}", response_model=RoomResponse)
async def get_room(room_id: int, db: Session = Depends(get_db)):
    service = RoomService(db)
    return service.get_by_id(room_id)


@router.post("/", response_model=RoomResponse)
async def create_room(
        room: RoomCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    service = RoomService(db)
    return service.create(room, owner_id=current_user.id)


@router.put("/{room_id}", response_model=RoomResponse)
async def put_room(
        room_id: int,
        room_data: RoomUpdate,
        db: Session = Depends(get_db),
        current_user_id: User = Depends(get_current_user),
):
    service = RoomService(db)
    return service.update(room_id, room_data, current_user_id.id)


@router.delete("/{room_id}", response_model=RoomResponse)
async def delete_room(
        room_id: int,
        db: Session = Depends(get_db),
        current_user_id: User = Depends(get_current_user),
):
    service = RoomService(db)
    return service.delete(room_id, current_user_id.id)


@router.post("/{room_id}/tags", response_model=RoomResponse)
async def add_tags(
        room_id: int,
        tag_ids: list[int],
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    service = RoomService(db)
    return service.add_tags(room_id, tag_ids, current_user.id)


@router.delete("/{room_id}/tags", response_model=RoomResponse)
async def delete_tags(
        room_id: int,
        tag_ids: list[int],
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    service = RoomService(db)
    return service.delete_tags(room_id, tag_ids, current_user.id)
