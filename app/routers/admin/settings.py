"""Admin site settings router."""

from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.database import get_database
from app.dependencies import get_current_admin
from app.repositories.site_settings_repo import SiteSettingsRepository
from app.schemas.site_settings import SiteSettingsResponse, SiteSettingsUpdate
from app.services.site_settings_service import SiteSettingsService

router = APIRouter(prefix="/settings", tags=["Admin - Settings"])


def get_service(database: AsyncIOMotorDatabase) -> SiteSettingsService:
    return SiteSettingsService(SiteSettingsRepository(database))


@router.get("", response_model=SiteSettingsResponse)
async def get_settings(
    database: AsyncIOMotorDatabase = Depends(get_database),
    admin: dict = Depends(get_current_admin),
):
    """Get site settings (admin)."""
    service = get_service(database)
    settings = await service.get_settings()
    if not settings:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Settings not found",
        )
    return settings


@router.put("", response_model=SiteSettingsResponse)
async def update_settings(
    data: SiteSettingsUpdate,
    database: AsyncIOMotorDatabase = Depends(get_database),
    admin: dict = Depends(get_current_admin),
):
    """Update site settings (admin)."""
    service = get_service(database)
    return await service.update_settings(data)
