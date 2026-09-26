"""Contact message repository."""

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.repositories.base import BaseRepository


class ContactMessageRepository(BaseRepository):
    """Repository for contact message operations."""

    def __init__(self, database: AsyncIOMotorDatabase) -> None:
        super().__init__(database["contact_messages"])

    async def get_all_ordered(self):
        """Get all messages sorted by creation date (newest first)."""
        return await self.find_many(sort=[("created_at", -1)])

    async def get_unread_count(self) -> int:
        """Get count of unread messages."""
        return await self.count_documents({"is_read": False})

    async def mark_as_read(self, message_id: str):
        """Mark a message as read."""
        return await self.update_one(message_id, {"is_read": True})
