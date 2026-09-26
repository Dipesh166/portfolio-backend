"""Admin profile router."""

from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.database import get_database
from app.dependencies import get_current_admin
from app.repositories.profile_repo import ProfileRepository
from app.schemas.profile import ProfileResponse, ProfileUpdate
from app.services.profile_service import ProfileService

router = APIRouter(prefix="/profile", tags=["Admin - Profile"])


def get_profile_service(database: AsyncIOMotorDatabase) -> ProfileService:
    return ProfileService(ProfileRepository(database))


@router.get("", response_model=ProfileResponse)
async def get_profile(
    database: AsyncIOMotorDatabase = Depends(get_database),
    admin: dict = Depends(get_current_admin),
):
    """Get profile (admin)."""
    service = get_profile_service(database)
    profile = await service.get_profile()
    if not profile:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found",
        )
    return profile


@router.put("", response_model=ProfileResponse)
async def update_profile(
    data: ProfileUpdate,
    database: AsyncIOMotorDatabase = Depends(get_database),
    admin: dict = Depends(get_current_admin),
):
    """Update profile (admin)."""
    service = get_profile_service(database)
    return await service.update_profile(data)
