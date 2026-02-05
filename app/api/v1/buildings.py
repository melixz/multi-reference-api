from fastapi import APIRouter, Depends

from app.api.v1.dependencies import get_building_service
from app.schemas.building import BuildingRead
from app.schemas.common import ApiResponse
from app.services.building import BuildingService

router = APIRouter(prefix="/buildings", tags=["Buildings"])


@router.get("/", response_model=ApiResponse[list[BuildingRead]])
async def list_buildings(
    service: BuildingService = Depends(get_building_service),
):
    buildings = await service.list_all()
    return ApiResponse(data=buildings)
