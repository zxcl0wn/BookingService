from sqlalchemy.ext.asyncio import AsyncSession
from ..models import User
from ..auth.utils.auth_utils import get_password_hash
from sqlalchemy import select


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db


    async def get_all(self) -> list[User]:
        result = await self.db.execute(select(User))
        return result.scalars().all()


    async def get_by_id(self, users_id: int) -> User|None:
        result = await self.db.execute(
            select(User).where(User.id == users_id)
        )
        return result.scalars().one_or_none()


    async def create(self, user: dict) -> User:
        hashed_password = get_password_hash(user["password"])
        new_user = User(
            username=user["username"],
            email=user["email"],
            name=user["name"],
            phone=user["phone"],
            password=hashed_password
        )
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        return new_user


    async def update(self, user: User, user_data: dict) -> User:
        hashed_password = get_password_hash(user_data["password"])

        for key, value in user_data.items():
            if value is not None:
                if key == "password":
                    setattr(user, key, hashed_password)
                else:
                    setattr(user, key, value)
        await self.db.commit()
        await self.db.refresh(user)
        return user


    async def delete(self, user: User) -> User:
        await self.db.delete(user)
        await self.db.commit()
        return user


    async def get_user_by_username(self, username: str) -> User|None:
        result = await self.db.execute(
            select(User).where(User.username==username)
        )
        return result.scalar_one_or_none()


    async def get_user_by_email(self, email: str) -> User|None:
        user = await self.db.execute(
            select(User).where(User.email==email)
        )
        return user.scalar_one_or_none()


    async def get_user_by_phone(self, phone: int) -> User|None:
        user = await self.db.execute(
            select(User).where(User.phone==phone)
        )
        return user.scalar_one_or_none()
