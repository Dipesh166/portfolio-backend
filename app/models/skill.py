"""Skill model."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class SkillMedia(BaseModel):
    """Media object for skill images."""

    file_id: str
    url: str
    alt: str = ""
    filename: str = ""
    content_type: str = "image/jpeg"
    size: int = 0


class SkillModel(BaseModel):
    """MongoDB skill document schema."""

    id: Optional[str] = Field(None, alias="_id")
    name: str
    category: str
    level: str = "Intermediate"  # Beginner, Intermediate, Advanced, Expert
    icon: str = ""
    image: Optional[SkillMedia] = None
    display_order: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {"populate_by_name": True}
