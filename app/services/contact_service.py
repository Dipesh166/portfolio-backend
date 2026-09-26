"""Contact message service."""

from typing import List

from app.repositories.contact_repo import ContactMessageRepository
from app.schemas.contact import ContactCreate, ContactResponse


class ContactService:
    """Handle contact message business logic."""

    def __init__(self, contact_repo: ContactMessageRepository) -> None:
        self.contact_repo = contact_repo

    async def get_all(self) -> List[ContactResponse]:
        """Get all messages."""
        messages = await self.contact_repo.get_all_ordered()
        return [
            ContactResponse(
                id=str(msg.get("id", "")),
                name=msg.get("name", ""),
                email=msg.get("email", ""),
                subject=msg.get("subject", ""),
                message=msg.get("message", ""),
                is_read=msg.get("is_read", False),
                created_at=str(msg.get("created_at", "")),
            )
            for msg in messages
        ]

    async def get_by_id(self, message_id: str) -> ContactResponse:
        """Get message by ID."""
        message = await self.contact_repo.find_one_by_id(message_id)
        if not message:
            from fastapi import HTTPException, status
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Message not found",
            )
        return ContactResponse(
            id=str(message.get("id", "")),
            name=message.get("name", ""),
            email=message.get("email", ""),
            subject=message.get("subject", ""),
            message=message.get("message", ""),
            is_read=message.get("is_read", False),
            created_at=str(message.get("created_at", "")),
        )

    async def create(self, data: ContactCreate) -> ContactResponse:
        """Create a new contact message."""
        msg_data = data.model_dump()
        msg_id = await self.contact_repo.insert_one(msg_data)
        message = await self.contact_repo.find_one_by_id(msg_id)
        return ContactResponse(
            id=str(message.get("id", "")),
            name=message.get("name", ""),
            email=message.get("email", ""),
            subject=message.get("subject", ""),
            message=message.get("message", ""),
            is_read=message.get("is_read", False),
            created_at=str(message.get("created_at", "")),
        )

    async def mark_as_read(self, message_id: str) -> ContactResponse:
        """Mark a message as read."""
        message = await self.contact_repo.mark_as_read(message_id)
        if not message:
            from fastapi import HTTPException, status
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Message not found",
            )
        return await self.get_by_id(message_id)

    async def delete(self, message_id: str) -> bool:
        """Delete a message."""
        deleted = await self.contact_repo.delete_one(message_id)
        if not deleted:
            from fastapi import HTTPException, status
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Message not found",
            )
        return True

    async def get_unread_count(self) -> int:
        """Get count of unread messages."""
        return await self.contact_repo.get_unread_count()
