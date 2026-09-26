"""Profile service."""

from typing import Optional

from app.repositories.profile_repo import ProfileRepository
from app.schemas.profile import ProfileResponse, ProfileUpdate


class ProfileService:
    """Handle profile business logic."""

    def __init__(self, profile_repo: ProfileRepository) -> None:
        self.profile_repo = profile_repo

    async def get_profile(self) -> Optional[ProfileResponse]:
        """Get the profile."""
        profile = await self.profile_repo.get_profile()
        if profile:
            return ProfileResponse(**profile)
        return None

    async def update_profile(self, data: ProfileUpdate) -> ProfileResponse:
        """Update the profile."""
        update_data = data.model_dump(exclude_unset=True)
        profile = await self.profile_repo.upsert_profile(update_data)
        return ProfileResponse(**profile)
