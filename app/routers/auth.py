"""Authentication router."""

from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.database import get_database
from app.dependencies import get_current_admin
from app.repositories.admin_repo import AdminRepository
from app.schemas.admin import AdminCreate, AdminLogin, AdminResponse, AdminToken
from app.schemas.common import MessageResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup", response_model=AdminResponse, status_code=201)
async def signup(
    data: AdminCreate,
    database: AsyncIOMotorDatabase = Depends(get_database),
):
    """Create a new admin account."""
    admin_repo = AdminRepository(database)
    auth_service = AuthService(admin_repo)
    admin = await auth_service.create_admin(
        email=data.email, password=data.password, full_name=data.full_name
    )
    return AdminResponse(
        id=admin["id"],
        email=admin["email"],
        full_name=admin["full_name"],
        is_active=admin["is_active"],
    )


@router.post("/login", response_model=AdminToken)
async def login(
    credentials: AdminLogin,
    database: AsyncIOMotorDatabase = Depends(get_database),
):
    """Admin login endpoint."""
    admin_repo = AdminRepository(database)
    auth_service = AuthService(admin_repo)
    token = await auth_service.authenticate(
        email=credentials.email, password=credentials.password
    )
    return AdminToken(access_token=token)


@router.get("/me", response_model=MessageResponse)
async def get_me(
    admin: dict = Depends(get_current_admin),
):
    """Get current authenticated admin info."""
    return MessageResponse(
        message=f"Authenticated as {admin.get('email', 'unknown')}",
        success=True,
    )
