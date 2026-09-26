"""Admin authentication schemas."""

from pydantic import BaseModel, EmailStr, Field


class AdminLogin(BaseModel):
    """Admin login request."""

    email: EmailStr
    password: str = Field(..., min_length=6)


class AdminToken(BaseModel):
    """JWT token response."""

    access_token: str
    token_type: str = "bearer"


class AdminResponse(BaseModel):
    """Admin user response (without password)."""

    id: str
    email: str
    full_name: str
    is_active: bool


class AdminCreate(BaseModel):
    """Admin creation request."""

    email: EmailStr
    password: str = Field(..., min_length=6)
    full_name: str = Field(..., min_length=1)
