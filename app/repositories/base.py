"""Base repository with generic CRUD operations."""

from typing import Any, Dict, List, Optional

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo import ReturnDocument


class BaseRepository:
    """Generic repository for MongoDB operations."""

    def __init__(self, collection: AsyncIOMotorCollection) -> None:
        self.collection = collection

    def _convert_id(self, document: Optional[dict]) -> Optional[dict]:
        """Convert MongoDB _id to string id."""
        if document and "_id" in document:
            document["id"] = str(document.pop("_id"))
        return document

    def _convert_ids(self, documents: List[dict]) -> List[dict]:
        """Convert MongoDB _id to string id for a list of documents."""
        return [self._convert_id(doc) for doc in documents]

    async def find_one(self, query: Dict[str, Any]) -> Optional[dict]:
        """Find a single document."""
        document = await self.collection.find_one(query)
        return self._convert_id(document)

    async def find_many(
        self,
        query: Dict[str, Any] = None,
        sort: List[tuple] = None,
        limit: int = 0,
        skip: int = 0,
    ) -> List[dict]:
        """Find multiple documents."""
        if query is None:
            query = {}

        cursor = self.collection.find(query)

        if sort:
            cursor = cursor.sort(sort)
        if skip:
            cursor = cursor.skip(skip)
        if limit:
            cursor = cursor.limit(limit)

        documents = await cursor.to_list(length=None)
        return self._convert_ids(documents)

    async def find_one_by_id(self, document_id: str) -> Optional[dict]:
        """Find a document by its ID."""
        try:
            document = await self.collection.find_one({"_id": ObjectId(document_id)})
            return self._convert_id(document)
        except Exception:
            return None

    async def insert_one(self, document: dict) -> str:
        """Insert a single document. Returns the inserted ID."""
        result = await self.collection.insert_one(document)
        return str(result.inserted_id)

    async def update_one(
        self, document_id: str, update_data: Dict[str, Any]
    ) -> Optional[dict]:
        """Update a single document. Returns the updated document."""
        try:
            await self.collection.update_one(
                {"_id": ObjectId(document_id)},
                {"$set": update_data},
            )
            return await self.find_one_by_id(document_id)
        except Exception:
            return None

    async def delete_one(self, document_id: str) -> bool:
        """Delete a single document."""
        try:
            result = await self.collection.delete_one({"_id": ObjectId(document_id)})
            return result.deleted_count > 0
        except Exception:
            return False

    async def count_documents(self, query: Dict[str, Any] = None) -> int:
        """Count documents matching query."""
        if query is None:
            query = {}
        return await self.collection.count_documents(query)

    async def find_one_and_update(
        self,
        query: Dict[str, Any],
        update_data: Dict[str, Any],
        upsert: bool = False,
    ) -> Optional[dict]:
        """Find and update a document."""
        document = await self.collection.find_one_and_update(
            query,
            {"$set": update_data},
            upsert=upsert,
            return_document=ReturnDocument.AFTER,
        )
        return self._convert_id(document)
