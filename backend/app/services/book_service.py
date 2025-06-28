from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
import json

from app.models.book import Book
from app.schemas.book import BookCreate, BookResponse, BookList
from app.cache import get_cache, set_cache, delete_cache


class BookService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_book_by_id(self, book_id: int) -> Optional[Book]:
        """Get a book by ID"""
        return self.db.query(Book).filter(Book.id == book_id).first()
    
    def get_books(self, page: int = 1, per_page: int = 50) -> BookList:
        """Get books with pagination"""
        offset = (page - 1) * per_page
        
        books = self.db.query(Book).offset(offset).limit(per_page).all()
        total = self.db.query(Book).count()
        
        return BookList(
            books=books,
            total=total,
            page=page,
            per_page=per_page
        )
    
    async def get_books_cached(self, page: int = 1, per_page: int = 50) -> BookList:
        """Get books with caching"""
        cache_key = f"books:page:{page}:per_page:{per_page}"
        
        # Try to get from cache
        cached_result = await get_cache(cache_key)
        if cached_result:
            return BookList(**cached_result)
        
        # Cache miss - fetch from database
        result = self.get_books(page, per_page)
        
        # Convert to dict for caching
        result_dict = {
            "books": [book.__dict__ for book in result.books],
            "total": result.total,
            "page": result.page,
            "per_page": result.per_page
        }
        
        # Clean SQLAlchemy internal attributes
        for book in result_dict["books"]:
            book.pop("_sa_instance_state", None)
        
        # Set cache
        await set_cache(cache_key, result_dict)
        
        return result
    
    async def create_book(self, book_data: BookCreate) -> Book:
        """Create a new book"""
        # Check if ISBN already exists
        if book_data.isbn:
            existing = self.db.query(Book).filter(Book.isbn == book_data.isbn).first()
            if existing:
                raise ValueError(f"Book with ISBN {book_data.isbn} already exists")
        
        book = Book(**book_data.dict())
        self.db.add(book)
        self.db.commit()
        self.db.refresh(book)
        
        # Invalidate cache
        await self._invalidate_books_cache()
        
        return book
    
    def update_average_rating(self, book_id: int):
        """Update the average rating for a book"""
        from app.models.review import Review
        
        avg_rating = self.db.query(func.avg(Review.rating)).filter(
            Review.book_id == book_id
        ).scalar()
        
        book = self.get_book_by_id(book_id)
        if book:
            book.average_rating = round(avg_rating or 0.0, 1)
            self.db.commit()
    
    async def _invalidate_books_cache(self):
        """Invalidate all books cache entries"""
        # In a real application, you might want to use cache patterns or tags
        # For now, we'll delete common cache keys
        for page in range(1, 10):  # Clear first 10 pages
            for per_page in [10, 25, 50, 100]:
                cache_key = f"books:page:{page}:per_page:{per_page}"
                await delete_cache(cache_key)