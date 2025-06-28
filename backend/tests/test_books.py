import pytest
from fastapi.testclient import TestClient
from app.models.book import Book


@pytest.mark.asyncio
async def test_create_book(client: TestClient, sample_book_data):
    """Test creating a new book"""
    response = client.post("/books/", json=sample_book_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == sample_book_data["title"]
    assert data["author"] == sample_book_data["author"]
    assert data["isbn"] == sample_book_data["isbn"]
    assert "id" in data
    assert "created_at" in data


@pytest.mark.asyncio
async def test_get_books_empty(client: TestClient):
    """Test getting books when database is empty"""
    response = client.get("/books/")
    
    assert response.status_code == 200
    data = response.json()
    assert data["books"] == []
    assert data["total"] == 0
    assert data["page"] == 1


@pytest.mark.asyncio
async def test_get_books_with_data(client: TestClient, sample_book_data):
    """Test getting books with data"""
    # Create a book first
    client.post("/books/", json=sample_book_data)
    
    response = client.get("/books/")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data["books"]) == 1
    assert data["total"] == 1
    assert data["books"][0]["title"] == sample_book_data["title"]


def test_create_book_invalid_isbn(client: TestClient):
    """Test creating a book with invalid ISBN"""
    invalid_book_data = {
        "title": "Test Book",
        "author": "Test Author",
        "isbn": "invalid-isbn"
    }
    
    response = client.post("/books/", json=invalid_book_data)
    assert response.status_code == 422


def test_get_book_not_found(client: TestClient):
    """Test getting a non-existent book"""
    response = client.get("/books/999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_book_by_id(client: TestClient, sample_book_data):
    """Test getting a specific book by ID"""
    # Create a book first
    create_response = client.post("/books/", json=sample_book_data)
    book_id = create_response.json()["id"]
    
    response = client.get(f"/books/{book_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == book_id
    assert data["title"] == sample_book_data["title"]