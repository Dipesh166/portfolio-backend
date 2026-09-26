"""Profile repository."""

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.repositories.base import BaseRepository


class ProfileRepository(BaseRepository):
    """Repository for profile operations."""

    def __init__(self, database: AsyncIOMotorDatabase) -> None:
        super().__init__(database["profile"])

    async def get_profile(self):
        """Get the single profile document."""
        return await self.find_one({})

    async def upsert_profile(self, profile_data: dict):
        """Create or update the profile."""
        existing = await self.get_profile()
        if existing:
            return await self.update_one(existing["id"], profile_data)
        profile_id = await self.insert_one(profile_data)
        return await self.find_one_by_id(profile_id)
