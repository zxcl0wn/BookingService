from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from ..auth.services.auth_services import get_current_user
from ..models import User
from ..schemas import BookingResponse, BookingCreate, BookingUpdate, ReviewCreate, ReviewResponse
from ..services import BookingService, ReviewService
from ..database import get_db


router = APIRouter(
    prefix="/booking",
    tags=["Booking"]
)

@router.get("/", response_model=list[BookingResponse])
async def get_bookings(db: AsyncSession = Depends(get_db)):
    service = BookingService(db)
    return await service.get_all()


@router.get("/{booking_id}", response_model=BookingResponse)
async def get_booking(booking_id: int, db: AsyncSession = Depends(get_db)):
    service = BookingService(db)
    return await service.get_by_id(booking_id)


@router.post("/{room_id}", response_model=BookingResponse)
async def create_booking(
        booking: BookingCreate,
        room_id: int,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    service = BookingService(db)
    return await service.create(booking, room_id, current_user.id)


@router.put("/{booking_id}", response_model=BookingResponse)
async def put_booking(
        booking_id: int,
        booking_data: BookingUpdate,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    service = BookingService(db)
    return await service.update(booking_id, booking_data, current_user.id)


@router.delete("/{booking_id}", response_model=BookingResponse)
async def delete_booking(
        booking_id: int,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    service = BookingService(db)
    return await service.delete(booking_id, current_user.id)


@router.post("/{booking_id}/review", response_model=ReviewResponse)
async def create_review(
        review: ReviewCreate,
        booking_id: int,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    service = ReviewService(db)
    return await service.create(review, booking_id, current_user.id)

# TODO: 1. Перенести эндпоинт в room, провести миграции