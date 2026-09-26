"""Certification model."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class CertificationMedia(BaseModel):
    """Media object for certificate images."""

    file_id: str
    url: str
    alt: str = ""
    filename: str = ""
    content_type: str = "image/jpeg"
    size: int = 0


class CertificationModel(BaseModel):
    """MongoDB certification document schema."""

    id: Optional[str] = Field(None, alias="_id")
    title: str
    issuer: str
    issue_date: str  # YYYY-MM format
    credential_id: str = ""
    credential_url: str = ""
    certificate_image: Optional[CertificationMedia] = None
    display_order: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {"populate_by_name": True}
