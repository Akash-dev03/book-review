A backend system for a Book Review application built with FastAPI, SQLAlchemy, PostgreSQL, Redis, and Docker.

## Features

- RESTful API with FastAPI
- PostgreSQL database with SQLAlchemy ORM
- Redis caching for improved performance
- Database migrations with Alembic
- Comprehensive testing with pytest
- Docker containerization
- Clean architecture with proper separation of concerns

## Quick Start

1. Clone the repository
2. Copy `.env.example` to `.env` and update values
3. Start the application:

```bash
make docker-up
```

The API will be available at http://localhost:8000

## Development

### Prerequisites
- Python 3.11+
- Docker and Docker Compose
- Make (optional, for convenience commands)

### Setup
```bash
# Install dependencies
make install

# Run development server
make dev

# Create and apply migrations
make migrate msg="Initial migration"
make upgrade

# Run tests
make test
```

## API Endpoints

- `GET /books` - List all books (with caching)
- `POST /books` - Create a new book
- `GET /books/{book_id}/reviews` - Get reviews for a book
- `POST /books/{book_id}/reviews` - Add a review to a book

## Project Structure

The project follows clean architecture principles with clear separation of concerns:
- `models/` - Database models
- `schemas/` - Pydantic schemas for validation
- `routers/` - API route handlers
- `services/` - Business logic
- `utils/` - Utility functions and dependencies
