import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.db import get_session
from app.main import app


@pytest.fixture
def client():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    SQLModel.metadata.create_all(engine)

    def override():
        with Session(engine) as s:
            yield s

    app.dependency_overrides[get_session] = override
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


def auth_headers(client, email="a@example.com", password="password123"):
    client.post("/auth/register", json={"email": email, "password": password})
    token = client.post("/auth/token", data={"username": email, "password": password}).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}


def test_register_duplicate_and_short_password(client):
    assert client.post("/auth/register", json={"email": "x@example.com", "password": "password123"}).status_code == 201
    assert client.post("/auth/register", json={"email": "x@example.com", "password": "password123"}).status_code == 409
    assert client.post("/auth/register", json={"email": "y@example.com", "password": "short"}).status_code == 422


def test_items_crud_and_isolation(client):
    h = auth_headers(client)
    created = client.post("/items", json={"title": "First"}, headers=h)
    assert created.status_code == 201
    item_id = created.json()["id"]
    assert client.patch(f"/items/{item_id}", json={"title": "Renamed"}, headers=h).json()["title"] == "Renamed"
    assert len(client.get("/items", headers=h).json()) == 1

    other = auth_headers(client, "b@example.com")
    assert client.get(f"/items/{item_id}", headers=other).status_code == 404

    assert client.delete(f"/items/{item_id}", headers=h).status_code == 204
    assert client.get("/items", headers=h).json() == []


def test_requires_auth(client):
    assert client.get("/items").status_code == 401
