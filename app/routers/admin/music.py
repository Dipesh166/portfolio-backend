"""Admin music router."""

from typing import List

from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.database import get_database
from app.dependencies import get_current_admin
from app.repositories.music_repo import MusicRepository
from app.schemas.common import MessageResponse
from app.schemas.music import MusicCreate, MusicResponse, MusicUpdate
from app.services.music_service import MusicService

router = APIRouter(prefix="/music", tags=["Admin - Music"])


def get_service(database: AsyncIOMotorDatabase) -> MusicService:
    return MusicService(MusicRepository(database))


@router.get("", response_model=List[MusicResponse])
async def get_music(
    database: AsyncIOMotorDatabase = Depends(get_database),
    admin: dict = Depends(get_current_admin),
):
    """Get all music tracks (admin)."""
    service = get_service(database)
    return await service.get_all()


@router.get("/{music_id}", response_model=MusicResponse)
async def get_music_track(
    music_id: str,
    database: AsyncIOMotorDatabase = Depends(get_database),
    admin: dict = Depends(get_current_admin),
):
    """Get music track by ID (admin)."""
    service = get_service(database)
    return await service.get_by_id(music_id)


@router.post("", response_model=MusicResponse, status_code=201)
async def create_music_track(
    data: MusicCreate,
    database: AsyncIOMotorDatabase = Depends(get_database),
    admin: dict = Depends(get_current_admin),
):
    """Create music track (admin)."""
    service = get_service(database)
    return await service.create(data)


@router.put("/{music_id}", response_model=MusicResponse)
async def update_music_track(
    music_id: str,
    data: MusicUpdate,
    database: AsyncIOMotorDatabase = Depends(get_database),
    admin: dict = Depends(get_current_admin),
):
    """Update music track (admin)."""
    service = get_service(database)
    return await service.update(music_id, data)


@router.delete("/{music_id}", response_model=MessageResponse)
async def delete_music_track(
    music_id: str,
    database: AsyncIOMotorDatabase = Depends(get_database),
    admin: dict = Depends(get_current_admin),
):
    """Delete music track (admin)."""
    service = get_service(database)
    await service.delete(music_id)
    return MessageResponse(message="Music track deleted successfully")