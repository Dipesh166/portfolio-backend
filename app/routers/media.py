"""Media upload/delete/serve router."""

import io

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from fastapi.responses import StreamingResponse
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.database import get_database
from app.dependencies import get_current_admin
from app.schemas.common import MediaObject
from app.services.media_service import MediaService

router = APIRouter(prefix="/media", tags=["Media"])

media_service = MediaService()

IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif", "application/pdf"}
AUDIO_TYPES = {
    "audio/mpeg",
    "audio/mp3",
    "audio/wav",
    "audio/x-wav",
    "audio/ogg",
    "audio/aac",
    "audio/mp4",
    "audio/x-m4a",
    "audio/flac",
    "audio/x-flac",
    "audio/webm",
    "audio/midi",
    "audio/x-midi",
}
ALLOWED_TYPES = IMAGE_TYPES | AUDIO_TYPES
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
MAX_AUDIO_SIZE = 50 * 1024 * 1024  # 50MB


@router.post("/upload", response_model=MediaObject)
async def upload_media(
    file: UploadFile = File(...),
    folder: str = Form("portfolio"),
    alt: str = Form(""),
    admin: dict = Depends(get_current_admin),
):
    """Upload an image or audio file to MongoDB GridFS (admin)."""
    # Validate file type
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed: {', '.join(sorted(ALLOWED_TYPES))}",
        )

    # Validate file size
    max_size = MAX_AUDIO_SIZE if file.content_type in AUDIO_TYPES else MAX_FILE_SIZE
    contents = await file.read()
    if len(contents) > max_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File size exceeds {max_size // (1024 * 1024)}MB limit",
        )

    # Reset file position
    file.file = io.BytesIO(contents)

    return await media_service.upload(file, folder, alt)


@router.get("/{file_id:path}")
async def serve_image(
    file_id: str,
    database: AsyncIOMotorDatabase = Depends(get_database),
):
    """Serve an image from MongoDB GridFS (public)."""
    result = await media_service.get(file_id)

    return StreamingResponse(
        io.BytesIO(result["file_data"]),
        media_type=result["content_type"],
        headers={
            "Content-Disposition": f'inline; filename="{result["filename"]}"',
            "Cache-Control": "public, max-age=86400",
        },
    )


@router.delete("/{file_id:path}")
async def delete_image(
    file_id: str,
    admin: dict = Depends(get_current_admin),
):
    """Delete an image from MongoDB GridFS (admin)."""
    success = await media_service.delete(file_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete image",
        )
    return {"message": "Image deleted successfully", "success": True}
