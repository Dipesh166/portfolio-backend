"""Social link service."""

from typing import List

from app.repositories.social_repo import SocialLinkRepository
from app.schemas.social import SocialLinkCreate, SocialLinkResponse, SocialLinkUpdate


class SocialLinkService:
    """Handle social link business logic."""

    def __init__(self, social_repo: SocialLinkRepository) -> None:
        self.social_repo = social_repo

    async def get_all(self) -> List[SocialLinkResponse]:
        """Get all social links."""
        socials = await self.social_repo.get_all_ordered()
        return [SocialLinkResponse(**s) for s in socials]

    async def get_enabled(self) -> List[SocialLinkResponse]:
        """Get enabled social links."""
        socials = await self.social_repo.get_enabled()
        return [SocialLinkResponse(**s) for s in socials]

    async def get_by_id(self, social_id: str) -> SocialLinkResponse:
        """Get social link by ID."""
        social = await self.social_repo.find_one_by_id(social_id)
        if not social:
            from fastapi import HTTPException, status
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Social link not found",
            )
        return SocialLinkResponse(**social)

    async def create(self, data: SocialLinkCreate) -> SocialLinkResponse:
        """Create a new social link."""
        social_data = data.model_dump()
        social_id = await self.social_repo.insert_one(social_data)
        social = await self.social_repo.find_one_by_id(social_id)
        return SocialLinkResponse(**social)

    async def update(
        self, social_id: str, data: SocialLinkUpdate
    ) -> SocialLinkResponse:
        """Update a social link."""
        update_data = data.model_dump(exclude_unset=True)
        social = await self.social_repo.update_one(social_id, update_data)
        if not social:
            from fastapi import HTTPException, status
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Social link not found",
            )
        return SocialLinkResponse(**social)

    async def delete(self, social_id: str) -> bool:
        """Delete a social link."""
        deleted = await self.social_repo.delete_one(social_id)
        if not deleted:
            from fastapi import HTTPException, status
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Social link not found",
            )
        return True
