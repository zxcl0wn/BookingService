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
        result = await self.db.execute(select(User.id==users_id))
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


    async def update(self, user_id: int, user_data: dict) -> User|None:
        user = await self.db.get(User, user_id)
        hashed_password = get_password_hash(user_data["password"])

        if user:
            for key, value in user_data.items():
                if value is not None:
                    if key == "password":
                        setattr(user, key, hashed_password)
                    else:
                        setattr(user, key, value)
            await self.db.commit()
            await self.db.refresh(user)
            return user
        return None


    async def delete(self, user_id: int) -> User|None:
        user = await self.db.get(User, user_id)
        if user:
            await self.db.delete(user)
            await self.db.commit()
            return user
        return None


    async def get_user_by_username(self, username: str) -> User|None:
        result = await self.db.execute(select(User).where(User.username==username))
        return result.scalars().first()
