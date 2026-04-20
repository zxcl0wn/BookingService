from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..auth.services.auth_services import get_current_user
from ..models import User
from ..schemas import UserResponse, UserUpdate
from ..database import get_db
from ..services import UserService


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/", response_model=list[UserResponse])
async def get_users(db: AsyncSession = Depends(get_db)):
    service = UserService(db)
    return await service.get_all()


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    service = UserService(db)
    return await service.get_by_id(user_id)


@router.put("/{user_id}", response_model=UserResponse)
async def put_user(
        user_id: int,
        user_data: UserUpdate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    service = UserService(db)
    return await service.update(user_id, user_data, current_user.id)


@router.delete("/{user_id}", response_model=UserResponse)
async def delete_user(
        user_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    service = UserService(db)
    return await service.delete(user_id, current_user.id)

