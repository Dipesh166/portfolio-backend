"""Social link model."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class SocialLinkModel(BaseModel):
    """MongoDB social link document schema."""

    id: Optional[str] = Field(None, alias="_id")
    platform: str
    url: str
    icon: str = ""
    display_order: int = 0
    enabled: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {"populate_by_name": True}
