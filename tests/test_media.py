import io

from fastapi.testclient import TestClient
import pytest

pytestmark = pytest.mark.asyncio

class TestMedia:
    @pytest.fixture(scope="class")
    def test_user_token(self, client: TestClient) -> str:
        client.post(
            "/api/v1/users/",
            json={"email": "mediauser@example.com", "password": "password123"},
        )
        login_response = client.post(
            "/api/v1/login/access-token",
            data={"username": "mediauser@example.com", "password": "password123"},
        )
        return login_response.json()["access_token"]

    async def test_upload_media(self, client: TestClient, test_user_token: str):
        headers = {"Authorization": f"Bearer {test_user_token}"}
        file_content = b"This is a test file."
        files = {"file": ("test.txt", io.BytesIO(file_content), "text/plain")}
        response = client.post("/api/v1/media/", files=files, headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["filename"] == "test.txt"
        assert data["content_type"] == "text/plain"
        assert data["size"] == len(file_content)

    async def test_list_media(self, client: TestClient, test_user_token: str):
        headers = {"Authorization": f"Bearer {test_user_token}"}
        response = client.get("/api/v1/media/", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        assert data[0]["filename"] == "test.txt"

    async def test_get_media_item(self, client: TestClient, test_user_token: str):
        headers = {"Authorization": f"Bearer {test_user_token}"}
        # First, get the list of media to find an ID
        list_response = client.get("/api/v1/media/", headers=headers)
        media_id = list_response.json()[0]["id"]

        # Then, get the item by ID
        response = client.get(f"/api/v1/media/{media_id}", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == media_id
        assert data["filename"] == "test.txt"

    async def test_delete_media_item(self, client: TestClient, test_user_token: str):
        headers = {"Authorization": f"Bearer {test_user_token}"}
        # First, get the list of media to find an ID
        list_response = client.get("/api/v1/media/", headers=headers)
        media_id = list_response.json()[0]["id"]

        # Then, delete the item
        response = client.delete(f"/api/v1/media/{media_id}", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == media_id

        # Verify it's gone
        get_response = client.get(f"/api/v1/media/{media_id}", headers=headers)
        assert get_response.status_code == 404
