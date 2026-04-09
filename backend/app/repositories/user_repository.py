from sqlalchemy.orm import Session
from ..models import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[User]:
        return self.db.query(User).all()

    def get_by_id(self, users_id: int) -> User|None:
        return self.db.get(User, users_id)

    def create(self, user: dict) -> User:
        new_user = User(**user)
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def update(self, user_id: int, user_data: dict) -> User|None:
        user = self.db.get(User, user_id)
        if user:
            for key, value in user_data.items():
                if value is not None:
                    setattr(user, key, value)
            self.db.commit()
            self.db.refresh(user)
            return user
        return None

    def delete(self, user_id: int) -> User|None:
        user = self.db.get(User, user_id)
        if user:
            self.db.delete(user)
            self.db.commit()
            return user
        return None