from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from pydantic_extra_types.phone_numbers import PhoneNumber


class UserBase(BaseModel):
    username: str = Field(..., min_length=5, max_length=20, description="Username")
    email: EmailStr|None = Field(None, description="Email")
    name: str = Field(..., min_length=5, max_length=30, description="Name")
    phone: PhoneNumber|None = Field(None, description="Phone")


class UserResponse(UserBase):
    id: int = Field(..., description="ID")
    created_at: datetime = Field(..., description="Created At")
    photo: PhoneNumber|None = Field(None, description="Photo")

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    password: str = Field(..., min_length=5)


class UserUpdate(BaseModel):
    username: str|None = Field(None, min_length=5, max_length=20, description="Username")
    email: EmailStr |None = Field(None, description="Email")
    password: str|None = Field(None, description="Hashed password")
    name: str|None = Field(None, min_length=5, max_length=30, description="Name")
    phone: PhoneNumber|None = Field(None, description="Phone")
