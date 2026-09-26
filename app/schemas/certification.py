"""Certification schemas."""

from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.common import MediaObject


class CertificationCreate(BaseModel):
    """Certification create request."""

    title: str = Field(..., min_length=1)
    issuer: str = Field(..., min_length=1)
    issue_date: str = Field(..., pattern=r"^\d{4}-\d{2}$")
    credential_id: str = ""
    credential_url: str = ""
    certificate_image: Optional[MediaObject] = None
    display_order: int = 0


class CertificationUpdate(BaseModel):
    """Certification update request."""

    title: Optional[str] = Field(None, min_length=1)
    issuer: Optional[str] = Field(None, min_length=1)
    issue_date: Optional[str] = Field(None, pattern=r"^\d{4}-\d{2}$")
    credential_id: Optional[str] = None
    credential_url: Optional[str] = None
    certificate_image: Optional[MediaObject] = None
    display_order: Optional[int] = None


class CertificationResponse(BaseModel):
    """Certification response."""

    id: str
    title: str
    issuer: str
    issue_date: str
    credential_id: str
    credential_url: str
    certificate_image: Optional[MediaObject] = None
    display_order: int

    model_config = {"from_attributes": True}
