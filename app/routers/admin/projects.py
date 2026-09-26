"""Admin project router."""

from typing import List

from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.database import get_database
from app.dependencies import get_current_admin
from app.repositories.project_repo import ProjectRepository
from app.schemas.common import MessageResponse
from app.schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate
from app.services.project_service import ProjectService

router = APIRouter(prefix="/projects", tags=["Admin - Projects"])


def get_service(database: AsyncIOMotorDatabase) -> ProjectService:
    return ProjectService(ProjectRepository(database))


@router.get("", response_model=List[ProjectResponse])
async def get_projects(
    database: AsyncIOMotorDatabase = Depends(get_database),
    admin: dict = Depends(get_current_admin),
):
    """Get all projects (admin)."""
    service = get_service(database)
    return await service.get_all()


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: str,
    database: AsyncIOMotorDatabase = Depends(get_database),
    admin: dict = Depends(get_current_admin),
):
    """Get project by ID (admin)."""
    service = get_service(database)
    return await service.get_by_id(project_id)


@router.post("", response_model=ProjectResponse, status_code=201)
async def create_project(
    data: ProjectCreate,
    database: AsyncIOMotorDatabase = Depends(get_database),
    admin: dict = Depends(get_current_admin),
):
    """Create project (admin)."""
    service = get_service(database)
    return await service.create(data)


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: str,
    data: ProjectUpdate,
    database: AsyncIOMotorDatabase = Depends(get_database),
    admin: dict = Depends(get_current_admin),
):
    """Update project (admin)."""
    service = get_service(database)
    return await service.update(project_id, data)


@router.delete("/{project_id}", response_model=MessageResponse)
async def delete_project(
    project_id: str,
    database: AsyncIOMotorDatabase = Depends(get_database),
    admin: dict = Depends(get_current_admin),
):
    """Delete project (admin)."""
    service = get_service(database)
    await service.delete(project_id)
    return MessageResponse(message="Project deleted successfully")
