from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.review import Review
from app.schemas.review import ReviewCreate, ReviewResponse, ReviewList
from app.services.book_service import BookService


class ReviewService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_review_by_id(self, review_id: int) -> Optional[Review]:
        """Get a review by ID"""
        return self.db.query(Review).filter(Review.id == review_id).first()
    
    def get_reviews_by_book(self, book_id: int, page: int = 1, per_page: int = 50) -> ReviewList:
        """Get reviews for a specific book with pagination"""
        offset = (page - 1) * per_page
        
        reviews = (
            self.db.query(Review)
            .filter(Review.book_id == book_id)
            .order_by(Review.created_at.desc())
            .offset(offset)
            .limit(per_page)
            .all()
        )
        
        total = self.db.query(Review).filter(Review.book_id == book_id).count()
        
        return ReviewList(
            reviews=reviews,
            total=total,
            book_id=book_id,
            page=page,
            per_page=per_page
        )
    
    async def create_review(self, book_id: int, review_data: ReviewCreate) -> Review:
        """Create a new review for a book"""
        review = Review(book_id=book_id, **review_data.dict())
        self.db.add(review)
        self.db.commit()
        self.db.refresh(review)
        
        # Update book's average rating
        book_service = BookService(self.db)
        book_service.update_average_rating(book_id)
        
        # Invalidate books cache since average rating changed
        await book_service._invalidate_books_cache()
        
        return review