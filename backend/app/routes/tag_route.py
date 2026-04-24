from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas import TagResponse, TagCreate, TagUpdate
from ..core.database import get_db
from ..services import TagService


router = APIRouter(
    prefix="/tags",
    tags=["Tags"]
)


@router.get("/", response_model=list[TagResponse])
async def get_tags(db: AsyncSession = Depends(get_db)):
    service = TagService(db)
    return await service.get_all()


@router.get("/{tag_id}", response_model=TagResponse)
async def get_tag(tag_id: int, db: AsyncSession = Depends(get_db)):
    service = TagService(db)
    return await service.get_by_id(tag_id)


@router.post("/", response_model=TagResponse)
async def create_tag(tag: TagCreate, db: AsyncSession = Depends(get_db)):
    service = TagService(db)
    return await service.create(tag)


@router.put("/{tag_id}", response_model=TagResponse)
async def create_tag(tag_id: int, tag: TagUpdate, db: AsyncSession = Depends(get_db)):
    service = TagService(db)
    return await service.update(tag_id, tag)


@router.delete("/{tag_id}", response_model=TagResponse)
async def delete_tag(tag_id: int, db: AsyncSession = Depends(get_db)):
    service = TagService(db)
    return await service.delete(tag_id)
