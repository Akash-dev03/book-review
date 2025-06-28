````markdown
# 📚 Book Review Backend System

A scalable and production-ready **backend system for a Book Review application**, built using **FastAPI**, **PostgreSQL**, **Redis**, **SQLAlchemy**, and **Docker**, following clean architecture and modern Python best practices.

---

## 🚀 Features

- ✅ FastAPI-based high-performance RESTful API
- ✅ PostgreSQL + SQLAlchemy ORM for robust database management
- ✅ Redis caching to enhance response speed and reduce DB load
- ✅ Alembic for version-controlled database migrations
- ✅ Pytest for thorough and modular test coverage
- ✅ Dockerized setup for easy deployment and isolation
- ✅ Clean, maintainable architecture (models, services, routers, schemas)

---

## ⚙️ Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/Akash-dev03/book-review.git
cd book-review
````

### 2. Set up environment

```bash
cp .env.example .env
# Update values like DB credentials, Redis URL, etc.
```

### 3. Run using Docker

```bash
make docker-up
```

The API will be accessible at:
➡️ **[http://localhost:8000](http://localhost:8000)**

---

## 💻 Local Development

### 📋 Prerequisites

* Python 3.11+
* Docker & Docker Compose
* Make (recommended for quick commands)

### 🛠️ Setup & Commands

```bash
# Install dependencies locally (optional if using outside Docker)
make install

# Run development server
make dev

# Apply database migrations
make migrate msg="Initial migration"
make upgrade

# Run tests
make test
```

---

## 📚 API Endpoints

| Method | Endpoint                   | Description                         |
| ------ | -------------------------- | ----------------------------------- |
| GET    | `/books`                   | List all books (supports caching)   |
| POST   | `/books`                   | Create a new book                   |
| GET    | `/books/{book_id}`         | Get details of a specific book      |
| GET    | `/books/{book_id}/reviews` | Get all reviews for a specific book |
| POST   | `/books/{book_id}/reviews` | Add a review to a book              |

---

## 🧱 Project Structure

```
app/
├── routers/       # Route definitions (books, reviews)
├── models/        # SQLAlchemy database models
├── schemas/       # Pydantic models for request/response validation
├── services/      # Business logic
├── database.py    # DB setup & session handling
├── cache.py       # Redis cache helpers
└── main.py        # FastAPI app entry point

tests/
├── test_books.py
├── test_reviews.py
└── test_integration.py
```

---

## 🧪 Testing

The project includes comprehensive test coverage using `pytest`.

```bash
make test
```

Test Features:

* Unit and integration test cases
* Isolated test DB
* Fixtures for sample data
* Mocked cache for consistent test results

---

## 📦 Deployment

This project is Dockerized and ready to deploy on platforms like **Render**, **Railway**, or **Fly.io**.

To run in production mode:

```bash
make docker-up
```

---

## ✅ Assessment Notes

This project was developed as part of a backend development assessment.

**What it demonstrates:**

* Deep understanding of backend architecture
* Clean code with modular separation of concerns
* Redis integration and caching strategy
* API validation and error handling with FastAPI
* Full testing strategy using Pytest
* Hands-on Docker and Makefile usage

---

## 📫 Contact

Developed by **Akash**

📧 Email: \[[a03akash@gmail.com](mailto:a03akash@gmail.com)]

🔗 GitHub: [github.com/Akash-dev03](https://github.com/Akash-dev03)

🔗 Portfolio https://portfolio-akashs-projects-2b49a841.vercel.app/

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
