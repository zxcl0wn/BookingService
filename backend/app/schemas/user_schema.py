from pydantic import BaseModel, Field
from datetime import datetime


class UserBase(BaseModel):
    username: str = Field(..., min_length=5, max_length=20, description="Username")
    email: str|None = Field(None, description="Email")
    name: str = Field(..., min_length=5, max_length=30, description="Name")
    phone: int|None = Field(None, description="Phone")


class UserResponse(UserBase):
    id: int = Field(..., description="ID")
    created_at: datetime = Field(..., description="Created At")
    photo: str|None = Field(None, description="Photo")


class UserCreate(UserBase):
    password: str = Field(..., min_length=5, max_length=30)


class UserUpdate(BaseModel):
    username: str|None = None
    email: str|None = None
    password: str|None = None
    name: str|None = None
    phone: int|None = None
