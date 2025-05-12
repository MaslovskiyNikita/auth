# tests/e2e/test_auth_flow.py
import pytest
from httpx import AsyncClient
from sqlalchemy import select

from src.auth.infrastructure.db.models.user import UserDB


@pytest.mark.asyncio
async def test_full_registration_flow(async_client: AsyncClient, session):

    register_data = {
        "email": "e2e_test@example.com",
        "username": "e2e_user",
        "password": "StrongPassword123!",
        "first_name": "EndToEnd",
        "last_name": "Test",
    }

    registration_response = await async_client.post("/users/", json=register_data)
    assert registration_response.status_code == 200


@pytest.mark.asyncio
async def test_registration_with_invalid_data(async_client: AsyncClient):
    invalid_data = [
        {"email": "invalid@example.com", "password": "short"},
        {
            "email": "not-an-email",
            "username": "user",
            "password": "ValidPass123!",
            "first_name": "Test",
            "last_name": "User",
        },
    ]

    for data in invalid_data:
        response = await async_client.post("/users/", json=data)
        assert response.status_code == 422


@pytest.mark.asyncio
async def test_duplicate_registration(async_client: AsyncClient):

    user_data = {
        "email": "duplicate@example.com",
        "username": "unique_user",
        "password": "Password123!",
        "first_name": "Test",
        "last_name": "User",
    }

    response1 = await async_client.post("/users/", json=user_data)
    assert response1.status_code == 200
    response2 = await async_client.post("/users/", json=user_data)
    assert response2.status_code == 400
