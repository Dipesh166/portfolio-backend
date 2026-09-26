"""Skill schemas."""

from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.common import MediaObject


class SkillCreate(BaseModel):
    """Skill create request."""

    name: str = Field(..., min_length=1)
    category: str = Field(..., min_length=1)
    level: str = "Intermediate"
    icon: str = ""
    image: Optional[MediaObject] = None
    display_order: int = 0


class SkillUpdate(BaseModel):
    """Skill update request."""

    name: Optional[str] = Field(None, min_length=1)
    category: Optional[str] = Field(None, min_length=1)
    level: Optional[str] = None
    icon: Optional[str] = None
    image: Optional[MediaObject] = None
    display_order: Optional[int] = None


class SkillResponse(BaseModel):
    """Skill response."""

    id: str
    name: str
    category: str
    level: str
    icon: str
    image: Optional[MediaObject] = None
    display_order: int

    model_config = {"from_attributes": True}
