from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..schemas import RoomResponse, RoomCreate, RoomUpdate
from ..database import get_db
from ..services import RoomService

router = APIRouter(
    prefix="/rooms",
    tags=["Rooms"]
)
# TODO: add auth, jwt
@router.get("/", response_model=list[RoomResponse])
async def get_rooms(db: Session = Depends(get_db)):
    service = RoomService(db)
    return service.get_all()


@router.get("/{room_id}", response_model=RoomResponse)
async def get_room(room_id: int, db: Session = Depends(get_db)):
    service = RoomService(db)
    return service.get_by_id(room_id)


@router.post("/", response_model=RoomResponse)
async def create_room(room: RoomCreate, db: Session = Depends(get_db), ):
    service = RoomService(db)
    return service.create(room)


@router.put("/{room_id}", response_model=RoomResponse)
async def put_room(room_id: int, room_data: RoomUpdate, db: Session = Depends(get_db)):
    service = RoomService(db)
    return service.update(room_id, room_data)


@router.delete("/{room_id}", response_model=RoomResponse)
async def delete_room(room_id: int, db: Session = Depends(get_db)):
    service = RoomService(db)
    return service.delete(room_id)