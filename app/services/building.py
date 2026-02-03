from app.repositories.building import BuildingRepository


class BuildingService:
    def __init__(self, repository: BuildingRepository) -> None:
        self.repository = repository

    async def list_all(self):
        return await self.repository.list_all()
