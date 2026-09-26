"""Admin experience router."""

from typing import List

from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.database import get_database
from app.dependencies import get_current_admin
from app.repositories.experience_repo import ExperienceRepository
from app.schemas.common import MessageResponse
from app.schemas.experience import ExperienceCreate, ExperienceResponse, ExperienceUpdate
from app.services.experience_service import ExperienceService

router = APIRouter(prefix="/experiences", tags=["Admin - Experience"])


def get_service(database: AsyncIOMotorDatabase) -> ExperienceService:
    return ExperienceService(ExperienceRepository(database))


@router.get("", response_model=List[ExperienceResponse])
async def get_experiences(
    database: AsyncIOMotorDatabase = Depends(get_database),
    admin: dict = Depends(get_current_admin),
):
    """Get all experiences (admin)."""
    service = get_service(database)
    return await service.get_all()


@router.get("/{experience_id}", response_model=ExperienceResponse)
async def get_experience(
    experience_id: str,
    database: AsyncIOMotorDatabase = Depends(get_database),
    admin: dict = Depends(get_current_admin),
):
    """Get experience by ID (admin)."""
    service = get_service(database)
    return await service.get_by_id(experience_id)


@router.post("", response_model=ExperienceResponse, status_code=201)
async def create_experience(
    data: ExperienceCreate,
    database: AsyncIOMotorDatabase = Depends(get_database),
    admin: dict = Depends(get_current_admin),
):
    """Create experience (admin)."""
    service = get_service(database)
    return await service.create(data)


@router.put("/{experience_id}", response_model=ExperienceResponse)
async def update_experience(
    experience_id: str,
    data: ExperienceUpdate,
    database: AsyncIOMotorDatabase = Depends(get_database),
    admin: dict = Depends(get_current_admin),
):
    """Update experience (admin)."""
    service = get_service(database)
    return await service.update(experience_id, data)


@router.delete("/{experience_id}", response_model=MessageResponse)
async def delete_experience(
    experience_id: str,
    database: AsyncIOMotorDatabase = Depends(get_database),
    admin: dict = Depends(get_current_admin),
):
    """Delete experience (admin)."""
    service = get_service(database)
    await service.delete(experience_id)
    return MessageResponse(message="Experience deleted successfully")
