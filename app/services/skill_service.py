"""Skill service."""

from typing import List

from app.repositories.skill_repo import SkillRepository
from app.schemas.skill import SkillCreate, SkillResponse, SkillUpdate


class SkillService:
    """Handle skill business logic."""

    def __init__(self, skill_repo: SkillRepository) -> None:
        self.skill_repo = skill_repo

    async def get_all(self) -> List[SkillResponse]:
        """Get all skills."""
        skills = await self.skill_repo.get_all_ordered()
        return [SkillResponse(**skill) for skill in skills]

    async def get_by_category(self, category: str) -> List[SkillResponse]:
        """Get skills by category."""
        skills = await self.skill_repo.get_by_category(category)
        return [SkillResponse(**skill) for skill in skills]

    async def get_by_id(self, skill_id: str) -> SkillResponse:
        """Get skill by ID."""
        skill = await self.skill_repo.find_one_by_id(skill_id)
        if not skill:
            from fastapi import HTTPException, status
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Skill not found",
            )
        return SkillResponse(**skill)

    async def create(self, data: SkillCreate) -> SkillResponse:
        """Create a new skill."""
        skill_data = data.model_dump()
        skill_id = await self.skill_repo.insert_one(skill_data)
        skill = await self.skill_repo.find_one_by_id(skill_id)
        return SkillResponse(**skill)

    async def update(self, skill_id: str, data: SkillUpdate) -> SkillResponse:
        """Update a skill."""
        update_data = data.model_dump(exclude_unset=True)
        skill = await self.skill_repo.update_one(skill_id, update_data)
        if not skill:
            from fastapi import HTTPException, status
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Skill not found",
            )
        return SkillResponse(**skill)

    async def delete(self, skill_id: str) -> bool:
        """Delete a skill."""
        deleted = await self.skill_repo.delete_one(skill_id)
        if not deleted:
            from fastapi import HTTPException, status
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Skill not found",
            )
        return True
