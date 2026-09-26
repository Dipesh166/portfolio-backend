"""Admin contact messages router."""

from typing import List

from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.database import get_database
from app.dependencies import get_current_admin
from app.repositories.contact_repo import ContactMessageRepository
from app.schemas.common import MessageResponse
from app.schemas.contact import ContactResponse
from app.services.contact_service import ContactService

router = APIRouter(prefix="/messages", tags=["Admin - Messages"])


def get_service(database: AsyncIOMotorDatabase) -> ContactService:
    return ContactService(ContactMessageRepository(database))


@router.get("", response_model=List[ContactResponse])
async def get_messages(
    database: AsyncIOMotorDatabase = Depends(get_database),
    admin: dict = Depends(get_current_admin),
):
    """Get all contact messages (admin)."""
    service = get_service(database)
    return await service.get_all()


@router.get("/unread-count")
async def get_unread_count(
    database: AsyncIOMotorDatabase = Depends(get_database),
    admin: dict = Depends(get_current_admin),
):
    """Get unread message count (admin)."""
    service = get_service(database)
    count = await service.get_unread_count()
    return {"count": count}


@router.get("/{message_id}", response_model=ContactResponse)
async def get_message(
    message_id: str,
    database: AsyncIOMotorDatabase = Depends(get_database),
    admin: dict = Depends(get_current_admin),
):
    """Get message by ID (admin)."""
    service = get_service(database)
    return await service.get_by_id(message_id)


@router.put("/{message_id}/read", response_model=ContactResponse)
async def mark_as_read(
    message_id: str,
    database: AsyncIOMotorDatabase = Depends(get_database),
    admin: dict = Depends(get_current_admin),
):
    """Mark message as read (admin)."""
    service = get_service(database)
    return await service.mark_as_read(message_id)


@router.delete("/{message_id}", response_model=MessageResponse)
async def delete_message(
    message_id: str,
    database: AsyncIOMotorDatabase = Depends(get_database),
    admin: dict = Depends(get_current_admin),
):
    """Delete message (admin)."""
    service = get_service(database)
    await service.delete(message_id)
    return MessageResponse(message="Message deleted successfully")
