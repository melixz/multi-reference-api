from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from app.models.activity import Activity


class ActivityRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, activity_id: int) -> Activity | None:
        return await self.session.get(Activity, activity_id)

    async def get_descendant_ids(self, activity_id: int) -> list[int]:
        activity_alias = aliased(Activity)

        cte = select(Activity.id).where(Activity.id == activity_id).cte(recursive=True)
        cte = cte.union_all(
            select(activity_alias.id).where(activity_alias.parent_id == cte.c.id),
        )

        stmt: Select[tuple[int]] = select(cte.c.id)
        result = await self.session.execute(stmt)
        return [row[0] for row in result.all()]

    async def get_depth_from_parent(self, parent_id: int | None) -> int:
        depth = 0
        current_id = parent_id
        while current_id is not None:
            depth += 1
            stmt = select(Activity.parent_id).where(Activity.id == current_id)
            current_id = await self.session.scalar(stmt)
            if depth > 3:
                break
        return depth
