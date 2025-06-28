from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.review import ReviewCreate, ReviewResponse, ReviewList
from app.services.review_service import ReviewService
from app.services.book_service import BookService
from app.exceptions import BookNotFoundError

router = APIRouter()


@router.get("/{book_id}/reviews", response_model=ReviewList)
async def get_book_reviews(
    book_id: int,
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get all reviews for a specific book"""
    try:
        # Check if book exists
        book_service = BookService(db)
        book = book_service.get_book_by_id(book_id)
        if not book:
            raise BookNotFoundError(book_id)
        
        review_service = ReviewService(db)
        result = review_service.get_reviews_by_book(
            book_id=book_id, 
            page=page, 
            per_page=per_page
        )
        return result
    except BookNotFoundError:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{book_id}/reviews", response_model=ReviewResponse, status_code=201)
async def create_review(
    book_id: int,
    review: ReviewCreate,
    db: Session = Depends(get_db)
):
    """Add a new review to a book"""
    try:
        # Check if book exists
        book_service = BookService(db)
        book = book_service.get_book_by_id(book_id)
        if not book:
            raise BookNotFoundError(book_id)
        
        review_service = ReviewService(db)
        new_review = await review_service.create_review(book_id, review)
        return new_review
    except BookNotFoundError:
        raise
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))