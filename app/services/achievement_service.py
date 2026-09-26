"""Achievement service."""

from typing import List

from app.repositories.achievement_repo import AchievementRepository
from app.schemas.achievement import (
    AchievementCreate,
    AchievementResponse,
    AchievementUpdate,
)


class AchievementService:
    """Handle achievement business logic."""

    def __init__(self, achievement_repo: AchievementRepository) -> None:
        self.achievement_repo = achievement_repo

    async def get_all(self) -> List[AchievementResponse]:
        """Get all achievements."""
        achievements = await self.achievement_repo.get_all_ordered()
        return [AchievementResponse(**ach) for ach in achievements]

    async def get_by_id(self, achievement_id: str) -> AchievementResponse:
        """Get achievement by ID."""
        achievement = await self.achievement_repo.find_one_by_id(achievement_id)
        if not achievement:
            from fastapi import HTTPException, status
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Achievement not found",
            )
        return AchievementResponse(**achievement)

    async def create(self, data: AchievementCreate) -> AchievementResponse:
        """Create a new achievement."""
        ach_data = data.model_dump()
        ach_id = await self.achievement_repo.insert_one(ach_data)
        achievement = await self.achievement_repo.find_one_by_id(ach_id)
        return AchievementResponse(**achievement)

    async def update(
        self, achievement_id: str, data: AchievementUpdate
    ) -> AchievementResponse:
        """Update an achievement."""
        update_data = data.model_dump(exclude_unset=True)
        achievement = await self.achievement_repo.update_one(
            achievement_id, update_data
        )
        if not achievement:
            from fastapi import HTTPException, status
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Achievement not found",
            )
        return AchievementResponse(**achievement)

    async def delete(self, achievement_id: str) -> bool:
        """Delete an achievement."""
        deleted = await self.achievement_repo.delete_one(achievement_id)
        if not deleted:
            from fastapi import HTTPException, status
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Achievement not found",
            )
        return True
