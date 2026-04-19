from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from ..services import ReviewService
from ..schemas import ReviewResponse, ReviewCreate, ReviewUpdate
from ..database import get_db


router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"]
)

@router.get("/", response_model=list[ReviewResponse])
async def get_reviews(db: AsyncSession = Depends(get_db)):
    service = ReviewService(db)
    return await service.get_all()


@router.get("/{review_id}", response_model=ReviewResponse)
async def get_review(review_id: int, db: AsyncSession = Depends(get_db)):
    service = ReviewService(db)
    return await service.get_by_id(review_id)


@router.post("/", response_model=ReviewResponse)
async def create_review(review: ReviewCreate, db: AsyncSession = Depends(get_db)):  # TODO
    service = ReviewService(db)
    return await service.create(review)


@router.put("/{review_id}", response_model=ReviewResponse)
async def put_review(review_id: int, review_data: ReviewUpdate, db: AsyncSession = Depends(get_db)):
    service = ReviewService(db)
    return await service.update(review_id, review_data)


@router.delete("/{review_id}", response_model=ReviewResponse)
async def delete_review(review_id: int, db: AsyncSession = Depends(get_db)):
    service = ReviewService(db)
    return await service.delete(review_id)
