"""Task 6 Tests — POST /api/auth/refresh endpoint."""
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
        "SECRET_KEY": "test-secret-t6",
    })
    with app.app_context():
        db.create_all()
        with app.test_client() as c:
            yield c


@pytest.fixture(scope="module")
def token(client):
    client.post("/api/auth/register", json={
        "username": "t6user", "email": "t6@example.com", "password": "pass1234"
    })
    res = client.post("/api/auth/login", json={"username": "t6user", "password": "pass1234"})
    return res.get_json()["token"]


def test_refresh_no_token_returns_401(client):
    """POST /api/auth/refresh with no token returns 401."""
    res = client.post("/api/auth/refresh")
    assert res.status_code == 401


def test_refresh_invalid_token_returns_401(client):
    """POST /api/auth/refresh with invalid token returns 401."""
    res = client.post("/api/auth/refresh", headers={"Authorization": "Bearer bad"})
    assert res.status_code == 401


def test_refresh_valid_token_returns_200(client, token):
    """POST /api/auth/refresh with valid token returns 200."""
    res = client.post("/api/auth/refresh", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200


def test_refresh_response_has_token_key(client, token):
    """Refresh response contains 'token' key."""
    res = client.post("/api/auth/refresh", headers={"Authorization": f"Bearer {token}"})
    data = res.get_json()
    assert "token" in data


def test_refresh_new_token_is_string(client, token):
    """New token is a non-empty string."""
    res = client.post("/api/auth/refresh", headers={"Authorization": f"Bearer {token}"})
    new_token = res.get_json()["token"]
    assert isinstance(new_token, str) and len(new_token) > 10


def test_refresh_new_token_is_usable(client, token):
    """New token can authenticate on protected endpoints."""
    res = client.post("/api/auth/refresh", headers={"Authorization": f"Bearer {token}"})
    new_token = res.get_json()["token"]
    # Use new token to create an item (a protected endpoint)
    r2 = client.post("/api/items", json={"name": "test-item"},
                     headers={"Authorization": f"Bearer {new_token}"})
    assert r2.status_code == 201


def test_refresh_returns_json(client, token):
    """Refresh endpoint returns JSON content type."""
    res = client.post("/api/auth/refresh", headers={"Authorization": f"Bearer {token}"})
    assert "application/json" in res.content_type


def test_refresh_works_with_newly_refreshed_token(client, token):
    """Refreshing twice in a row both return 200."""
    r1 = client.post("/api/auth/refresh", headers={"Authorization": f"Bearer {token}"})
    new_token = r1.get_json()["token"]
    r2 = client.post("/api/auth/refresh", headers={"Authorization": f"Bearer {new_token}"})
    assert r2.status_code == 200
