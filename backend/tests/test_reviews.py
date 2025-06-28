import pytest
from fastapi.testclient import TestClient


@pytest.mark.asyncio
async def test_create_review(client: TestClient, sample_book_data, sample_review_data):
    """Test creating a new review"""
    # Create a book first
    book_response = client.post("/books/", json=sample_book_data)
    book_id = book_response.json()["id"]
    
    # Create a review
    response = client.post(f"/books/{book_id}/reviews", json=sample_review_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["reviewer_name"] == sample_review_data["reviewer_name"]
    assert data["rating"] == sample_review_data["rating"]
    assert data["book_id"] == book_id
    assert "id" in data
    assert "created_at" in data


def test_create_review_for_nonexistent_book(client: TestClient, sample_review_data):
    """Test creating a review for a non-existent book"""
    response = client.post("/books/999/reviews", json=sample_review_data)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_reviews_empty(client: TestClient, sample_book_data):
    """Test getting reviews when there are none"""
    # Create a book first
    book_response = client.post("/books/", json=sample_book_data)
    book_id = book_response.json()["id"]
    
    response = client.get(f"/books/{book_id}/reviews")
    
    assert response.status_code == 200
    data = response.json()
    assert data["reviews"] == []
    assert data["total"] == 0
    assert data["book_id"] == book_id


@pytest.mark.asyncio
async def test_get_reviews_with_data(client: TestClient, sample_book_data, sample_review_data):
    """Test getting reviews with data"""
    # Create a book first
    book_response = client.post("/books/", json=sample_book_data)
    book_id = book_response.json()["id"]
    
    # Create a review
    client.post(f"/books/{book_id}/reviews", json=sample_review_data)
    
    response = client.get(f"/books/{book_id}/reviews")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data["reviews"]) == 1
    assert data["total"] == 1
    assert data["reviews"][0]["reviewer_name"] == sample_review_data["reviewer_name"]


def test_create_review_invalid_rating(client: TestClient, sample_book_data):
    """Test creating a review with invalid rating"""
    # Create a book first
    book_response = client.post("/books/", json=sample_book_data)
    book_id = book_response.json()["id"]
    
    invalid_review_data = {
        "reviewer_name": "Test Reviewer",
        "rating": 6.0,  # Invalid rating (should be 1-5)
        "comment": "Invalid rating test"
    }
    
    response = client.post(f"/books/{book_id}/reviews", json=invalid_review_data)
    assert response.status_code == 422


def test_get_reviews_for_nonexistent_book(client: TestClient):
    """Test getting reviews for a non-existent book"""
    response = client.get("/books/999/reviews")
    assert response.status_code == 404

