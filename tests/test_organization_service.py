from unittest.mock import AsyncMock

import pytest
from fastapi import HTTPException

from app.repositories.organization import OrganizationRepository
from app.services.activity import ActivityService
from app.services.organization import OrganizationService


@pytest.mark.unit
async def test_list_by_activity_with_descendants():
    repo = AsyncMock(spec=OrganizationRepository)
    activity_service = AsyncMock(spec=ActivityService)
    activity_service.get_descendant_ids = AsyncMock(return_value=[1, 2, 3])
    repo.list_by_activity_ids = AsyncMock(return_value=["org1", "org2"])

    service = OrganizationService(repo, activity_service)
    result = await service.list_by_activity(activity_id=1, include_descendants=True)

    activity_service.get_descendant_ids.assert_awaited_once_with(1)
    repo.list_by_activity_ids.assert_awaited_once_with([1, 2, 3])
    assert result == ["org1", "org2"]


@pytest.mark.unit
async def test_list_by_activity_without_descendants():
    repo = AsyncMock(spec=OrganizationRepository)
    activity_service = AsyncMock(spec=ActivityService)
    repo.list_by_activity_ids = AsyncMock(return_value=["org1"])

    service = OrganizationService(repo, activity_service)
    result = await service.list_by_activity(activity_id=5, include_descendants=False)

    activity_service.get_descendant_ids.assert_not_called()
    repo.list_by_activity_ids.assert_awaited_once_with([5])
    assert result == ["org1"]


@pytest.mark.unit
async def test_get_by_id_not_found():
    repo = AsyncMock(spec=OrganizationRepository)
    activity_service = AsyncMock(spec=ActivityService)
    repo.get_by_id = AsyncMock(return_value=None)

    service = OrganizationService(repo, activity_service)

    with pytest.raises(HTTPException) as exc:
        await service.get_by_id(organization_id=999)

    assert exc.value.status_code == 404
