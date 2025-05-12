from unittest.mock import AsyncMock, MagicMock

import pytest

from src.auth.application.exeptions.exeptions import InvalidTokenError
from src.auth.application.use_cases.validate_token import ValidateTokenUseCase
from src.auth.domain.entity.user import User
from src.tests.unit.conftest import mock_token_service, mock_uow


@pytest.mark.asyncio
async def test_validate_token_success(mock_token_service, mock_uow):
    mock_token_service.validate_token.return_value = "test@example.com"
    mock_uow.user_repository.get_by_email.return_value = MagicMock()

    use_case = ValidateTokenUseCase(mock_token_service, mock_uow)
    await use_case.execute("valid_token")

    mock_token_service.validate_token.assert_called_once_with("valid_token")
    mock_uow.user_repository.get_by_email.assert_awaited_once_with("test@example.com")
    mock_uow.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_validate_invalid_token(mock_token_service, mock_uow):
    mock_token_service.validate_token.side_effect = InvalidTokenError("Invalid")

    use_case = ValidateTokenUseCase(mock_token_service, mock_uow)

    with pytest.raises(InvalidTokenError):
        await use_case.execute("invalid_token")
