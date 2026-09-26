"""Contact message model."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ContactMessageModel(BaseModel):
    """MongoDB contact message document schema."""

    id: Optional[str] = Field(None, alias="_id")
    name: str
    email: str
    subject: str = ""
    message: str
    is_read: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {"populate_by_name": True}
