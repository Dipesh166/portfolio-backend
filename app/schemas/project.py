"""Project schemas."""

from typing import List, Optional

from pydantic import BaseModel, Field

from app.schemas.common import MediaObject


class ProjectCreate(BaseModel):
    """Project create request."""

    title: str = Field(..., min_length=1)
    slug: str = Field(..., min_length=1)
    short_description: str = ""
    description: str = ""
    thumbnail: Optional[MediaObject] = None
    images: List[MediaObject] = []
    technologies: List[str] = []
    github_url: str = ""
    live_url: str = ""
    featured: bool = False
    status: str = "completed"
    display_order: int = 0


class ProjectUpdate(BaseModel):
    """Project update request."""

    title: Optional[str] = Field(None, min_length=1)
    slug: Optional[str] = Field(None, min_length=1)
    short_description: Optional[str] = None
    description: Optional[str] = None
    thumbnail: Optional[MediaObject] = None
    images: Optional[List[MediaObject]] = None
    technologies: Optional[List[str]] = None
    github_url: Optional[str] = None
    live_url: Optional[str] = None
    featured: Optional[bool] = None
    status: Optional[str] = None
    display_order: Optional[int] = None


class ProjectResponse(BaseModel):
    """Project response."""

    id: str
    title: str
    slug: str
    short_description: str
    description: str
    thumbnail: Optional[MediaObject] = None
    images: List[MediaObject]
    technologies: List[str]
    github_url: str
    live_url: str
    featured: bool
    status: str
    display_order: int

    model_config = {"from_attributes": True}
