from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..schemas import UserResponse, UserCreate, UserUpdate
from ..database import get_db
from ..services import UserService


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/", response_model=list[UserResponse])
async def get_users(db: Session = Depends(get_db)):
    service = UserService(db)
    return service.get_all()


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.get_by_id(user_id)


@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.create(user)


@router.put("/{user_id}", response_model=UserResponse)
async def put_user(room_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.update(room_id, user_data)


@router.delete("/{user_id}", response_model=UserResponse)
async def delete_user(room_id: int, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.delete(room_id)

