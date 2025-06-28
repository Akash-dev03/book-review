from fastapi import HTTPException


class CustomHTTPException(HTTPException):
    """Custom HTTP Exception with additional context"""
    def __init__(self, status_code: int, detail: str, context: dict = None):
        super().__init__(status_code, detail)
        self.context = context or {}


class BookNotFoundError(CustomHTTPException):
    def __init__(self, book_id: int):
        super().__init__(
            status_code=404,
            detail=f"Book with id {book_id} not found",
            context={"book_id": book_id}
        )


class ValidationError(CustomHTTPException):
    def __init__(self, detail: str, field: str = None):
        super().__init__(
            status_code=422,
            detail=detail,
            context={"field": field} if field else {}
        )