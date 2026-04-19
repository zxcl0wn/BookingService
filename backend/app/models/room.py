from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Float
from ..database import Base
import datetime
from sqlalchemy.orm import relationship


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True, default=True)
    address = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.datetime.now(datetime.UTC))
    price_per_night = Column(Integer, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    rating = Column(Float, nullable=True, default=None)

    tags = relationship("Tag", secondary="tag_rooms", lazy="selectin")
