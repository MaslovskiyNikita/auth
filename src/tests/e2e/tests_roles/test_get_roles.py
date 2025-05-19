import pytest
from sqlalchemy import select

from src.auth.infrastructure.db.models.user import UserDB
from src.auth.infrastructure.db.models.user_role import RoleDB


@pytest.mark.asyncio
async def test_create_role_flow(
    auth_client, session, test_user: UserDB, setup_permissions
):

    response = await auth_client.get("/roles/read")

    assert response.status_code == 200
