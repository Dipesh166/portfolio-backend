"""Site settings schemas."""

from typing import Optional

from pydantic import BaseModel


class SEOUpdate(BaseModel):
    """SEO settings update."""

    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    og_image: Optional[str] = None
    site_url: Optional[str] = None
    google_analytics_id: Optional[str] = None


class SiteSettingsUpdate(BaseModel):
    """Site settings update request."""

    site_name: Optional[str] = None
    site_tagline: Optional[str] = None
    footer_text: Optional[str] = None
    maintenance_mode: Optional[bool] = None
    seo: Optional[SEOUpdate] = None


class SiteSettingsResponse(BaseModel):
    """Site settings response."""

    id: str
    site_name: str
    site_tagline: str
    footer_text: str
    maintenance_mode: bool
    seo: dict

    model_config = {"from_attributes": True}
