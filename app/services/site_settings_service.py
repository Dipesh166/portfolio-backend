"""Site settings service."""

from typing import Optional

from app.repositories.site_settings_repo import SiteSettingsRepository
from app.schemas.site_settings import SiteSettingsResponse, SiteSettingsUpdate


class SiteSettingsService:
    """Handle site settings business logic."""

    def __init__(self, settings_repo: SiteSettingsRepository) -> None:
        self.settings_repo = settings_repo

    async def get_settings(self) -> Optional[SiteSettingsResponse]:
        """Get site settings."""
        settings = await self.settings_repo.get_settings()
        if settings:
            return SiteSettingsResponse(**settings)
        return None

    async def update_settings(self, data: SiteSettingsUpdate) -> SiteSettingsResponse:
        """Update site settings."""
        update_data = data.model_dump(exclude_unset=True)
        settings = await self.settings_repo.upsert_settings(update_data)
        return SiteSettingsResponse(**settings)
