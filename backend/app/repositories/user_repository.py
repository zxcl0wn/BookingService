from sqlalchemy.orm import Session
from ..models import User
from ..auth.security import verify_password, get_password_hash


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[User]:
        return self.db.query(User).all()

    def get_by_id(self, users_id: int) -> User|None:
        return self.db.get(User, users_id)

    def create(self, user: dict) -> User:
        hashed_password = get_password_hash(user["password"])
        new_user = User(
            username=user["username"],
            email=user["email"],
            name=user["name"],
            phone=user["phone"],
            password=hashed_password
        )
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def update(self, user_id: int, user_data: dict) -> User|None:
        user = self.db.get(User, user_id)
        hashed_password = get_password_hash(user_data["password"])
        if user:
            for key, value in user_data.items():
                if value is not None:
                    if key is "password":
                        setattr(user, key, hashed_password)
                    else:
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