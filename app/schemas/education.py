"""Education schemas."""

from typing import Optional

from pydantic import BaseModel, Field


class EducationCreate(BaseModel):
    """Education create request."""

    institution: str = Field(..., min_length=1)
    degree: str = Field(..., min_length=1)
    field: str = ""
    start_date: str = Field(..., pattern=r"^\d{4}-\d{2}$")
    end_date: Optional[str] = Field(None, pattern=r"^\d{4}-\d{2}$")
    description: str = ""
    grade: str = ""
    location: str = ""
    logo: Optional[dict] = None
    display_order: int = 0


class EducationUpdate(BaseModel):
    """Education update request."""

    institution: Optional[str] = Field(None, min_length=1)
    degree: Optional[str] = Field(None, min_length=1)
    field: Optional[str] = None
    start_date: Optional[str] = Field(None, pattern=r"^\d{4}-\d{2}$")
    end_date: Optional[str] = Field(None, pattern=r"^\d{4}-\d{2}$")
    description: Optional[str] = None
    grade: Optional[str] = None
    location: Optional[str] = None
    logo: Optional[dict] = None
    display_order: Optional[int] = None


class EducationResponse(BaseModel):
    """Education response."""

    id: str
    institution: str
    degree: str
    field: str
    start_date: str
    end_date: Optional[str] = None
    description: str
    grade: str
    location: str
    logo: Optional[dict] = None
    display_order: int

    model_config = {"from_attributes": True}
