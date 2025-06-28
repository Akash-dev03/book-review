from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.book import BookCreate, BookResponse, BookList
from app.services.book_service import BookService
from app.exceptions import BookNotFoundError

router = APIRouter()


@router.get("/", response_model=BookList)
async def get_books(
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get all books with caching"""
    try:
        book_service = BookService(db)
        result = await book_service.get_books_cached(page=page, per_page=per_page)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=BookResponse, status_code=201)
async def create_book(
    book: BookCreate,
    db: Session = Depends(get_db)
):
    """Create a new book"""
    try:
        book_service = BookService(db)
        new_book = await book_service.create_book(book)
        return new_book
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{book_id}", response_model=BookResponse)
async def get_book(
    book_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific book by ID"""
    try:
        book_service = BookService(db)
        book = book_service.get_book_by_id(book_id)
        if not book:
            raise BookNotFoundError(book_id)
        return book
    except BookNotFoundError:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))