from unittest.mock import AsyncMock, MagicMock

import pytest


@pytest.fixture(scope="session")
def mock_token_service():
    service = MagicMock()
    service.validate_token = MagicMock()
    return service


@pytest.fixture(scope="session")
def mock_uow():
    uow = MagicMock()
    uow.user_repository = AsyncMock()
    uow.user_repository.get_by_email = AsyncMock()
    uow.commit = AsyncMock()
    return uow
