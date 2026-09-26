"""Admin achievement router."""

from typing import List

from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.database import get_database
from app.dependencies import get_current_admin
from app.repositories.achievement_repo import AchievementRepository
from app.schemas.achievement import (
    AchievementCreate,
    AchievementResponse,
    AchievementUpdate,
)
from app.schemas.common import MessageResponse
from app.services.achievement_service import AchievementService

router = APIRouter(prefix="/achievements", tags=["Admin - Achievements"])


def get_service(database: AsyncIOMotorDatabase) -> AchievementService:
    return AchievementService(AchievementRepository(database))


@router.get("", response_model=List[AchievementResponse])
async def get_achievements(
    database: AsyncIOMotorDatabase = Depends(get_database),
    admin: dict = Depends(get_current_admin),
):
    """Get all achievements (admin)."""
    service = get_service(database)
    return await service.get_all()


@router.get("/{achievement_id}", response_model=AchievementResponse)
async def get_achievement(
    achievement_id: str,
    database: AsyncIOMotorDatabase = Depends(get_database),
    admin: dict = Depends(get_current_admin),
):
    """Get achievement by ID (admin)."""
    service = get_service(database)
    return await service.get_by_id(achievement_id)


@router.post("", response_model=AchievementResponse, status_code=201)
async def create_achievement(
    data: AchievementCreate,
    database: AsyncIOMotorDatabase = Depends(get_database),
    admin: dict = Depends(get_current_admin),
):
    """Create achievement (admin)."""
    service = get_service(database)
    return await service.create(data)


@router.put("/{achievement_id}", response_model=AchievementResponse)
async def update_achievement(
    achievement_id: str,
    data: AchievementUpdate,
    database: AsyncIOMotorDatabase = Depends(get_database),
    admin: dict = Depends(get_current_admin),
):
    """Update achievement (admin)."""
    service = get_service(database)
    return await service.update(achievement_id, data)


@router.delete("/{achievement_id}", response_model=MessageResponse)
async def delete_achievement(
    achievement_id: str,
    database: AsyncIOMotorDatabase = Depends(get_database),
    admin: dict = Depends(get_current_admin),
):
    """Delete achievement (admin)."""
    service = get_service(database)
    await service.delete(achievement_id)
    return MessageResponse(message="Achievement deleted successfully")
