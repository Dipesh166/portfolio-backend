"""Profile model."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ProfileMedia(BaseModel):
    """Media object for profile images."""

    file_id: str
    url: str
    alt: str = ""
    filename: str = ""
    content_type: str = "image/jpeg"
    size: int = 0


class ProfileModel(BaseModel):
    """MongoDB profile document schema."""

    id: Optional[str] = Field(None, alias="_id")
    name: str
    headline: str
    short_bio: str = ""
    about: str = ""
    profile_image: Optional[ProfileMedia] = None
    resume: Optional[ProfileMedia] = None
    location: str = ""
    email: str = ""
    phone: str = ""
    resume_url: str = ""
    availability: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {"populate_by_name": True}
