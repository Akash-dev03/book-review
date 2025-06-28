from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

from app.config import settings
from app.database import engine, create_tables
from app.cache import init_cache
from app.routers import books, reviews
from app.exceptions import CustomHTTPException


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    create_tables()
    await init_cache()
    yield
    # Shutdown
    pass


app = FastAPI(
    title="Book Review API",
    description="A professional book review system",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(books.router, prefix="/books", tags=["books"])
app.include_router(reviews.router, prefix="/books", tags=["reviews"])


@app.exception_handler(CustomHTTPException)
async def custom_http_exception_handler(request, exc: CustomHTTPException):
    return HTTPException(status_code=exc.status_code, detail=exc.detail)


@app.get("/")
async def root():
    return {"message": "Book Review API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )