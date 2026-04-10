from pydantic import BaseModel, Field
from datetime import datetime

class RoomBase(BaseModel):
    title: str = Field(..., min_length=10, max_length=30, description="Room title")
    description: str|None = Field(None, min_length=20, max_length=200, description="Room description")
    address: str = Field(..., min_length=10, max_length=100, description="Room address")
    price_per_night: int = Field(..., ge=1, description="Price per night")


class RoomCreate(RoomBase):
    ...


class RoomResponse(RoomBase):
    id: int = Field(..., description="ID")
    rating: float|None = Field(None, ge=1, le=10, description="Room rating")
    created_at: datetime = Field(..., description="Room created at")
    owner_id: int = Field(..., description="Owner ID")


class RoomUpdate(BaseModel):
    title: str|None = None
    description: str|None = None
    address: str|None = None
    price_per_night: int|None = None
