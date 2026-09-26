"""Admin user model."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, EmailStr


class AdminModel(BaseModel):
    """MongoDB admin document schema."""

    id: Optional[str] = Field(None, alias="_id")
    email: EmailStr
    hashed_password: str
    full_name: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {"populate_by_name": True}
