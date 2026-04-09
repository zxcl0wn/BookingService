from sqlalchemy.orm import Session
from ..models import Booking


class BookingRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(self) -> list[Booking]:
        return self.db.query(Booking).all()

    def get_by_id(self, booking_id: int) -> Booking|None:
        return self.db.get(Booking, booking_id)

    def create(self, booking: dict) -> Booking:
        new_booking = Booking(**booking)
        self.db.add(new_booking)
        self.db.commit()
        self.db.refresh(new_booking)
        return new_booking

    def update(self, booking_id: int, booking_data: dict) -> Booking|None:
        booking = self.db.get(Booking, booking_id)
        if booking:
            for key, value in booking_data.items():
                if value is not None:
                    setattr(booking, key, value)
            self.db.commit()
            self.db.refresh(booking)
            return booking
        return None

    def delete(self, booking_id) -> Booking|None:
        booking = self.db.get(Booking, booking_id)
        if booking:
            self.db.delete(booking)
            self.db.commit()
            return booking
        return None