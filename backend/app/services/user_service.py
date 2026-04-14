from fastapi import HTTPException, status
from ..models import User
from ..repositories import UserRepository
from sqlalchemy.orm import Session
from ..schemas.user_schema import UserResponse, UserCreate, UserUpdate
from sqlalchemy.exc import IntegrityError


class UserService:
    def __init__(self, db: Session):
        self.db = UserRepository(db)


    def get_all(self) -> list[UserResponse]:
        users = self.db.get_all()
        return [UserResponse.model_validate(user) for user in users]


    def get_by_id(self, user_id: int) -> UserResponse:
        user = self.db.get_by_id(user_id)
        print(f'{user = }')
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return UserResponse.model_validate(user)


    def create(self, user: UserCreate) -> UserResponse:
        try:
            new_user = self.db.create(user.model_dump())
            return UserResponse.model_validate(new_user)
        except IntegrityError:
            raise HTTPException(status_code=409, detail="User already exists")


    def update(self, user_id: int, user_data: UserUpdate) -> UserResponse:
        user = self.db.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        try:
            updated_user = self.db.update(user_id, user_data.model_dump())
            return UserResponse.model_validate(updated_user)
        except:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to update user")


    def delete(self, user_id: int) -> UserResponse:
        user = self.db.delete(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return UserResponse.model_validate(user)


    def get_user_by_username(self, username: str) -> User:
        user = self.db.get_user_by_username(username)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return UserResponse.model_validate(user)