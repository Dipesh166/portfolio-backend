# Backend Implementation Plan

## Phase 1: Project Setup

- [ ] 1.1 Create project folder structure
- [ ] 1.2 Create `requirements.txt` with dependencies
- [ ] 1.3 Create `.env.example` with environment variables
- [ ] 1.4 Create `app/__init__.py` and `app/main.py` entry point

## Phase 2: Core Configuration

- [ ] 2.1 Create `app/core/config.py` - Pydantic Settings for env vars
- [ ] 2.2 Create `app/core/database.py` - MongoDB connection with Motor
- [ ] 2.3 Create `app/core/security.py` - JWT token creation/verification
- [ ] 2.4 Create `app/core/cloudinary.py` - Cloudinary configuration

## Phase 3: Pydantic Models & Schemas

- [ ] 3.1 Create `app/models/__init__.py`
- [ ] 3.2 Create `app/models/admin.py` - Admin user model
- [ ] 3.3 Create `app/models/profile.py` - Profile model
- [ ] 3.4 Create `app/models/experience.py` - Experience model
- [ ] 3.5 Create `app/models/education.py` - Education model
- [ ] 3.6 Create `app/models/project.py` - Project model
- [ ] 3.7 Create `app/models/skill.py` - Skill model
- [ ] 3.8 Create `app/models/certification.py` - Certification model
- [ ] 3.9 Create `app/models/achievement.py` - Achievement model
- [ ] 3.10 Create `app/models/social.py` - Social link model
- [ ] 3.11 Create `app/models/contact.py` - Contact message model
- [ ] 3.12 Create `app/models/site_settings.py` - Site settings model

## Phase 4: Schemas (Request/Response)

- [ ] 4.1 Create `app/schemas/__init__.py`
- [ ] 4.2 Create `app/schemas/common.py` - Shared schemas (MediaObject, PaginatedResponse)
- [ ] 4.3 Create `app/schemas/admin.py` - Admin auth schemas
- [ ] 4.4 Create `app/schemas/profile.py` - Profile schemas
- [ ] 4.5 Create `app/schemas/experience.py` - Experience schemas
- [ ] 4.6 Create `app/schemas/education.py` - Education schemas
- [ ] 4.7 Create `app/schemas/project.py` - Project schemas
- [ ] 4.8 Create `app/schemas/skill.py` - Skill schemas
- [ ] 4.9 Create `app/schemas/certification.py` - Certification schemas
- [ ] 4.10 Create `app/schemas/achievement.py` - Achievement schemas
- [ ] 4.11 Create `app/schemas/social.py` - Social link schemas
- [ ] 4.12 Create `app/schemas/contact.py` - Contact message schemas
- [ ] 4.13 Create `app/schemas/site_settings.py` - Site settings schemas
- [ ] 4.14 Create `app/schemas/portfolio.py` - Combined portfolio response

## Phase 5: Repository Layer

- [ ] 5.1 Create `app/repositories/__init__.py`
- [ ] 5.2 Create `app/repositories/base.py` - Base repository with CRUD
- [ ] 5.3 Create `app/repositories/admin_repo.py`
- [ ] 5.4 Create `app/repositories/profile_repo.py`
- [ ] 5.5 Create `app/repositories/experience_repo.py`
- [ ] 5.6 Create `app/repositories/education_repo.py`
- [ ] 5.7 Create `app/repositories/project_repo.py`
- [ ] 5.8 Create `app/repositories/skill_repo.py`
- [ ] 5.9 Create `app/repositories/certification_repo.py`
- [ ] 5.10 Create `app/repositories/achievement_repo.py`
- [ ] 5.11 Create `app/repositories/social_repo.py`
- [ ] 5.12 Create `app/repositories/contact_repo.py`
- [ ] 5.13 Create `app/repositories/site_settings_repo.py`

## Phase 6: Service Layer

- [ ] 6.1 Create `app/services/__init__.py`
- [ ] 6.2 Create `app/services/auth_service.py` - Authentication logic
- [ ] 6.3 Create `app/services/profile_service.py`
- [ ] 6.4 Create `app/services/experience_service.py`
- [ ] 6.5 Create `app/services/education_service.py`
- [ ] 6.6 Create `app/services/project_service.py`
- [ ] 6.7 Create `app/services/skill_service.py`
- [ ] 6.8 Create `app/services/certification_service.py`
- [ ] 6.9 Create `app/services/achievement_service.py`
- [ ] 6.10 Create `app/services/social_service.py`
- [ ] 6.11 Create `app/services/contact_service.py`
- [ ] 6.12 Create `app/services/media_service.py` - Cloudinary upload/delete
- [ ] 6.13 Create `app/services/site_settings_service.py`
- [ ] 6.14 Create `app/services/portfolio_service.py` - Aggregated portfolio

## Phase 7: API Dependencies

- [ ] 7.1 Create `app/dependencies.py` - Auth dependency, DB dependency

## Phase 8: API Routers

- [ ] 8.1 Create `app/routers/__init__.py`
- [ ] 8.2 Create `app/routers/auth.py` - Login endpoint
- [ ] 8.3 Create `app/routers/admin/profile.py` - Admin profile CRUD
- [ ] 8.4 Create `app/routers/admin/experience.py` - Admin experience CRUD
- [ ] 8.5 Create `app/routers/admin/education.py` - Admin education CRUD
- [ ] 8.6 Create `app/routers/admin/projects.py` - Admin project CRUD
- [ ] 8.7 Create `app/routers/admin/skills.py` - Admin skill CRUD
- [ ] 8.8 Create `app/routers/admin/certifications.py` - Admin certification CRUD
- [ ] 8.9 Create `app/routers/admin/achievements.py` - Admin achievement CRUD
- [ ] 8.10 Create `app/routers/admin/socials.py` - Admin social link CRUD
- [ ] 8.11 Create `app/routers/admin/settings.py` - Admin site settings
- [ ] 8.12 Create `app/routers/admin/messages.py` - Admin contact messages
- [ ] 8.13 Create `app/routers/media.py` - Media upload/delete
- [ ] 8.14 Create `app/routers/public.py` - Public portfolio endpoints

## Phase 9: Application Entry Point

- [ ] 9.1 Update `app/main.py` with all routers, CORS, lifespan
- [ ] 9.2 Add error handlers and middleware

## Phase 10: Verification

- [ ] 10.1 Verify project structure
- [ ] 10.2 Run syntax check on all files
