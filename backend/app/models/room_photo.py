from sqlalchemy import Column, ForeignKey, String, Boolean, Integer
from ..database import Base


class RoomPhoto(Base):
    __tablename__ = "room_photos"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    photo_url = Column(String, nullable=False)
    is_main = Column(Boolean, nullable=False, default=False)
