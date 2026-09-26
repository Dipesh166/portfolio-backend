"""Site settings model."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class SEOSettings(BaseModel):
    """SEO-related settings."""

    meta_title: str = ""
    meta_description: str = ""
    og_image: str = ""
    site_url: str = ""
    google_analytics_id: str = ""


class SiteSettingsModel(BaseModel):
    """MongoDB site settings document schema."""

    id: Optional[str] = Field(None, alias="_id")
    site_name: str = "Dipesh Kumar Mandal"
    site_tagline: str = ""
    footer_text: str = ""
    maintenance_mode: bool = False
    seo: SEOSettings = SEOSettings()
    social_preview: dict = {}
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {"populate_by_name": True}
