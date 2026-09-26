"""Achievement schemas."""

from typing import Optional

from pydantic import BaseModel, Field


class AchievementCreate(BaseModel):
    """Achievement create request."""

    title: str = Field(..., min_length=1)
    description: str = ""
    date: str = ""
    url: str = ""
    icon: str = ""
    display_order: int = 0


class AchievementUpdate(BaseModel):
    """Achievement update request."""

    title: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = None
    date: Optional[str] = None
    url: Optional[str] = None
    icon: Optional[str] = None
    display_order: Optional[int] = None


class AchievementResponse(BaseModel):
    """Achievement response."""

    id: str
    title: str
    description: str
    date: str
    url: str
    icon: str
    display_order: int

    model_config = {"from_attributes": True}
