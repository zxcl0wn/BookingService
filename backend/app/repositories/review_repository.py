from sqlalchemy.orm import Session
from ..models import Review
from sqlalchemy.sql import func


class ReviewRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Review]:
        return self.db.query(Review).all()

    def get_by_id(self, review_id: int) -> Review|None:
        return self.db.get(Review, review_id)

    def create(self, review: dict) -> Review:
        new_review = Review(**review)
        self.db.add(new_review)
        self.db.commit()
        self.db.refresh(new_review)
        return new_review

    def update(self, review_id, review_data: dict) -> Review|None:
        review = self.db.get(Review, review_id)
        if review:
            for key, value in review_data.items():
                if value is not None:
                    setattr(review, key, value)
            self.db.commit()
            self.db.refresh(review)
            return review
        return None

    def delete(self, review_id: int) -> Review|None:
        review = self.db.get(Review, review_id)
        if review:
            self.db.delete(review)
            self.db.commit()
            return review
        return None

    def avg_rating(self) -> float:
        sum_rating = self.db.query(func.sum(Review.rating)).scalar()
        return sum_rating / len(sum_rating)
