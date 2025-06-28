import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.cache import get_cache, set_cache


@pytest.mark.asyncio
async def test_books_cache_miss_flow(client: TestClient, sample_book_data):
    """Test that cache miss flows correctly fetch from DB and set cache"""
    
    # Mock cache to simulate cache miss
    with patch('app.cache.get_cache', return_value=None) as mock_get_cache, \
         patch('app.cache.set_cache', return_value=True) as mock_set_cache:
        
        # Create a book first
        client.post("/books/", json=sample_book_data)
        
        # Get books - should trigger cache miss
        response = client.get("/books/")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["books"]) == 1
        assert data["total"] == 1
        
        # Verify cache was checked
        mock_get_cache.assert_called_once()
        
        # Verify cache was set after DB fetch
        mock_set_cache.assert_called_once()


@pytest.mark.asyncio
async def test_full_book_review_workflow(client: TestClient, sample_book_data, sample_review_data):
    """Test complete workflow: create book, add review, verify average rating update"""
    
    # Step 1: Create a book
    book_response = client.post("/books/", json=sample_book_data)
    assert book_response.status_code == 201
    book_id = book_response.json()["id"]
    initial_rating = book_response.json()["average_rating"]
    assert initial_rating == 0.0
    
    # Step 2: Add a review
    review_response = client.post(f"/books/{book_id}/reviews", json=sample_review_data)
    assert review_response.status_code == 201
    
    # Step 3: Verify book's average rating was updated
    updated_book_response = client.get(f"/books/{book_id}")
    assert updated_book_response.status_code == 200
    updated_rating = updated_book_response.json()["average_rating"]
    assert updated_rating == sample_review_data["rating"]
    
    # Step 4: Add another review
    second_review_data = {
        "reviewer_name": "Another Reviewer",
        "rating": 3.0,
        "comment": "It was okay"
    }
    client.post(f"/books/{book_id}/reviews", json=second_review_data)
    
    # Step 5: Verify average rating calculation
    final_book_response = client.get(f"/books/{book_id}")
    final_rating = final_book_response.json()["average_rating"]
    expected_avg = (sample_review_data["rating"] + second_review_data["rating"]) / 2
    assert abs(final_rating - expected_avg) < 0.1  # Allow for floating point precision
    
    # Step 6: Verify reviews are retrieved correctly
    reviews_response = client.get(f"/books/{book_id}/reviews")
    assert reviews_response.status_code == 200
    reviews_data = reviews_response.json()
    assert reviews_data["total"] == 2
    assert len(reviews_data["reviews"]) == 2


@pytest.mark.asyncio
async def test_pagination_and_caching(client: TestClient):
    """Test pagination works correctly with caching"""
    
    # Create multiple books
    books_data = [
        {"title": f"Book {i}", "author": f"Author {i}", "published_year": 2020 + i}
        for i in range(1, 6)  # Create 5 books
    ]
    
    for book_data in books_data:
        client.post("/books/", json=book_data)
    
    # Test pagination
    response1 = client.get("/books/?page=1&per_page=3")
    assert response1.status_code == 200
    data1 = response1.json()
    assert len(data1["books"]) == 3
    assert data1["total"] == 5
    assert data1["page"] == 1
    
    response2 = client.get("/books/?page=2&per_page=3")
    assert response2.status_code == 200
    data2 = response2.json()
    assert len(data2["books"]) == 2  # Remaining books
    assert data2["total"] == 5
    assert data2["page"] == 2


@pytest.mark.asyncio
async def test_error_handling(client: TestClient):
    """Test various error scenarios"""
    
    # Test invalid book creation
    invalid_book = {
        "title": "",  # Empty title
        "author": "Test Author"
    }
    response = client.post("/books/", json=invalid_book)
    assert response.status_code == 422
    
    # Test duplicate ISBN
    book_data = {
        "title": "Test Book",
        "author": "Test Author",
        "isbn": "1234567890123"
    }
    
    # Create first book
    response1 = client.post("/books/", json=book_data)
    assert response1.status_code == 201
    
    # Try to create duplicate
    response2 = client.post("/books/", json=book_data)
    assert response2.status_code == 422
    
    # Test invalid review rating
    book_id = response1.json()["id"]
    invalid_review = {
        "reviewer_name": "Test Reviewer",
        "rating": 0.5,  # Below minimum
        "comment": "Invalid rating"
    }
    
    response3 = client.post(f"/books/{book_id}/reviews", json=invalid_review)
    assert response3.status_code == 422