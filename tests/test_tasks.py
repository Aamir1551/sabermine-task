from __future__ import annotations
import os
import tempfile
import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db


TMP_DIR = tempfile.gettempdir()
TEST_DB_PATH = os.path.join(TMP_DIR, "test_app.db")
TEST_DATABASE_URL = f"sqlite:///{TEST_DB_PATH}"

# Clean old test DB if present
if os.path.exists(TEST_DB_PATH):
    os.remove(TEST_DB_PATH)

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Apply dependency override for the whole test module
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="module")
def client():
    # Context manager ensures FastAPI lifespan runs properly
    with TestClient(app) as c:
        yield c


def test_create_task_success(client: TestClient):
    payload = {
        "title": "Pay bills",
        "description": "Electricity + water",
        "priority": 1,
        "due_date": "2030-01-30T15:00:00"
    }
    r = client.post("/tasks/", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["id"] > 0
    assert data["title"] == "Pay bills"
    assert data["priority"] == 1
    assert data["completed"] is False


def test_create_task_invalid_priority(client: TestClient):
    payload = {
        "title": "Bad prio",
        "description": "nope",
        "priority": 99,  # invalid
        "due_date": "2030-01-30T15:00:00"
    }
    r = client.post("/tasks/", json=payload)
    assert r.status_code == 422  # pydantic validation error


def test_get_nonexistent_task(client: TestClient):
    r = client.get("/tasks/999999/")
    assert r.status_code == 404
    assert r.json()["detail"] == "Task not found."
