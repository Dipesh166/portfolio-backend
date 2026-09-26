"""Experience service."""

from typing import List

from app.repositories.experience_repo import ExperienceRepository
from app.schemas.experience import ExperienceCreate, ExperienceResponse, ExperienceUpdate


class ExperienceService:
    """Handle experience business logic."""

    def __init__(self, experience_repo: ExperienceRepository) -> None:
        self.experience_repo = experience_repo

    async def get_all(self) -> List[ExperienceResponse]:
        """Get all experiences."""
        experiences = await self.experience_repo.get_all_ordered()
        return [ExperienceResponse(**exp) for exp in experiences]

    async def get_by_id(self, experience_id: str) -> ExperienceResponse:
        """Get experience by ID."""
        experience = await self.experience_repo.find_one_by_id(experience_id)
        if not experience:
            from fastapi import HTTPException, status
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Experience not found",
            )
        return ExperienceResponse(**experience)

    async def create(self, data: ExperienceCreate) -> ExperienceResponse:
        """Create a new experience."""
        exp_data = data.model_dump()
        exp_id = await self.experience_repo.insert_one(exp_data)
        experience = await self.experience_repo.find_one_by_id(exp_id)
        return ExperienceResponse(**experience)

    async def update(
        self, experience_id: str, data: ExperienceUpdate
    ) -> ExperienceResponse:
        """Update an experience."""
        update_data = data.model_dump(exclude_unset=True)
        experience = await self.experience_repo.update_one(experience_id, update_data)
        if not experience:
            from fastapi import HTTPException, status
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Experience not found",
            )
        return ExperienceResponse(**experience)

    async def delete(self, experience_id: str) -> bool:
        """Delete an experience."""
        deleted = await self.experience_repo.delete_one(experience_id)
        if not deleted:
            from fastapi import HTTPException, status
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Experience not found",
            )
        return True
