import pytest
from fastapi import status
from httpx import AsyncClient

from src.tests.factories import UserFactory


@pytest.mark.asyncio
async def test_create_user_success(
    async_client: AsyncClient,
):

    response = await async_client.get("/health")
    assert response.status_code == 200

    user_data = UserFactory.build()
    user_dict = {
        "email": user_data.email,
        "username": user_data.username,
        "first_name": user_data.first_name,
        "last_name": user_data.last_name,
        "password": "testpassword123!",
    }

    response = await async_client.post("/users/", json=user_dict)
    assert response.status_code == status.HTTP_200_OK
