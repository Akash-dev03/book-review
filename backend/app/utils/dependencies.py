from sqlalchemy.orm import Session
from app.database import get_db


def get_database_session() -> Session:
    """Get database session dependency"""
    return next(get_db())