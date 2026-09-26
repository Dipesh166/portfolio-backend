"""Education model."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class EducationModel(BaseModel):
    """MongoDB education document schema."""

    id: Optional[str] = Field(None, alias="_id")
    institution: str
    degree: str
    field: str = ""
    start_date: str  # YYYY-MM format
    end_date: Optional[str] = None
    description: str = ""
    grade: str = ""
    location: str = ""
    logo: Optional[dict] = None
    display_order: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {"populate_by_name": True}
