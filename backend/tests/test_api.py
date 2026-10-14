from fastapi.testclient import TestClient

from tests.conftest import auth_header


def register(client: TestClient, email: str, name: str = "Test User") -> None:
    response = client.post("/api/auth/register", json={"name": name, "email": email, "password": "password123"})
    assert response.status_code == 201
    assert "hashed_password" not in response.json()


def test_register_and_login(client: TestClient) -> None:
    register(client, "user@example.com")
    response = client.post("/api/auth/login", json={"email": "user@example.com", "password": "password123"})
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert response.json()["access_token"]


def test_create_task_for_current_user(client: TestClient) -> None:
    register(client, "user@example.com")
    response = client.post("/api/tasks", json={"title": "Learn FastAPI", "priority": "high"}, headers=auth_header(client, "user@example.com", "password123"))
    assert response.status_code == 201
    assert response.json()["title"] == "Learn FastAPI"
    assert response.json()["status"] == "todo"


def test_cannot_access_another_users_task(client: TestClient) -> None:
    register(client, "owner@example.com", "Owner")
    owner_headers = auth_header(client, "owner@example.com", "password123")
    task = client.post("/api/tasks", json={"title": "Private task"}, headers=owner_headers).json()
    register(client, "other@example.com", "Other")
    other_headers = auth_header(client, "other@example.com", "password123")

    response = client.get(f"/api/tasks/{task['id']}", headers=other_headers)
    assert response.status_code == 404
