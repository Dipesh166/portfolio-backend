"""Media service for MongoDB GridFS operations."""

import io
from typing import Optional

from fastapi import HTTPException, UploadFile, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.database import db
from app.core.gridfs_media import delete_image, get_image, replace_image, upload_image
from app.schemas.common import MediaObject


class MediaService:
    """Handle media upload, retrieval, and deletion via MongoDB GridFS."""

    def _get_database(self) -> AsyncIOMotorDatabase:
        return db.get_database()

    async def upload(
        self, file: UploadFile, folder: str = "portfolio", alt: str = ""
    ) -> MediaObject:
        """Upload an image and return media object."""
        try:
            file_data = await file.read()
            content_type = file.content_type or "image/jpeg"
            filename = file.filename or "upload.jpg"

            result = await upload_image(
                db=self._get_database(),
                file_data=file_data,
                filename=filename,
                content_type=content_type,
                folder=folder,
            )

            return MediaObject(
                file_id=result["file_id"],
                url=result["url"],
                alt=alt or filename,
                filename=filename,
                content_type=content_type,
                size=result["size"],
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to upload image: {str(e)}",
            )

    async def get(self, file_id: str) -> dict:
        """Retrieve image data from GridFS."""
        result = await get_image(self._get_database(), file_id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Image not found",
            )
        return result

    async def delete(self, file_id: str) -> bool:
        """Delete an image from GridFS."""
        if not file_id:
            return True
        return await delete_image(self._get_database(), file_id)

    async def replace(
        self,
        old_file_id: Optional[str],
        file: UploadFile,
        folder: str = "portfolio",
        alt: str = "",
    ) -> MediaObject:
        """Replace an existing image with a new one."""
        file_data = await file.read()
        content_type = file.content_type or "image/jpeg"
        filename = file.filename or "upload.jpg"

        result = await replace_image(
            db=self._get_database(),
            old_file_id=old_file_id,
            file_data=file_data,
            filename=filename,
            content_type=content_type,
            folder=folder,
        )

        return MediaObject(
            file_id=result["file_id"],
            url=result["url"],
            alt=alt or filename,
            filename=filename,
            content_type=content_type,
            size=result["size"],
        )
