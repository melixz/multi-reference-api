from unittest.mock import AsyncMock

import pytest

from app.repositories.activity import ActivityRepository
from app.services.activity import ActivityService


@pytest.mark.unit
async def test_ensure_depth_limit_ok():
    repo = AsyncMock(spec=ActivityRepository)
    repo.get_depth_from_parent = AsyncMock(return_value=2)
    service = ActivityService(repo)

    await service.ensure_depth_limit(parent_id=1)

    repo.get_depth_from_parent.assert_awaited_once_with(1)


@pytest.mark.unit
async def test_ensure_depth_limit_exceeded():
    repo = AsyncMock(spec=ActivityRepository)
    repo.get_depth_from_parent = AsyncMock(return_value=3)
    service = ActivityService(repo)

    with pytest.raises(ValueError, match="Activity nesting depth limit exceeded"):
        await service.ensure_depth_limit(parent_id=1)
