"""Music model."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class MusicMedia(BaseModel):
    """Media object for audio files."""

    file_id: str
    url: str
    alt: str = ""
    filename: str = ""
    content_type: str = "audio/mpeg"
    size: int = 0


class MusicModel(BaseModel):
    """MongoDB music document schema."""

    id: Optional[str] = Field(None, alias="_id")
    title: str
    artist: str = ""
    audio: Optional[MusicMedia] = None
    cover_image: Optional[MusicMedia] = None
    display_order: int = 0
    enabled: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {"populate_by_name": True}