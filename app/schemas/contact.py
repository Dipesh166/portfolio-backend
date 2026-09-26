"""Contact message schemas."""

from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class ContactCreate(BaseModel):
    """Contact form request (public)."""

    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    subject: str = Field("", max_length=200)
    message: str = Field(..., min_length=10, max_length=5000)


class ContactResponse(BaseModel):
    """Contact message response (admin)."""

    id: str
    name: str
    email: str
    subject: str
    message: str
    is_read: bool
    created_at: str

    model_config = {"from_attributes": True}
