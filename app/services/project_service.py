"""Project service."""

from typing import List

from app.repositories.project_repo import ProjectRepository
from app.schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate


class ProjectService:
    """Handle project business logic."""

    def __init__(self, project_repo: ProjectRepository) -> None:
        self.project_repo = project_repo

    async def get_all(self) -> List[ProjectResponse]:
        """Get all projects."""
        projects = await self.project_repo.get_all_ordered()
        return [ProjectResponse(**proj) for proj in projects]

    async def get_featured(self) -> List[ProjectResponse]:
        """Get featured projects."""
        projects = await self.project_repo.get_featured()
        return [ProjectResponse(**proj) for proj in projects]

    async def get_by_id(self, project_id: str) -> ProjectResponse:
        """Get project by ID."""
        project = await self.project_repo.find_one_by_id(project_id)
        if not project:
            from fastapi import HTTPException, status
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found",
            )
        return ProjectResponse(**project)

    async def get_by_slug(self, slug: str) -> ProjectResponse:
        """Get project by slug."""
        project = await self.project_repo.find_by_slug(slug)
        if not project:
            from fastapi import HTTPException, status
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found",
            )
        return ProjectResponse(**project)

    async def create(self, data: ProjectCreate) -> ProjectResponse:
        """Create a new project."""
        proj_data = data.model_dump()
        proj_id = await self.project_repo.insert_one(proj_data)
        project = await self.project_repo.find_one_by_id(proj_id)
        return ProjectResponse(**project)

    async def update(self, project_id: str, data: ProjectUpdate) -> ProjectResponse:
        """Update a project."""
        update_data = data.model_dump(exclude_unset=True)
        project = await self.project_repo.update_one(project_id, update_data)
        if not project:
            from fastapi import HTTPException, status
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found",
            )
        return ProjectResponse(**project)

    async def delete(self, project_id: str) -> bool:
        """Delete a project."""
        deleted = await self.project_repo.delete_one(project_id)
        if not deleted:
            from fastapi import HTTPException, status
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found",
            )
        return True
