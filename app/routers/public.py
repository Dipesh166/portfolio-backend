"""Public portfolio endpoints (no authentication required)."""

from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.database import get_database
from app.repositories.achievement_repo import AchievementRepository
from app.repositories.certification_repo import CertificationRepository
from app.repositories.education_repo import EducationRepository
from app.repositories.experience_repo import ExperienceRepository
from app.repositories.music_repo import MusicRepository
from app.repositories.profile_repo import ProfileRepository
from app.repositories.project_repo import ProjectRepository
from app.repositories.site_settings_repo import SiteSettingsRepository
from app.repositories.skill_repo import SkillRepository
from app.repositories.social_repo import SocialLinkRepository
from app.schemas.achievement import AchievementResponse
from app.schemas.certification import CertificationResponse
from app.schemas.contact import ContactCreate, ContactResponse
from app.schemas.education import EducationResponse
from app.schemas.experience import ExperienceResponse
from app.schemas.music import MusicResponse
from app.schemas.portfolio import PortfolioResponse
from app.schemas.project import ProjectResponse
from app.schemas.skill import SkillResponse
from app.schemas.social import SocialLinkResponse
from app.services.contact_service import ContactService
from app.services.portfolio_service import PortfolioService
from app.repositories.contact_repo import ContactMessageRepository

router = APIRouter(prefix="/public", tags=["Public"])


@router.get("/portfolio", response_model=PortfolioResponse)
async def get_portfolio(
    database: AsyncIOMotorDatabase = Depends(get_database),
):
    """Get complete portfolio data (public)."""
    service = PortfolioService(
        profile_repo=ProfileRepository(database),
        experience_repo=ExperienceRepository(database),
        education_repo=EducationRepository(database),
        project_repo=ProjectRepository(database),
        skill_repo=SkillRepository(database),
        certification_repo=CertificationRepository(database),
        achievement_repo=AchievementRepository(database),
        music_repo=MusicRepository(database),
        social_repo=SocialLinkRepository(database),
        settings_repo=SiteSettingsRepository(database),
    )
    return await service.get_full_portfolio()


@router.get("/experiences", response_model=list[ExperienceResponse])
async def get_experiences(
    database: AsyncIOMotorDatabase = Depends(get_database),
):
    """Get all experiences (public)."""
    repo = ExperienceRepository(database)
    experiences = await repo.get_all_ordered()
    return [ExperienceResponse(**exp) for exp in experiences]


@router.get("/education", response_model=list[EducationResponse])
async def get_education(
    database: AsyncIOMotorDatabase = Depends(get_database),
):
    """Get all education (public)."""
    repo = EducationRepository(database)
    education = await repo.get_all_ordered()
    return [EducationResponse(**edu) for edu in education]


@router.get("/projects", response_model=list[ProjectResponse])
async def get_projects(
    database: AsyncIOMotorDatabase = Depends(get_database),
):
    """Get all projects (public)."""
    repo = ProjectRepository(database)
    projects = await repo.get_all_ordered()
    return [ProjectResponse(**proj) for proj in projects]


@router.get("/projects/{slug}", response_model=ProjectResponse)
async def get_project_by_slug(
    slug: str,
    database: AsyncIOMotorDatabase = Depends(get_database),
):
    """Get project by slug (public)."""
    repo = ProjectRepository(database)
    project = await repo.find_by_slug(slug)
    if not project:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    return ProjectResponse(**project)


@router.get("/skills", response_model=list[SkillResponse])
async def get_skills(
    database: AsyncIOMotorDatabase = Depends(get_database),
):
    """Get all skills (public)."""
    repo = SkillRepository(database)
    skills = await repo.get_all_ordered()
    return [SkillResponse(**skill) for skill in skills]


@router.get("/certifications", response_model=list[CertificationResponse])
async def get_certifications(
    database: AsyncIOMotorDatabase = Depends(get_database),
):
    """Get all certifications (public)."""
    repo = CertificationRepository(database)
    certifications = await repo.get_all_ordered()
    return [CertificationResponse(**cert) for cert in certifications]


@router.get("/achievements", response_model=list[AchievementResponse])
async def get_achievements(
    database: AsyncIOMotorDatabase = Depends(get_database),
):
    """Get all achievements (public)."""
    repo = AchievementRepository(database)
    achievements = await repo.get_all_ordered()
    return [AchievementResponse(**ach) for ach in achievements]


@router.get("/socials", response_model=list[SocialLinkResponse])
async def get_socials(
    database: AsyncIOMotorDatabase = Depends(get_database),
):
    """Get enabled social links (public)."""
    repo = SocialLinkRepository(database)
    socials = await repo.get_enabled()
    return [SocialLinkResponse(**s) for s in socials]


@router.get("/music", response_model=list[MusicResponse])
async def get_music(
    database: AsyncIOMotorDatabase = Depends(get_database),
):
    """Get enabled music tracks (public)."""
    repo = MusicRepository(database)
    tracks = await repo.get_enabled()
    return [MusicResponse(**t) for t in tracks]


@router.post("/contact", response_model=ContactResponse, status_code=201)
async def submit_contact(
    data: ContactCreate,
    database: AsyncIOMotorDatabase = Depends(get_database),
):
    """Submit contact form (public)."""
    service = ContactService(ContactMessageRepository(database))
    return await service.create(data)
