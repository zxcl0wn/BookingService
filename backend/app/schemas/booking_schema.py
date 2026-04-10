from pydantic import BaseModel, Field
from datetime import datetime


class BookingBase(BaseModel):
    user_id: int = Field(..., description="User ID")
    room_id: int = Field(..., description="Room ID")
    check_in: datetime = Field(..., description="Check-in date")
    check_out: datetime = Field(..., description="Check-out date")


class BookingResponse(BookingBase):
    id: int = Field(..., description="ID")

    class Config:
        from_attributes = True


class BookingCreate(BookingBase):
    ...


class BookingUpdate(BaseModel):
    check_in: datetime|None = None
    check_out: datetime|None = None
