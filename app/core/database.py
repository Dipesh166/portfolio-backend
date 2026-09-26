"""MongoDB database connection using Motor async driver."""

from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.config import get_settings


class Database:
    """MongoDB database manager."""

    def __init__(self) -> None:
        self._client: Optional[AsyncIOMotorClient] = None
        self._database: Optional[AsyncIOMotorDatabase] = None

    async def connect(self) -> None:
        """Establish database connection."""
        settings = get_settings()
        self._client = AsyncIOMotorClient(
            settings.mongodb_uri,
            serverSelectionTimeoutMS=10000,
            tls=True,
            tlsAllowInvalidCertificates=True,
        )
        self._database = self._client[settings.mongodb_database]
        # Verify connection
        await self._client.admin.command("ping")

    async def disconnect(self) -> None:
        """Close database connection."""
        if self._client:
            self._client.close()
            self._client = None
            self._database = None

    def get_database(self) -> AsyncIOMotorDatabase:
        """Get database instance."""
        if self._database is None:
            raise RuntimeError("Database not connected. Call connect() first.")
        return self._database


# Singleton instance
db = Database()


async def get_database() -> AsyncIOMotorDatabase:
    """Dependency for getting database instance."""
    return db.get_database()
