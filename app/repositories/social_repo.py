"""Social link repository."""

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.repositories.base import BaseRepository


class SocialLinkRepository(BaseRepository):
    """Repository for social link operations."""

    def __init__(self, database: AsyncIOMotorDatabase) -> None:
        super().__init__(database["social_links"])

    async def get_all_ordered(self):
        """Get all social links sorted by display_order."""
        return await self.find_many(sort=[("display_order", 1)])

    async def get_enabled(self):
        """Get only enabled social links."""
        return await self.find_many(
            query={"enabled": True}, sort=[("display_order", 1)]
        )
