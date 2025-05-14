import pytest
from fastapi import status
from httpx import AsyncClient

from src.auth.application.exeptions.exeptions import (
    InvalidPasswordError,
    UserNotActiveError,
    UserNotFoundError,
)
from src.tests.factories import UserFactory


@pytest.mark.asyncio
async def test_successful_login(async_client: AsyncClient, session):

    user = await UserFactory.create_async(
        session, email="test@example.com", password="valid_password", is_active=True
    )

    response = await async_client.post(
        "/users/login",
        params={"email": "test@example.com", "password": "valid_password"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert "X-Access-Token" in response.headers
    assert "X-Refresh-Token" in response.headers
    assert response.json() == {"message": "Login successful"}


@pytest.mark.asyncio
async def test_login_with_invalid_email(async_client: AsyncClient):
    response = await async_client.post(
        "/users/login", params={"email": "asdsdgfvcx", "password": "any_password"}
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_login_with_invalid_password(async_client: AsyncClient, session):
    user = await UserFactory.create_async(
        session, email="test@example.com", password="correct_password", is_active=True
    )

    response = await async_client.post(
        "/users/login",
        params={"email": "test@example.com", "password": "wrong_password"},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_login_inactive_user(async_client: AsyncClient, session):

    user = await UserFactory.create_async(
        session,
        email="inactive@example.com",
        password="valid_password",
        is_active=False,
    )
    response = await async_client.post(
        "/users/login",
        params={"email": "inactive@example.com", "password": "valid_password"},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_login_without_credentials(async_client: AsyncClient):
    response = await async_client.post("/users/login")

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
