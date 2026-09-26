"""Portfolio aggregated response schema."""

from typing import List, Optional

from pydantic import BaseModel

from app.schemas.achievement import AchievementResponse
from app.schemas.certification import CertificationResponse
from app.schemas.education import EducationResponse
from app.schemas.experience import ExperienceResponse
from app.schemas.music import MusicResponse
from app.schemas.profile import ProfileResponse
from app.schemas.project import ProjectResponse
from app.schemas.site_settings import SiteSettingsResponse
from app.schemas.skill import SkillResponse
from app.schemas.social import SocialLinkResponse


class PortfolioResponse(BaseModel):
    """Combined portfolio data for public endpoint."""

    profile: Optional[ProfileResponse] = None
    experiences: List[ExperienceResponse] = []
    education: List[EducationResponse] = []
    projects: List[ProjectResponse] = []
    skills: List[SkillResponse] = []
    certifications: List[CertificationResponse] = []
    achievements: List[AchievementResponse] = []
    social_links: List[SocialLinkResponse] = []
    music: List[MusicResponse] = []
    settings: Optional[SiteSettingsResponse] = None
