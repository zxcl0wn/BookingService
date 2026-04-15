from pydantic import BaseModel, Field


class RoomPhotoResponse(BaseModel):
    id: int = Field(..., description="ID")
    room_id: int = Field(..., description="Room ID")
    photo_url: str = Field(..., description="Photo URL")
    is_main: bool = Field(..., description="Is main photo")

    class Config:
        from_attributes = True


class RoomPhotoUpdate(BaseModel):
    is_main: bool|None = Field(None, description="Is main photo")
