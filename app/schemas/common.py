"""Common shared schemas."""

from typing import Any, Generic, List, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class MediaObject(BaseModel):
    """Reusable media object for images."""

    file_id: str
    url: str
    alt: str = ""
    filename: str = ""
    content_type: str = "image/jpeg"
    size: int = 0


class MessageResponse(BaseModel):
    """Standard message response."""

    message: str
    success: bool = True


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated list response."""

    items: List[T]
    total: int
    page: int
    pages: int


class ErrorResponse(BaseModel):
    """Standard error response."""

    detail: str
    success: bool = False
