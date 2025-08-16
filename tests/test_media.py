import io
import json

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

    async def test_upload_media_with_metadata(
        self, client: TestClient, test_user_token: str
    ):
        headers = {"Authorization": f"Bearer {test_user_token}"}
        file_content = b"This is another test file."
        files = {"file": ("test2.txt", io.BytesIO(file_content), "text/plain")}
        form_data = {
            "latitude": 34.0522,
            "longitude": -118.2437,
            "bookmarks": json.dumps([10, 20, 30]),
            "tags": json.dumps(["test", "metadata"]),
        }
        response = client.post(
            "/api/v1/media/", files=files, data=form_data, headers=headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["filename"] == "test2.txt"
        assert data["latitude"] == 34.0522
        assert data["longitude"] == -118.2437
        assert data["bookmarks"] == [10, 20, 30]
        assert data["tags"] == ["test", "metadata"]

    async def test_list_media(self, client: TestClient, test_user_token: str):
        headers = {"Authorization": f"Bearer {test_user_token}"}
        response = client.get("/api/v1/media/", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1  # Should have at least one from the previous tests

    async def test_get_media_item(self, client: TestClient, test_user_token: str):
        headers = {"Authorization": f"Bearer {test_user_token}"}
        list_response = client.get("/api/v1/media/", headers=headers)
        media_id = list_response.json()[0]["id"]
        response = client.get(f"/api/v1/media/{media_id}", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == media_id

    async def test_delete_media_item(self, client: TestClient, test_user_token: str):
        headers = {"Authorization": f"Bearer {test_user_token}"}
        list_response = client.get("/api/v1/media/", headers=headers)
        media_id_to_delete = list_response.json()[0]["id"]
        response = client.delete(
            f"/api/v1/media/{media_id_to_delete}", headers=headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == media_id_to_delete
        get_response = client.get(
            f"/api/v1/media/{media_id_to_delete}", headers=headers
        )
        assert get_response.status_code == 404
