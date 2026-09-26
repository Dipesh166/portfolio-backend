"""Social link schemas."""

from typing import Optional

from pydantic import BaseModel, Field


class SocialLinkCreate(BaseModel):
    """Social link create request."""

    platform: str = Field(..., min_length=1)
    url: str = Field(..., min_length=1)
    icon: str = ""
    display_order: int = 0
    enabled: bool = True


class SocialLinkUpdate(BaseModel):
    """Social link update request."""

    platform: Optional[str] = Field(None, min_length=1)
    url: Optional[str] = Field(None, min_length=1)
    icon: Optional[str] = None
    display_order: Optional[int] = None
    enabled: Optional[bool] = None


class SocialLinkResponse(BaseModel):
    """Social link response."""

    id: str
    platform: str
    url: str
    icon: str
    display_order: int
    enabled: bool

    model_config = {"from_attributes": True}
