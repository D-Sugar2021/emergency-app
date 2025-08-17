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

    async def test_upload_and_ai_processing(self, client: TestClient, test_user_token: str):
        headers = {"Authorization": f"Bearer {test_user_token}"}
        file_content = b"This is a test file for AI processing."
        files = {"file": ("ai_test.txt", io.BytesIO(file_content), "text/plain")}
        form_data = {
            "latitude": 34.0522,
            "longitude": -118.2437,
            "bookmarks": json.dumps([1, 2, 3]),
            "tags": json.dumps(["ai", "test"]),
        }
        response = client.post(
            "/api/v1/media/", files=files, data=form_data, headers=headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["filename"] == "ai_test.txt"
        assert data["ai_processing_status"] == "completed"
        assert "dummy transcription" in data["transcription"]
        assert "dummy summary" in data["summary"]

        # Verify that the data is retrievable
        media_id = data["id"]
        get_response = client.get(f"/api/v1/media/{media_id}", headers=headers)
        assert get_response.status_code == 200
        get_data = get_response.json()
        assert get_data["transcription"] == data["transcription"]
        assert get_data["summary"] == data["summary"]

    async def test_list_media(self, client: TestClient, test_user_token: str):
        headers = {"Authorization": f"Bearer {test_user_token}"}
        response = client.get("/api/v1/media/", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    async def test_delete_media_item(self, client: TestClient, test_user_token: str):
        headers = {"Authorization": f"Bearer {test_user_token}"}

        # First, upload a file to delete
        file_content = b"This file will be deleted."
        files = {"file": ("delete_me.txt", io.BytesIO(file_content), "text/plain")}
        upload_response = client.post("/api/v1/media/", files=files, headers=headers)
        media_id_to_delete = upload_response.json()["id"]

        # Then, delete the item
        response = client.delete(
            f"/api/v1/media/{media_id_to_delete}", headers=headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == media_id_to_delete

        # Verify it's gone
        get_response = client.get(
            f"/api/v1/media/{media_id_to_delete}", headers=headers
        )
        assert get_response.status_code == 404
