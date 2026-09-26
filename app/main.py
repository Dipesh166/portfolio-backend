"""FastAPI Portfolio Backend - Main Application."""

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import get_settings
from app.core.database import db
from app.routers import auth, media, public
from app.routers.admin import (
    achievements,
    certifications,
    education,
    experience,
    messages,
    music,
    profile,
    projects,
    settings,
    skills,
    socials,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan - startup and shutdown events."""
    # Startup
    settings = get_settings()
    await db.connect()
    print(f"Connected to MongoDB: {settings.mongodb_database}")
    yield
    # Shutdown
    await db.disconnect()
    print("Disconnected from MongoDB")


app = FastAPI(
    title="Portfolio Backend API",
    description="Dynamic Portfolio System Backend API",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS Configuration
cors_settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global Exception Handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "success": False},
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "success": False},
    )


# Health Check
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "success": True}


# Include Routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(media.router, prefix="/api/v1")

# Admin Routers
admin_prefix = "/api/v1/admin"
app.include_router(profile.router, prefix=admin_prefix)
app.include_router(experience.router, prefix=admin_prefix)
app.include_router(education.router, prefix=admin_prefix)
app.include_router(projects.router, prefix=admin_prefix)
app.include_router(skills.router, prefix=admin_prefix)
app.include_router(certifications.router, prefix=admin_prefix)
app.include_router(achievements.router, prefix=admin_prefix)
app.include_router(socials.router, prefix=admin_prefix)
app.include_router(music.router, prefix=admin_prefix)
app.include_router(settings.router, prefix=admin_prefix)
app.include_router(messages.router, prefix=admin_prefix)

# Public Router
app.include_router(public.router, prefix="/api/v1")
