import pytest
from sqlalchemy import select

from src.auth.infrastructure.db.models.user import UserDB
from src.auth.infrastructure.db.models.user_role import RoleDB


@pytest.mark.asyncio
async def test_create_role_flow(
    auth_client, session, test_user: UserDB, setup_permissions
):

    role_data = {
        "name": "admin",
        "permissions_name": ["create", "read", "update", "delete"],
    }

    await auth_client.post("/roles/create", json=role_data)

    role_to_delete = "admin"

    response = await auth_client.delete(
        f"roles/{role_to_delete}",
    )

    assert response.status_code == 200
