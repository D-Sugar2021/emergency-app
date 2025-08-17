from fastapi.testclient import TestClient
import pytest

pytestmark = pytest.mark.asyncio


class TestGuardianVault:
    @pytest.fixture(scope="class")
    def test_user_token(self, client: TestClient) -> str:
        client.post(
            "/api/v1/users/",
            json={"email": "vaultuser@example.com", "password": "password123"},
        )
        login_response = client.post(
            "/api/v1/login/access-token",
            data={"username": "vaultuser@example.com", "password": "password123"},
        )
        return login_response.json()["access_token"]

    async def test_update_and_read_vault(self, client: TestClient, test_user_token: str):
        headers = {"Authorization": f"Bearer {test_user_token}"}
        vault_data = {
            "emergency_contacts": [
                {"name": "Jane Doe", "phone": "123-456-7890", "relationship": "Spouse"}
            ],
            "allergies": "Peanuts",
            "medical_conditions": "Asthma",
        }

        # Update the vault
        update_response = client.put("/api/v1/vault/", json=vault_data, headers=headers)
        assert update_response.status_code == 200
        data = update_response.json()
        assert data["allergies"] == "Peanuts"
        assert data["medical_conditions"] == "Asthma"
        assert len(data["emergency_contacts"]) == 1
        assert data["emergency_contacts"][0]["name"] == "Jane Doe"

        # Read the vault and verify the data
        read_response = client.get("/api/v1/vault/", headers=headers)
        assert read_response.status_code == 200
        read_data = read_response.json()
        assert read_data == data
