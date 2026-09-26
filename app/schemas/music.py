"""Music schemas."""

from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.common import MediaObject


class MusicCreate(BaseModel):
    """Music create request."""

    title: str = Field(..., min_length=1)
    artist: str = ""
    audio: Optional[MediaObject] = None
    cover_image: Optional[MediaObject] = None
    display_order: int = 0
    enabled: bool = True


class MusicUpdate(BaseModel):
    """Music update request."""

    title: Optional[str] = Field(None, min_length=1)
    artist: Optional[str] = None
    audio: Optional[MediaObject] = None
    cover_image: Optional[MediaObject] = None
    display_order: Optional[int] = None
    enabled: Optional[bool] = None


class MusicResponse(BaseModel):
    """Music response."""

    id: str
    title: str
    artist: str
    audio: Optional[MediaObject] = None
    cover_image: Optional[MediaObject] = None
    display_order: int
    enabled: bool

    model_config = {"from_attributes": True}