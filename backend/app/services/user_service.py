from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import User
from ..repositories import UserRepository
from ..schemas.user_schema import UserResponse, UserCreate, UserUpdate
from sqlalchemy.exc import IntegrityError


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = UserRepository(db)


    async def get_all(self) -> list[UserResponse]:
        users = await self.db.get_all()
        return [UserResponse.model_validate(user) for user in users]


    async def get_by_id(self, user_id: int) -> UserResponse:
        user = await self.db.get_by_id(user_id)
        print(f'{user = }')
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return UserResponse.model_validate(user)


    async def create(self, user: UserCreate) -> UserResponse:
        try:
            new_user = await self.db.create(user.model_dump())
            return UserResponse.model_validate(new_user)
        except IntegrityError:
            raise HTTPException(status_code=409, detail="User already exists")


    async def update(self, user_id: int, user_data: UserUpdate, current_user_id: int) -> UserResponse:
        user = await self.db.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        if current_user_id != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to update this user")

        user_by_email = await self.db.get_user_by_email(user_data.email)
        if user_by_email is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")

        user_by_phone = await self.db.get_user_by_phone(user_data.phone)
        if user_by_phone is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Phone already exists")

        try:
            updated_user = await self.db.update(user_id, user_data.model_dump())
            return UserResponse.model_validate(updated_user)
        except Exception as E:
            print(E)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to update user")


    async def delete(self, user_id: int, current_user_id: int) -> UserResponse:
        user = await self.db.delete(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        if current_user_id != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to delete this user")

        return UserResponse.model_validate(user)


    async def get_user_by_username(self, username: str) -> User:
        user = await self.db.get_user_by_username(username)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user