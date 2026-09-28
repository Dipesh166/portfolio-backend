"""MongoDB GridFS-based media storage utilities."""

import io
from datetime import datetime, timezone
from email.utils import format_datetime
from typing import Optional

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorGridFSBucket


async def upload_image(
    db: AsyncIOMotorDatabase,
    file_data: bytes,
    filename: str,
    content_type: str = "image/jpeg",
    folder: str = "portfolio",
) -> dict:
    """Upload an image to MongoDB GridFS."""
    bucket = AsyncIOMotorGridFSBucket(db)

    file_id = await bucket.upload_from_stream(
        filename,
        io.BytesIO(file_data),
        metadata={
            "content_type": content_type,
            "folder": folder,
            "uploaded_at": datetime.now(timezone.utc),
            "size": len(file_data),
        },
    )

    return {
        "file_id": str(file_id),
        "url": f"/api/v1/media/{file_id}",
        "filename": filename,
        "content_type": content_type,
        "size": len(file_data),
    }


async def get_image(db: AsyncIOMotorDatabase, file_id: str) -> Optional[dict]:
    """Retrieve an image from GridFS."""
    bucket = AsyncIOMotorGridFSBucket(db)

    try:
        file_object_id = ObjectId(file_id)
    except Exception:
        return None

    grid_out = await bucket.open_download_stream(file_object_id)
    file_data = await grid_out.read()

    metadata = grid_out.metadata or {}

    return {
        "file_id": str(file_object_id),
        "file_data": file_data,
        "filename": grid_out.filename,
        "content_type": metadata.get("content_type", "image/jpeg"),
        "size": metadata.get("size", len(file_data)),
        "upload_date": _http_date(grid_out.upload_date),
    }


def _http_date(value: Optional[datetime]) -> str:
    """Format a datetime as an RFC 7231 IMF-fixdate, or an empty string."""
    if not isinstance(value, datetime):
        return ""
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return format_datetime(value, usegmt=True)


async def delete_image(db: AsyncIOMotorDatabase, file_id: str) -> bool:
    """Delete an image from GridFS."""
    bucket = AsyncIOMotorGridFSBucket(db)

    try:
        file_object_id = ObjectId(file_id)
    except Exception:
        return False

    try:
        await bucket.delete(file_object_id)
        return True
    except Exception:
        return False


async def replace_image(
    db: AsyncIOMotorDatabase,
    old_file_id: Optional[str],
    file_data: bytes,
    filename: str,
    content_type: str = "image/jpeg",
    folder: str = "portfolio",
) -> dict:
    """Replace an existing image with a new one."""
    if old_file_id:
        await delete_image(db, old_file_id)

    return await upload_image(db, file_data, filename, content_type, folder)
