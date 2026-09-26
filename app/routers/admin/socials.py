"""Admin social links router."""

from typing import List

from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.database import get_database
from app.dependencies import get_current_admin
from app.repositories.social_repo import SocialLinkRepository
from app.schemas.common import MessageResponse
from app.schemas.social import SocialLinkCreate, SocialLinkResponse, SocialLinkUpdate
from app.services.social_service import SocialLinkService

router = APIRouter(prefix="/social-links", tags=["Admin - Social Links"])


def get_service(database: AsyncIOMotorDatabase) -> SocialLinkService:
    return SocialLinkService(SocialLinkRepository(database))


@router.get("", response_model=List[SocialLinkResponse])
async def get_social_links(
    database: AsyncIOMotorDatabase = Depends(get_database),
    admin: dict = Depends(get_current_admin),
):
    """Get all social links (admin)."""
    service = get_service(database)
    return await service.get_all()


@router.get("/{social_id}", response_model=SocialLinkResponse)
async def get_social_link(
    social_id: str,
    database: AsyncIOMotorDatabase = Depends(get_database),
    admin: dict = Depends(get_current_admin),
):
    """Get social link by ID (admin)."""
    service = get_service(database)
    return await service.get_by_id(social_id)


@router.post("", response_model=SocialLinkResponse, status_code=201)
async def create_social_link(
    data: SocialLinkCreate,
    database: AsyncIOMotorDatabase = Depends(get_database),
    admin: dict = Depends(get_current_admin),
):
    """Create social link (admin)."""
    service = get_service(database)
    return await service.create(data)


@router.put("/{social_id}", response_model=SocialLinkResponse)
async def update_social_link(
    social_id: str,
    data: SocialLinkUpdate,
    database: AsyncIOMotorDatabase = Depends(get_database),
    admin: dict = Depends(get_current_admin),
):
    """Update social link (admin)."""
    service = get_service(database)
    return await service.update(social_id, data)


@router.delete("/{social_id}", response_model=MessageResponse)
async def delete_social_link(
    social_id: str,
    database: AsyncIOMotorDatabase = Depends(get_database),
    admin: dict = Depends(get_current_admin),
):
    """Delete social link (admin)."""
    service = get_service(database)
    await service.delete(social_id)
    return MessageResponse(message="Social link deleted successfully")
