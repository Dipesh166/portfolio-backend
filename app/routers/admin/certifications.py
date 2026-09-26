"""Admin certification router."""

from typing import List

from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.database import get_database
from app.dependencies import get_current_admin
from app.repositories.certification_repo import CertificationRepository
from app.schemas.common import MessageResponse
from app.schemas.certification import (
    CertificationCreate,
    CertificationResponse,
    CertificationUpdate,
)
from app.services.certification_service import CertificationService

router = APIRouter(prefix="/certifications", tags=["Admin - Certifications"])


def get_service(database: AsyncIOMotorDatabase) -> CertificationService:
    return CertificationService(CertificationRepository(database))


@router.get("", response_model=List[CertificationResponse])
async def get_certifications(
    database: AsyncIOMotorDatabase = Depends(get_database),
    admin: dict = Depends(get_current_admin),
):
    """Get all certifications (admin)."""
    service = get_service(database)
    return await service.get_all()


@router.get("/{certification_id}", response_model=CertificationResponse)
async def get_certification(
    certification_id: str,
    database: AsyncIOMotorDatabase = Depends(get_database),
    admin: dict = Depends(get_current_admin),
):
    """Get certification by ID (admin)."""
    service = get_service(database)
    return await service.get_by_id(certification_id)


@router.post("", response_model=CertificationResponse, status_code=201)
async def create_certification(
    data: CertificationCreate,
    database: AsyncIOMotorDatabase = Depends(get_database),
    admin: dict = Depends(get_current_admin),
):
    """Create certification (admin)."""
    service = get_service(database)
    return await service.create(data)


@router.put("/{certification_id}", response_model=CertificationResponse)
async def update_certification(
    certification_id: str,
    data: CertificationUpdate,
    database: AsyncIOMotorDatabase = Depends(get_database),
    admin: dict = Depends(get_current_admin),
):
    """Update certification (admin)."""
    service = get_service(database)
    return await service.update(certification_id, data)


@router.delete("/{certification_id}", response_model=MessageResponse)
async def delete_certification(
    certification_id: str,
    database: AsyncIOMotorDatabase = Depends(get_database),
    admin: dict = Depends(get_current_admin),
):
    """Delete certification (admin)."""
    service = get_service(database)
    await service.delete(certification_id)
    return MessageResponse(message="Certification deleted successfully")
