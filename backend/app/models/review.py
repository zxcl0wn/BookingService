from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime
from ..core.database import Base
import datetime


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    comment = Column(Text, nullable=True, default=None)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.datetime.now(datetime.UTC))
    booking_code: str = Column(String, unique=True, nullable=False)
