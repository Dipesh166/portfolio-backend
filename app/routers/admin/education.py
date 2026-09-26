"""Admin education router."""

from typing import List

from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.database import get_database
from app.dependencies import get_current_admin
from app.repositories.education_repo import EducationRepository
from app.schemas.common import MessageResponse
from app.schemas.education import EducationCreate, EducationResponse, EducationUpdate
from app.services.education_service import EducationService

router = APIRouter(prefix="/education", tags=["Admin - Education"])


def get_service(database: AsyncIOMotorDatabase) -> EducationService:
    return EducationService(EducationRepository(database))


@router.get("", response_model=List[EducationResponse])
async def get_education(
    database: AsyncIOMotorDatabase = Depends(get_database),
    admin: dict = Depends(get_current_admin),
):
    """Get all education (admin)."""
    service = get_service(database)
    return await service.get_all()


@router.get("/{education_id}", response_model=EducationResponse)
async def get_education_item(
    education_id: str,
    database: AsyncIOMotorDatabase = Depends(get_database),
    admin: dict = Depends(get_current_admin),
):
    """Get education by ID (admin)."""
    service = get_service(database)
    return await service.get_by_id(education_id)


@router.post("", response_model=EducationResponse, status_code=201)
async def create_education(
    data: EducationCreate,
    database: AsyncIOMotorDatabase = Depends(get_database),
    admin: dict = Depends(get_current_admin),
):
    """Create education (admin)."""
    service = get_service(database)
    return await service.create(data)


@router.put("/{education_id}", response_model=EducationResponse)
async def update_education(
    education_id: str,
    data: EducationUpdate,
    database: AsyncIOMotorDatabase = Depends(get_database),
    admin: dict = Depends(get_current_admin),
):
    """Update education (admin)."""
    service = get_service(database)
    return await service.update(education_id, data)


@router.delete("/{education_id}", response_model=MessageResponse)
async def delete_education(
    education_id: str,
    database: AsyncIOMotorDatabase = Depends(get_database),
    admin: dict = Depends(get_current_admin),
):
    """Delete education (admin)."""
    service = get_service(database)
    await service.delete(education_id)
    return MessageResponse(message="Education deleted successfully")
