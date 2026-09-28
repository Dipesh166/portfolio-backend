"""Media upload/delete/serve router."""

import hashlib
import io
import re

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Request,
    Response,
    UploadFile,
    status,
)
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

RANGE_PATTERN = re.compile(r"^bytes=(\d*)-(\d*)$")


def parse_range(header: str | None, size: int) -> tuple[int, int] | None:
    """Parse a single-range ``Range`` header into inclusive byte offsets."""
    if not header:
        return None
    match = RANGE_PATTERN.match(header.strip())
    if not match:
        return None
    raw_start, raw_end = match.group(1), match.group(2)
    if not raw_start and not raw_end:
        return None
    if not raw_start:
        suffix = int(raw_end)
        if suffix == 0:
            return None
        return max(0, size - suffix), size - 1
    start = int(raw_start)
    end = int(raw_end) if raw_end else size - 1
    if start > end or start >= size:
        return None
    return start, min(end, size - 1)


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


@router.api_route("/{file_id:path}", methods=["GET", "HEAD"])
async def serve_image(
    request: Request,
    file_id: str,
    database: AsyncIOMotorDatabase = Depends(get_database),
):
    """Serve an image or audio file from MongoDB GridFS (public)."""
    result = await media_service.get(file_id)
    data: bytes = result["file_data"]
    size = len(data)
    content_type = result["content_type"]
    is_audio = content_type.startswith("audio/")
    etag = f'"{hashlib.md5(data, usedforsecurity=False).hexdigest()}"'

    headers = {
        "Content-Disposition": f'inline; filename="{result["filename"]}"',
        "Accept-Ranges": "bytes",
        # CORSMiddleware only emits "Vary: Origin" when the request carries an
        # Origin header, so a non-CORS fetch of this URL used to be stored with no
        # Vary at all. Any later CORS request then matched that stored entry and
        # replayed a body with no Access-Control-Allow-Origin. Setting it here
        # makes the cache key always account for Origin (a repeated token is a
        # valid field list).
        "Vary": "Origin",
        "ETag": etag,
        "Last-Modified": result.get("upload_date") or "",
        # Audio is only ever consumed through createMediaElementSource(), which
        # requires a CORS-checked response. Never let one into the HTTP cache.
        "Cache-Control": "no-store" if is_audio else "public, max-age=86400",
    }
    headers = {k: v for k, v in headers.items() if v != ""}

    if request.headers.get("if-none-match") == etag:
        return Response(status_code=status.HTTP_304_NOT_MODIFIED, headers=headers)

    if request.method == "HEAD":
        headers["Content-Length"] = str(size)
        return Response(content=b"", media_type=content_type, headers=headers)

    range_header = request.headers.get("range")
    if range_header:
        span = parse_range(range_header, size)
        if span is None:
            return StreamingResponse(
                io.BytesIO(b""),
                status_code=status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE,
                media_type=content_type,
                headers={**headers, "Content-Range": f"bytes */{size}"},
            )
        start, end = span
        chunk = data[start : end + 1]
        return StreamingResponse(
            io.BytesIO(chunk),
            status_code=status.HTTP_206_PARTIAL_CONTENT,
            media_type=content_type,
            headers={
                **headers,
                "Content-Range": f"bytes {start}-{end}/{size}",
                "Content-Length": str(len(chunk)),
            },
        )

    return StreamingResponse(
        io.BytesIO(data),
        media_type=content_type,
        headers={**headers, "Content-Length": str(size)},
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
