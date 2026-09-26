"""Portfolio aggregation service."""

from typing import Optional

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
from app.schemas.education import EducationResponse
from app.schemas.experience import ExperienceResponse
from app.schemas.music import MusicResponse
from app.schemas.portfolio import PortfolioResponse
from app.schemas.profile import ProfileResponse
from app.schemas.project import ProjectResponse
from app.schemas.site_settings import SiteSettingsResponse
from app.schemas.skill import SkillResponse
from app.schemas.social import SocialLinkResponse


class PortfolioService:
    """Aggregate all portfolio data for public endpoint."""

    def __init__(
        self,
        profile_repo: ProfileRepository,
        experience_repo: ExperienceRepository,
        education_repo: EducationRepository,
        project_repo: ProjectRepository,
        skill_repo: SkillRepository,
        certification_repo: CertificationRepository,
        achievement_repo: AchievementRepository,
        music_repo: MusicRepository,
        social_repo: SocialLinkRepository,
        settings_repo: SiteSettingsRepository,
    ) -> None:
        self.profile_repo = profile_repo
        self.experience_repo = experience_repo
        self.education_repo = education_repo
        self.project_repo = project_repo
        self.skill_repo = skill_repo
        self.certification_repo = certification_repo
        self.achievement_repo = achievement_repo
        self.music_repo = music_repo
        self.social_repo = social_repo
        self.settings_repo = settings_repo

    async def get_full_portfolio(self) -> PortfolioResponse:
        """Get complete portfolio data."""
        # Fetch all data concurrently
        profile = await self.profile_repo.get_profile()
        experiences = await self.experience_repo.get_all_ordered()
        education = await self.education_repo.get_all_ordered()
        projects = await self.project_repo.get_all_ordered()
        skills = await self.skill_repo.get_all_ordered()
        certifications = await self.certification_repo.get_all_ordered()
        achievements = await self.achievement_repo.get_all_ordered()
        music = await self.music_repo.get_enabled()
        social_links = await self.social_repo.get_enabled()
        settings = await self.settings_repo.get_settings()

        return PortfolioResponse(
            profile=ProfileResponse(**profile) if profile else None,
            experiences=[ExperienceResponse(**exp) for exp in experiences],
            education=[EducationResponse(**edu) for edu in education],
            projects=[ProjectResponse(**proj) for proj in projects],
            skills=[SkillResponse(**skill) for skill in skills],
            certifications=[
                CertificationResponse(**cert) for cert in certifications
            ],
            achievements=[AchievementResponse(**ach) for ach in achievements],
            music=[MusicResponse(**tr) for tr in music],
            social_links=[SocialLinkResponse(**s) for s in social_links],
            settings=SiteSettingsResponse(**settings) if settings else None,
        )
