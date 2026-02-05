from app.repositories.activity import ActivityRepository


class ActivityService:
    def __init__(self, repository: ActivityRepository) -> None:
        self.repository = repository

    async def get_descendant_ids(self, activity_id: int) -> list[int]:
        return await self.repository.get_descendant_ids(activity_id)

    async def ensure_depth_limit(self, parent_id: int | None) -> None:
        depth = await self.repository.get_depth_from_parent(parent_id)
        if depth >= 3:
            raise ValueError("Activity nesting depth limit exceeded")
