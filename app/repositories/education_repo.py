"""Education repository."""

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.repositories.base import BaseRepository


class EducationRepository(BaseRepository):
    """Repository for education operations."""

    def __init__(self, database: AsyncIOMotorDatabase) -> None:
        super().__init__(database["education"])

    async def get_all_ordered(self):
        """Get all education sorted by display_order."""
        return await self.find_many(sort=[("display_order", 1)])
