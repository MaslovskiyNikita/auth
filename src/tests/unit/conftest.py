from unittest.mock import AsyncMock, MagicMock

import pytest


@pytest.fixture
def fake_user():
    return MagicMock(is_active=False)


@pytest.fixture
def mock_token_service():
    service = MagicMock()
    service.validate_token = MagicMock()
    return service


@pytest.fixture
def mock_uow(fake_user):
    uow = AsyncMock()
    uow.__aenter__.return_value = uow
    uow.__aexit__ = AsyncMock()
    uow.user_repository = AsyncMock()
    uow.user_repository.get_by_email = AsyncMock(return_value=fake_user)

    uow.commit = AsyncMock()

    return uow
