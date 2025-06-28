from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime


class ReviewBase(BaseModel):
    reviewer_name: str = Field(..., min_length=1, max_length=100)
    rating: float = Field(..., ge=1.0, le=5.0)
    comment: Optional[str] = None


class ReviewCreate(ReviewBase):
    @validator('rating')
    def validate_rating(cls, v):
        if not 1.0 <= v <= 5.0:
            raise ValueError('Rating must be between 1.0 and 5.0')
        return round(v, 1)  # Round to 1 decimal place


class ReviewResponse(ReviewBase):
    id: int
    book_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ReviewList(BaseModel):
    reviews: List[ReviewResponse]
    total: int
    book_id: int
    page: int = 1
    per_page: int = 50