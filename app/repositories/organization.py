from geoalchemy2 import Geometry
from geoalchemy2.elements import WKTElement
from sqlalchemy import Select, cast, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.building import Building
from app.models.organization import Organization
from app.models.organization_activity import OrganizationActivity


class OrganizationRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    def _base_stmt(self) -> Select[tuple[Organization]]:
        return (
            select(Organization)
            .options(
                selectinload(Organization.building),
                selectinload(Organization.phones),
                selectinload(Organization.activities),
            )
            .order_by(Organization.name)
        )

    async def get_by_id(self, organization_id: int) -> Organization | None:
        stmt = self._base_stmt().where(Organization.id == organization_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def list_by_building(self, building_id: int) -> list[Organization]:
        stmt = self._base_stmt().where(Organization.building_id == building_id)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def list_by_activity_ids(self, activity_ids: list[int]) -> list[Organization]:
        stmt = (
            self._base_stmt()
            .join(
                OrganizationActivity,
                OrganizationActivity.organization_id == Organization.id,
            )
            .where(OrganizationActivity.activity_id.in_(activity_ids))
            .distinct()
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def search_by_name(self, name: str) -> list[Organization]:
        stmt = self._base_stmt().where(Organization.name.ilike(f"%{name}%"))
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def list_by_geo_radius(
        self,
        lat: float,
        lon: float,
        radius_m: float,
    ) -> list[Organization]:
        point = WKTElement(f"POINT({lon} {lat})", srid=4326)
        stmt = (
            self._base_stmt()
            .join(Building, Organization.building_id == Building.id)
            .where(Building.location.ST_DWithin(point, radius_m))
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def list_by_geo_bbox(
        self,
        min_lon: float,
        min_lat: float,
        max_lon: float,
        max_lat: float,
    ) -> list[Organization]:
        envelope = func.ST_MakeEnvelope(min_lon, min_lat, max_lon, max_lat, 4326)
        location_geom = cast(
            Building.location,
            Geometry(geometry_type="POINT", srid=4326),
        )
        stmt = (
            self._base_stmt()
            .join(Building, Organization.building_id == Building.id)
            .where(func.ST_Within(location_geom, envelope))
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
