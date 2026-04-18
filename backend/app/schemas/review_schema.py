from pydantic import BaseModel, Field
from datetime import datetime


class ReviewBase(BaseModel):
    rating: int = Field(..., ge=1, le=10, description="Review rating")
    title: str = Field(..., min_length=5, max_length=25, description="Review title")
    comment: str|None = Field(None, min_length=5, max_length=100, description="Review comment")


class ReviewCreate(ReviewBase):
    booking_code: str = Field(..., description="Booking code")


class ReviewResponse(ReviewBase):
    user_id: int = Field(..., description="User ID")
    room_id: int = Field(..., description="Room ID")
    created_at: datetime = Field(..., description="Review created at")

    class Config:
        from_attributes = True


class ReviewUpdate(BaseModel):
    rating: int|None = Field(None, ge=1, le=10, description="Review rating")
    title: str|None = Field(None, min_length=5, max_length=25, description="Review title")
    comment: str|None = Field(None, min_length=5, max_length=100, description="Review comment")
