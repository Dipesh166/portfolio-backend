"""Experience model."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class ExperienceModel(BaseModel):
    """MongoDB experience document schema."""

    id: Optional[str] = Field(None, alias="_id")
    company: str
    position: str
    employment_type: str = "Full-time"
    location: str = ""
    start_date: str  # YYYY-MM format
    end_date: Optional[str] = None  # YYYY-MM or null if current
    is_current: bool = False
    description: str = ""
    technologies: List[str] = []
    company_url: str = ""
    logo: Optional[dict] = None
    display_order: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {"populate_by_name": True}
