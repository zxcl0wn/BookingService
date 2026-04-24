from sqlalchemy import Column, Integer, ForeignKey
from ..core.database import Base


class TagRoom(Base):
    __tablename__ = "tag_rooms"

    id = Column(Integer, primary_key=True, index=True)
    tag_id = Column(Integer, ForeignKey("tags.id"), nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
