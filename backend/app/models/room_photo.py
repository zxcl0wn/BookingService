from sqlalchemy import Column, ForeignKey, String, Boolean, Integer
from ..core.database import Base


class RoomPhoto(Base):
    __tablename__ = "room_photos"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False)
    photo_url = Column(String, nullable=False)
    is_main = Column(Boolean, nullable=False, default=False)
