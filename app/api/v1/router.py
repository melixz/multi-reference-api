from fastapi import APIRouter, Depends

from app.api.v1 import buildings, organizations
from app.core.security import get_api_key

api_router = APIRouter(prefix="/api/v1", dependencies=[Depends(get_api_key)])
api_router.include_router(buildings.router)
api_router.include_router(organizations.router)
