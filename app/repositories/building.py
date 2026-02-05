from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.building import Building


class BuildingRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_all(self) -> list[Building]:
        stmt = select(Building).order_by(Building.address)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
