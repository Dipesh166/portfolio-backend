"""Profile schemas."""

from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.common import MediaObject


class ProfileUpdate(BaseModel):
    """Profile update request."""

    name: Optional[str] = Field(None, min_length=1)
    headline: Optional[str] = None
    short_bio: Optional[str] = None
    about: Optional[str] = None
    profile_image: Optional[MediaObject] = None
    resume: Optional[MediaObject] = None
    location: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    resume_url: Optional[str] = None
    availability: Optional[bool] = None


class ProfileResponse(BaseModel):
    """Profile response."""

    id: str
    name: str
    headline: str
    short_bio: str = ""
    about: str = ""
    profile_image: Optional[MediaObject] = None
    resume: Optional[MediaObject] = None
    location: str = ""
    email: str = ""
    phone: str = ""
    resume_url: str = ""
    availability: bool = True

    model_config = {"from_attributes": True}
