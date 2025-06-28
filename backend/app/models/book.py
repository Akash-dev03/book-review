from sqlalchemy import Column, Integer, String, Text, Float
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin


class Book(Base, TimestampMixin):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    author = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    isbn = Column(String(13), unique=True, index=True)
    published_year = Column(Integer)
    average_rating = Column(Float, default=0.0)
    
    # Relationship
    reviews = relationship("Review", back_populates="book", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}', author='{self.author}')>"
