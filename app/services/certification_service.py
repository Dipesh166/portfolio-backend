"""Certification service."""

from typing import List

from app.repositories.certification_repo import CertificationRepository
from app.schemas.certification import (
    CertificationCreate,
    CertificationResponse,
    CertificationUpdate,
)


class CertificationService:
    """Handle certification business logic."""

    def __init__(self, certification_repo: CertificationRepository) -> None:
        self.certification_repo = certification_repo

    async def get_all(self) -> List[CertificationResponse]:
        """Get all certifications."""
        certifications = await self.certification_repo.get_all_ordered()
        return [CertificationResponse(**cert) for cert in certifications]

    async def get_by_id(self, certification_id: str) -> CertificationResponse:
        """Get certification by ID."""
        certification = await self.certification_repo.find_one_by_id(certification_id)
        if not certification:
            from fastapi import HTTPException, status
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Certification not found",
            )
        return CertificationResponse(**certification)

    async def create(self, data: CertificationCreate) -> CertificationResponse:
        """Create a new certification."""
        cert_data = data.model_dump()
        cert_id = await self.certification_repo.insert_one(cert_data)
        certification = await self.certification_repo.find_one_by_id(cert_id)
        return CertificationResponse(**certification)

    async def update(
        self, certification_id: str, data: CertificationUpdate
    ) -> CertificationResponse:
        """Update a certification."""
        update_data = data.model_dump(exclude_unset=True)
        certification = await self.certification_repo.update_one(
            certification_id, update_data
        )
        if not certification:
            from fastapi import HTTPException, status
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Certification not found",
            )
        return CertificationResponse(**certification)

    async def delete(self, certification_id: str) -> bool:
        """Delete a certification."""
        deleted = await self.certification_repo.delete_one(certification_id)
        if not deleted:
            from fastapi import HTTPException, status
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Certification not found",
            )
        return True
