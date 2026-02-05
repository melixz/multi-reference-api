from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.v1.dependencies import get_organization_service
from app.schemas.common import ApiResponse
from app.schemas.organization import OrganizationRead
from app.services.organization import OrganizationService

router = APIRouter(prefix="/organizations", tags=["Organizations"])


@router.get("/by-building/{building_id}", response_model=ApiResponse[list[OrganizationRead]])
async def list_by_building(
    building_id: int,
    service: OrganizationService = Depends(get_organization_service),
):
    organizations = await service.list_by_building(building_id)
    return ApiResponse(data=organizations)


@router.get("/by-activity/{activity_id}", response_model=ApiResponse[list[OrganizationRead]])
async def list_by_activity(
    activity_id: int,
    include_descendants: bool = Query(
        default=True,
        description="Включать дочерние виды деятельности",
    ),
    service: OrganizationService = Depends(get_organization_service),
):
    organizations = await service.list_by_activity(
        activity_id=activity_id,
        include_descendants=include_descendants,
    )
    return ApiResponse(data=organizations)


@router.get("/search", response_model=ApiResponse[list[OrganizationRead]])
async def search_by_name(
    name: str = Query(..., min_length=2, max_length=255),
    service: OrganizationService = Depends(get_organization_service),
):
    organizations = await service.search_by_name(name)
    return ApiResponse(data=organizations)


@router.get("/geo", response_model=ApiResponse[list[OrganizationRead]])
async def list_by_geo(
    lat: float | None = Query(None, ge=-90, le=90),
    lon: float | None = Query(None, ge=-180, le=180),
    radius_m: float | None = Query(None, gt=0),
    bbox: str | None = Query(
        None,
        description="min_lon,min_lat,max_lon,max_lat",
    ),
    service: OrganizationService = Depends(get_organization_service),
):
    if bbox and (lat is not None or lon is not None or radius_m is not None):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Use either bbox or lat/lon/radius_m",
        )

    if bbox:
        try:
            parts = [float(part.strip()) for part in bbox.split(",")]
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid bbox format",
            ) from exc

        if len(parts) != 4:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="bbox must have 4 values",
            )
        min_lon, min_lat, max_lon, max_lat = parts
        if min_lon >= max_lon or min_lat >= max_lat:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="bbox values are invalid",
            )
        organizations = await service.list_by_geo_bbox(
            min_lon=min_lon,
            min_lat=min_lat,
            max_lon=max_lon,
            max_lat=max_lat,
        )
        return ApiResponse(data=organizations)

    if lat is None or lon is None or radius_m is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Provide lat, lon and radius_m or bbox",
        )

    organizations = await service.list_by_geo_radius(
        lat=lat,
        lon=lon,
        radius_m=radius_m,
    )
    return ApiResponse(data=organizations)


@router.get("/{organization_id}", response_model=ApiResponse[OrganizationRead])
async def get_organization(
    organization_id: int,
    service: OrganizationService = Depends(get_organization_service),
):
    organization = await service.get_by_id(organization_id)
    return ApiResponse(data=organization)
