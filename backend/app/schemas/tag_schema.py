from pydantic import Field, BaseModel


class TagBase(BaseModel):
    title: str = Field(..., description="Tag title")


class TagResponse(TagBase):
    id: int = Field(..., description="ID")


class TagCreate(TagBase):
    ...


class TagUpdate(BaseModel):
    title: str|None = None