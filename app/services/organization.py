from fastapi import HTTPException, status

from app.repositories.organization import OrganizationRepository
from app.services.activity import ActivityService


class OrganizationService:
    def __init__(
        self,
        repository: OrganizationRepository,
        activity_service: ActivityService,
    ) -> None:
        self.repository = repository
        self.activity_service = activity_service

    async def get_by_id(self, organization_id: int):
        organization = await self.repository.get_by_id(organization_id)
        if not organization:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organization not found",
            )
        return organization

    async def list_by_building(self, building_id: int):
        return await self.repository.list_by_building(building_id)

    async def list_by_activity(
        self,
        activity_id: int,
        include_descendants: bool,
    ):
        if include_descendants:
            activity_ids = await self.activity_service.get_descendant_ids(activity_id)
        else:
            activity_ids = [activity_id]
        return await self.repository.list_by_activity_ids(activity_ids)

    async def search_by_name(self, name: str):
        return await self.repository.search_by_name(name)

    async def list_by_geo_radius(
        self,
        lat: float,
        lon: float,
        radius_m: float,
    ):
        return await self.repository.list_by_geo_radius(lat=lat, lon=lon, radius_m=radius_m)

    async def list_by_geo_bbox(
        self,
        min_lon: float,
        min_lat: float,
        max_lon: float,
        max_lat: float,
    ):
        return await self.repository.list_by_geo_bbox(
            min_lon=min_lon,
            min_lat=min_lat,
            max_lon=max_lon,
            max_lat=max_lat,
        )
