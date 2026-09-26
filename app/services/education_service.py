"""Education service."""

from typing import List

from app.repositories.education_repo import EducationRepository
from app.schemas.education import EducationCreate, EducationResponse, EducationUpdate


class EducationService:
    """Handle education business logic."""

    def __init__(self, education_repo: EducationRepository) -> None:
        self.education_repo = education_repo

    async def get_all(self) -> List[EducationResponse]:
        """Get all education entries."""
        education = await self.education_repo.get_all_ordered()
        return [EducationResponse(**edu) for edu in education]

    async def get_by_id(self, education_id: str) -> EducationResponse:
        """Get education by ID."""
        education = await self.education_repo.find_one_by_id(education_id)
        if not education:
            from fastapi import HTTPException, status
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Education not found",
            )
        return EducationResponse(**education)

    async def create(self, data: EducationCreate) -> EducationResponse:
        """Create a new education entry."""
        edu_data = data.model_dump()
        edu_id = await self.education_repo.insert_one(edu_data)
        education = await self.education_repo.find_one_by_id(edu_id)
        return EducationResponse(**education)

    async def update(
        self, education_id: str, data: EducationUpdate
    ) -> EducationResponse:
        """Update an education entry."""
        update_data = data.model_dump(exclude_unset=True)
        education = await self.education_repo.update_one(education_id, update_data)
        if not education:
            from fastapi import HTTPException, status
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Education not found",
            )
        return EducationResponse(**education)

    async def delete(self, education_id: str) -> bool:
        """Delete an education entry."""
        deleted = await self.education_repo.delete_one(education_id)
        if not deleted:
            from fastapi import HTTPException, status
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Education not found",
            )
        return True
