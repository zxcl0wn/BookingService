from sqlalchemy import Column, Integer, DateTime, String
from ..database import Base
import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=True, default=None)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    phone = Column(Integer, unique=True, nullable=True, default=None)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.datetime.now(datetime.UTC))
    photo = Column(String, nullable=True, default=None)
