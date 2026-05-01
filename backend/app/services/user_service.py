from fastapi import HTTPException, status, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from ..core.minio_handler import MinioHandler
from ..models import User
from ..repositories import UserRepository
from ..schemas.user_schema import UserResponse, UserCreate, UserUpdate
from sqlalchemy.exc import IntegrityError
from ..core.config import settings


class UserService:
    def __init__(self, db: AsyncSession):
        self.user_repository = UserRepository(db)
        self.minio_handler = MinioHandler()


    async def get_all(self, skip: int, limit: int) -> list[UserResponse]:
        users = await self.user_repository.get_all(skip=skip, limit=limit)
        return [UserResponse.model_validate(user) for user in users]


    async def get_by_id(self, user_id: int) -> UserResponse:
        user = await self.user_repository.get_by_id(user_id)

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return UserResponse.model_validate(user)


    async def create(self, user: UserCreate) -> UserResponse:
        try:
            new_user = await self.user_repository.create(user.model_dump())
            return UserResponse.model_validate(new_user)
        except IntegrityError:
            raise HTTPException(status_code=409, detail="User already exists")


    async def update(self, user_id: int, user_data: UserUpdate, current_user_id: int) -> UserResponse:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        if current_user_id != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to update this user")

        user_by_email = await self.user_repository.get_user_by_email(user_data.email)
        if user_by_email is not None and user_by_email.id != user.id:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")

        user_by_phone = await self.user_repository.get_user_by_phone(user_data.phone)
        if user_by_phone is not None and user_by_phone.id != user.id:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Phone already exists")

        # try:
        #     updated_user = await self.user_repository.update(user, user_data.model_dump())
        #     return UserResponse.model_validate(updated_user)
        # except Exception as E:
        #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to update user")
        await self.user_repository.update(user, user_data.model_dump())
        return UserResponse.model_validate(user)


    async def delete(self, user_id: int, current_user_id: int) -> UserResponse:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        if current_user_id != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to delete this user")

        await self.user_repository.delete(user)
        return UserResponse.model_validate(user)


    async def get_user_by_username(self, username: str) -> User:
        user = await self.user_repository.get_user_by_username(username)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user


    async def upload_avatar(self, current_user_id: int, file: UploadFile|None, current_user_photo: str|None):
        if not file.content_type.startswith('image/'):
            raise HTTPException(400, "File must be an image")

        if current_user_photo:
            await self.minio_handler.delete_file(settings.minio.user_avatars_bucket, current_user_photo)

        new_file_name = await self.minio_handler.upload_user_photo(current_user_id, file)
        await self.user_repository.update_avatar(current_user_id, new_file_name)

        url = await self.minio_handler.get_public_url(settings.minio.user_avatars_bucket, new_file_name)
        return {
            "url": url,
            "file_name": new_file_name
        }


    async def delete_avatar(self, current_user_id: int, current_user_photo: str|None):
        if not current_user_photo:
            raise HTTPException(404, "No avatar to delete")

        await self.minio_handler.delete_file(settings.minio.user_avatars_bucket, current_user_photo)
        await self.user_repository.update_avatar(current_user_id, None)

        return {
            "message": "Avatar deleted"
        }