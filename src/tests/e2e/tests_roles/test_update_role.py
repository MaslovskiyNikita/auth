import pytest
from sqlalchemy import select

from src.auth.infrastructure.db.models.user import UserDB
from src.auth.infrastructure.db.models.user_role import RoleDB


async def test_update_role_flow(auth_client, session, test_user, setup_permissions):
    await auth_client.post(
        "/roles/create", json={"name": "admin", "permissions_name": ["create", "read"]}
    )

    response = await auth_client.patch(
        "/roles/update", json={"name": "admin", "update_data": {"name": "superadmin"}}
    )

    assert response.status_code == 200
    result = await session.execute(select(RoleDB).where(RoleDB.name == "superadmin"))
    assert result.scalar_one().name == "superadmin"
