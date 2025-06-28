from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime


class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    author: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    isbn: Optional[str] = Field(None, min_length=10, max_length=13)
    published_year: Optional[int] = Field(None, ge=1000, le=2024)


class BookCreate(BookBase):
    @validator('isbn')
    def validate_isbn(cls, v):
        if v and not (v.isdigit() and len(v) in [10, 13]):
            raise ValueError('ISBN must be 10 or 13 digits')
        return v


class BookResponse(BookBase):
    id: int
    average_rating: float
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class BookList(BaseModel):
    books: List[BookResponse]
    total: int
    page: int = 1
    per_page: int = 50