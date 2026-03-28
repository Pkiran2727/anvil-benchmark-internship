"""Task 2 Tests — PUT /api/profile endpoint."""
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
        "SECRET_KEY": "test-secret-t2",
    })
    with app.app_context():
        db.create_all()
        with app.test_client() as c:
            yield c


@pytest.fixture(scope="module")
def token(client):
    client.post("/api/auth/register", json={
        "username": "t2user", "email": "t2@example.com", "password": "pass1234"
    })
    res = client.post("/api/auth/login", json={"username": "t2user", "password": "pass1234"})
    return res.get_json()["token"]


def test_update_profile_no_token_returns_401(client):
    """PUT /api/profile with no auth returns 401."""
    res = client.put("/api/profile", json={"bio": "hello"})
    assert res.status_code == 401


def test_update_profile_invalid_token_returns_401(client):
    """PUT /api/profile with invalid token returns 401."""
    res = client.put("/api/profile", json={"bio": "hi"},
                     headers={"Authorization": "Bearer invalid"})
    assert res.status_code == 401


def test_update_bio_returns_200(client, token):
    """PUT /api/profile with valid token and bio returns 200."""
    res = client.put("/api/profile", json={"bio": "My bio"},
                     headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200


def test_update_bio_value_persists(client, token):
    """Updated bio is reflected in the response."""
    client.put("/api/profile", json={"bio": "Updated bio"},
               headers={"Authorization": f"Bearer {token}"})
    res = client.put("/api/profile", json={"bio": "Updated bio"},
                     headers={"Authorization": f"Bearer {token}"})
    data = res.get_json()
    assert data.get("bio") == "Updated bio"


def test_update_email_returns_200(client, token):
    """PUT /api/profile can update email."""
    res = client.put("/api/profile", json={"email": "newemail@example.com"},
                     headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200


def test_update_profile_response_has_required_fields(client, token):
    """Updated profile response contains id, username, email, bio."""
    res = client.put("/api/profile", json={"bio": "check"},
                     headers={"Authorization": f"Bearer {token}"})
    data = res.get_json()
    for field in ("id", "username", "email", "bio"):
        assert field in data, f"Missing field: {field}"


def test_update_with_duplicate_email_returns_409(client, token):
    """Updating to an email already used by another user returns 409."""
    client.post("/api/auth/register", json={
        "username": "other2", "email": "other2@example.com", "password": "pass"
    })
    res = client.put("/api/profile", json={"email": "other2@example.com"},
                     headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 409


def test_update_profile_returns_json(client, token):
    """PUT /api/profile returns JSON content type."""
    res = client.put("/api/profile", json={"bio": "json?"},
                     headers={"Authorization": f"Bearer {token}"})
    assert "application/json" in res.content_type
