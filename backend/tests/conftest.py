import pytest
import asyncio
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import get_db, Base
from app.cache import init_cache
from app.models import book, review  # Ensure models are registered

# ✅ Use appropriate PostgreSQL URL
SQLALCHEMY_DATABASE_URL = (
    "test_database_url"
)

# ✅ Correct engine config for PostgreSQL (no SQLite-specific settings)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ Dependency override
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


# ✅ Sync fixture since TestClient is sync
@pytest.fixture(scope="function")
def client():
    """Create a test client"""
    Base.metadata.create_all(bind=engine)

    # Run async init_cache inside sync context
    asyncio.run(init_cache())

    with TestClient(app) as test_client:
        yield test_client

    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Create a database session for testing"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def sample_book_data():
    """Sample book data for testing"""
    return {
        "title": "Test Book",
        "author": "Test Author",
        "description": "A test book for testing purposes",
        "isbn": "1234567890123",
        "published_year": 2023
    }


@pytest.fixture
def sample_review_data():
    """Sample review data for testing"""
    return {
        "reviewer_name": "Test Reviewer",
        "rating": 4.5,
        "comment": "Great book! Highly recommended."
    }
