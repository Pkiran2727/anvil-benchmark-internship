"""Task 1 Tests — GET /api/profile endpoint."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "flask-task-api"))

import pytest
from app import create_app
from models import db


@pytest.fixture(scope="module")
def client():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SECRET_KEY": "test-secret-t1",
    })
    with app.app_context():
        db.create_all()
        with app.test_client() as c:
            yield c


@pytest.fixture(scope="module")
def token(client):
    client.post("/api/auth/register", json={
        "username": "t1user", "email": "t1@example.com", "password": "pass1234"
    })
    res = client.post("/api/auth/login", json={"username": "t1user", "password": "pass1234"})
    return res.get_json()["token"]


def test_profile_no_token_returns_401(client):
    """GET /api/profile with no auth returns 401."""
    res = client.get("/api/profile")
    assert res.status_code == 401


def test_profile_invalid_token_returns_401(client):
    """GET /api/profile with a malformed token returns 401."""
    res = client.get("/api/profile", headers={"Authorization": "Bearer bad.token"})
    assert res.status_code == 401


def test_profile_no_bearer_prefix_returns_401(client):
    """Authorization header without 'Bearer ' prefix returns 401."""
    res = client.get("/api/profile", headers={"Authorization": "justtoken"})
    assert res.status_code == 401


def test_profile_valid_token_returns_200(client, token):
    """GET /api/profile with valid token returns 200."""
    res = client.get("/api/profile", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200


def test_profile_contains_username(client, token):
    """Profile response contains correct username."""
    res = client.get("/api/profile", headers={"Authorization": f"Bearer {token}"})
    data = res.get_json()
    assert "username" in data
    assert data["username"] == "t1user"


def test_profile_contains_email(client, token):
    """Profile response contains correct email."""
    res = client.get("/api/profile", headers={"Authorization": f"Bearer {token}"})
    data = res.get_json()
    assert "email" in data
    assert data["email"] == "t1@example.com"


def test_profile_contains_bio(client, token):
    """Profile response contains bio field."""
    res = client.get("/api/profile", headers={"Authorization": f"Bearer {token}"})
    data = res.get_json()
    assert "bio" in data


def test_profile_returns_json_content_type(client, token):
    """Profile endpoint returns application/json."""
    res = client.get("/api/profile", headers={"Authorization": f"Bearer {token}"})
    assert "application/json" in res.content_type
