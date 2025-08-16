from fastapi.testclient import TestClient
import pytest

# Mark all tests in this module as async
pytestmark = pytest.mark.asyncio

async def test_create_user(client: TestClient):
    response = client.post(
        "/api/v1/users/",
        json={"email": "test@example.com", "password": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data
    assert "is_active" in data
    # Test creating a duplicate user
    response = client.post(
        "/api/v1/users/",
        json={"email": "test@example.com", "password": "password123"},
    )
    assert response.status_code == 400


async def test_login(client: TestClient):
    response = client.post(
        "/api/v1/login/access-token",
        data={"username": "test@example.com", "password": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


async def test_read_me(client: TestClient):
    # First, login to get a token
    login_response = client.post(
        "/api/v1/login/access-token",
        data={"username": "test@example.com", "password": "password123"},
    )
    token = login_response.json()["access_token"]

    # Then, use the token to access the protected endpoint
    me_response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert me_response.status_code == 200
    data = me_response.json()
    assert data["email"] == "test@example.com"
