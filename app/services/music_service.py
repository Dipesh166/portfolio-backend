"""Music service."""

from typing import List, Optional

from fastapi import HTTPException, status

from app.repositories.music_repo import MusicRepository
from app.schemas.music import MusicCreate, MusicResponse, MusicUpdate
from app.services.media_service import MediaService


class MusicService:
    """Handle music business logic."""

    def __init__(
        self,
        music_repo: MusicRepository,
        media_service: Optional[MediaService] = None,
    ) -> None:
        self.music_repo = music_repo
        self.media_service = media_service or MediaService()

    async def get_all(self) -> List[MusicResponse]:
        """Get all music tracks."""
        tracks = await self.music_repo.get_all_ordered()
        return [MusicResponse(**track) for track in tracks]

    async def get_enabled(self) -> List[MusicResponse]:
        """Get enabled music tracks."""
        tracks = await self.music_repo.get_enabled()
        return [MusicResponse(**track) for track in tracks]

    async def get_by_id(self, music_id: str) -> MusicResponse:
        """Get music track by ID."""
        track = await self.music_repo.find_one_by_id(music_id)
        if not track:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Music track not found",
            )
        return MusicResponse(**track)

    async def create(self, data: MusicCreate) -> MusicResponse:
        """Create a new music track."""
        track_data = data.model_dump()
        track_id = await self.music_repo.insert_one(track_data)
        track = await self.music_repo.find_one_by_id(track_id)
        return MusicResponse(**track)

    async def update(self, music_id: str, data: MusicUpdate) -> MusicResponse:
        """Update a music track."""
        update_data = data.model_dump(exclude_unset=True)
        existing = await self.music_repo.find_one_by_id(music_id)
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Music track not found",
            )

        # Clean up old media files if they were replaced or removed.
        await self._cleanup_replaced(existing, "audio", update_data)
        await self._cleanup_replaced(existing, "cover_image", update_data)

        track = await self.music_repo.update_one(music_id, update_data)
        return MusicResponse(**track)

    async def delete(self, music_id: str) -> bool:
        """Delete a music track and its media files."""
        existing = await self.music_repo.find_one_by_id(music_id)
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Music track not found",
            )

        deleted = await self.music_repo.delete_one(music_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Music track not found",
            )

        for field in ("audio", "cover_image"):
            media = existing.get(field)
            if media and media.get("file_id"):
                await self._delete_file(media["file_id"])
        return True

    async def _cleanup_replaced(
        self, existing: dict, field: str, update_data: dict
    ) -> None:
        """Delete the old media file for a field that was replaced or cleared."""
        if field not in update_data:
            return
        old_media = existing.get(field)
        new_media = update_data.get(field)
        old_file_id = old_media.get("file_id") if old_media else None
        new_file_id = new_media.get("file_id") if new_media else None
        if old_file_id and old_file_id != new_file_id:
            await self._delete_file(old_file_id)

    async def _delete_file(self, file_id: str) -> None:
        """Delete a stored media file, ignoring errors."""
        try:
            await self.media_service.delete(file_id)
        except Exception:
            pass