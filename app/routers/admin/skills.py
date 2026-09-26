"""Admin skill router."""

from typing import List

from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.database import get_database
from app.dependencies import get_current_admin
from app.repositories.skill_repo import SkillRepository
from app.schemas.common import MessageResponse
from app.schemas.skill import SkillCreate, SkillResponse, SkillUpdate
from app.services.skill_service import SkillService

router = APIRouter(prefix="/skills", tags=["Admin - Skills"])


def get_service(database: AsyncIOMotorDatabase) -> SkillService:
    return SkillService(SkillRepository(database))


@router.get("", response_model=List[SkillResponse])
async def get_skills(
    database: AsyncIOMotorDatabase = Depends(get_database),
    admin: dict = Depends(get_current_admin),
):
    """Get all skills (admin)."""
    service = get_service(database)
    return await service.get_all()


@router.get("/{skill_id}", response_model=SkillResponse)
async def get_skill(
    skill_id: str,
    database: AsyncIOMotorDatabase = Depends(get_database),
    admin: dict = Depends(get_current_admin),
):
    """Get skill by ID (admin)."""
    service = get_service(database)
    return await service.get_by_id(skill_id)


@router.post("", response_model=SkillResponse, status_code=201)
async def create_skill(
    data: SkillCreate,
    database: AsyncIOMotorDatabase = Depends(get_database),
    admin: dict = Depends(get_current_admin),
):
    """Create skill (admin)."""
    service = get_service(database)
    return await service.create(data)


@router.put("/{skill_id}", response_model=SkillResponse)
async def update_skill(
    skill_id: str,
    data: SkillUpdate,
    database: AsyncIOMotorDatabase = Depends(get_database),
    admin: dict = Depends(get_current_admin),
):
    """Update skill (admin)."""
    service = get_service(database)
    return await service.update(skill_id, data)


@router.delete("/{skill_id}", response_model=MessageResponse)
async def delete_skill(
    skill_id: str,
    database: AsyncIOMotorDatabase = Depends(get_database),
    admin: dict = Depends(get_current_admin),
):
    """Delete skill (admin)."""
    service = get_service(database)
    await service.delete(skill_id)
    return MessageResponse(message="Skill deleted successfully")
