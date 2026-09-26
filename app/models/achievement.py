"""Achievement model."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class AchievementModel(BaseModel):
    """MongoDB achievement document schema."""

    id: Optional[str] = Field(None, alias="_id")
    title: str
    description: str = ""
    date: str = ""  # YYYY-MM format
    url: str = ""
    icon: str = ""
    display_order: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {"populate_by_name": True}
