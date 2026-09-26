"""Experience schemas."""

from typing import List, Optional

from pydantic import BaseModel, Field


class ExperienceCreate(BaseModel):
    """Experience create request."""

    company: str = Field(..., min_length=1)
    position: str = Field(..., min_length=1)
    employment_type: str = "Full-time"
    location: str = ""
    start_date: str = Field(..., pattern=r"^\d{4}-\d{2}$")
    end_date: Optional[str] = Field(None, pattern=r"^\d{4}-\d{2}$")
    is_current: bool = False
    description: str = ""
    technologies: List[str] = []
    company_url: str = ""
    logo: Optional[dict] = None
    display_order: int = 0


class ExperienceUpdate(BaseModel):
    """Experience update request."""

    company: Optional[str] = Field(None, min_length=1)
    position: Optional[str] = Field(None, min_length=1)
    employment_type: Optional[str] = None
    location: Optional[str] = None
    start_date: Optional[str] = Field(None, pattern=r"^\d{4}-\d{2}$")
    end_date: Optional[str] = Field(None, pattern=r"^\d{4}-\d{2}$")
    is_current: Optional[bool] = None
    description: Optional[str] = None
    technologies: Optional[List[str]] = None
    company_url: Optional[str] = None
    logo: Optional[dict] = None
    display_order: Optional[int] = None


class ExperienceResponse(BaseModel):
    """Experience response."""

    id: str
    company: str
    position: str
    employment_type: str
    location: str
    start_date: str
    end_date: Optional[str] = None
    is_current: bool
    description: str
    technologies: List[str]
    company_url: str
    logo: Optional[dict] = None
    display_order: int

    model_config = {"from_attributes": True}
