import uuid
from sqlalchemy import Column, ForeignKey, Integer, DateTime, String
from ..database import Base
from datetime import timezone

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    booking_code = Column(String, unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    check_in = Column(DateTime(timezone=True), nullable=False)
    check_out = Column(DateTime(timezone=True), nullable=False)
