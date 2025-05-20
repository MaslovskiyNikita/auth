from httpx import AsyncClient

from src.auth.main.settings import settings


async def test_successful_token_refresh(
    auth_client: AsyncClient,
    test_user,
):

    login_response = await auth_client.post(
        "/users/login",
        params={"email": test_user.email, "password": "strongpassword123"},
    )

    assert login_response.status_code == 200
    refresh_token = login_response.json()["refresh_token"]
    assert refresh_token, "No refresh token returned"

    response = await auth_client.post(
        "/tokens/refresh", json={"refreshToken": refresh_token}
    )

    data = response.json()
    assert response.status_code == 200

    assert "access_token" in data
    assert "refresh_token" in data
