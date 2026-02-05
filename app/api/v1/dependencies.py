from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.activity import ActivityRepository
from app.repositories.building import BuildingRepository
from app.repositories.organization import OrganizationRepository
from app.services.activity import ActivityService
from app.services.building import BuildingService
from app.services.organization import OrganizationService


def get_activity_service(
    session: AsyncSession = Depends(get_db),
) -> ActivityService:
    return ActivityService(ActivityRepository(session))


def get_organization_service(
    session: AsyncSession = Depends(get_db),
) -> OrganizationService:
    activity_service = ActivityService(ActivityRepository(session))
    return OrganizationService(OrganizationRepository(session), activity_service)


def get_building_service(
    session: AsyncSession = Depends(get_db),
) -> BuildingService:
    return BuildingService(BuildingRepository(session))
