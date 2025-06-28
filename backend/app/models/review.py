from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin


class Review(Base, TimestampMixin):
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    reviewer_name = Column(String(100), nullable=False)
    rating = Column(Float, nullable=False)  # 1.0 to 5.0
    comment = Column(Text)
    
    # Relationship
    book = relationship("Book", back_populates="reviews")
    
    def __repr__(self):
        return f"<Review(id={self.id}, book_id={self.book_id}, rating={self.rating})>"

# app/schemas/__init__.py
from app.schemas.book import BookCreate, BookResponse, BookList
from app.schemas.review import ReviewCreate, ReviewResponse, ReviewList

__all__ = [
    "BookCreate", "BookResponse", "BookList",
    "ReviewCreate", "ReviewResponse", "ReviewList"
]