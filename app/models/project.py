"""Project model."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class ProjectMedia(BaseModel):
    """Media object for project images."""

    file_id: str
    url: str
    alt: str = ""
    filename: str = ""
    content_type: str = "image/jpeg"
    size: int = 0


class ProjectModel(BaseModel):
    """MongoDB project document schema."""

    id: Optional[str] = Field(None, alias="_id")
    title: str
    slug: str
    short_description: str = ""
    description: str = ""
    thumbnail: Optional[ProjectMedia] = None
    images: List[ProjectMedia] = []
    technologies: List[str] = []
    github_url: str = ""
    live_url: str = ""
    featured: bool = False
    status: str = "completed"  # completed, in_progress, planned
    display_order: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {"populate_by_name": True}
