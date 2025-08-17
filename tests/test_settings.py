from fastapi.testclient import TestClient
import pytest

pytestmark = pytest.mark.asyncio


class TestUserSettings:
    @pytest.fixture(scope="class")
    def test_user_token(self, client: TestClient) -> str:
        client.post(
            "/api/v1/users/",
            json={"email": "settingsuser@example.com", "password": "password123"},
        )
        login_response = client.post(
            "/api/v1/login/access-token",
            data={"username": "settingsuser@example.com", "password": "password123"},
        )
        return login_response.json()["access_token"]

    async def test_read_and_update_settings(
        self, client: TestClient, test_user_token: str
    ):
        headers = {"Authorization": f"Bearer {test_user_token}"}

        # Read initial settings (should be created with defaults)
        read_response = client.get("/api/v1/settings/", headers=headers)
        assert read_response.status_code == 200
        data = read_response.json()
        assert data["chime_volume"] == 1.0

        # Update settings
        update_data = {"chime_volume": 0.5}
        update_response = client.put(
            "/api/v1/settings/", json=update_data, headers=headers
        )
        assert update_response.status_code == 200
        updated_data = update_response.json()
        assert updated_data["chime_volume"] == 0.5

        # Read again to verify
        read_again_response = client.get("/api/v1/settings/", headers=headers)
        assert read_again_response.status_code == 200
        final_data = read_again_response.json()
        assert final_data["chime_volume"] == 0.5
