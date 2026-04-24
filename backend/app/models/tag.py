from sqlalchemy import Column, String, Integer
from ..core.database import Base


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, nullable=False)
