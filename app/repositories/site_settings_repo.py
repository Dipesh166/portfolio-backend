"""Site settings repository."""

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.repositories.base import BaseRepository


class SiteSettingsRepository(BaseRepository):
    """Repository for site settings operations."""

    def __init__(self, database: AsyncIOMotorDatabase) -> None:
        super().__init__(database["site_settings"])

    async def get_settings(self):
        """Get the single settings document."""
        return await self.find_one({})

    async def upsert_settings(self, settings_data: dict):
        """Create or update site settings."""
        existing = await self.get_settings()
        if existing:
            return await self.update_one(existing["id"], settings_data)
        settings_id = await self.insert_one(settings_data)
        return await self.find_one_by_id(settings_id)
