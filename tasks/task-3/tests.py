"""Task 3 Tests — DELETE /api/account endpoint."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "flask-task-api"))

import pytest
from app import create_app
from models import db


@pytest.fixture(scope="module")
def app_instance():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SECRET_KEY": "test-secret-t3",
    })
    with app.app_context():
        db.create_all()
        yield app


@pytest.fixture(scope="module")
def client(app_instance):
    return app_instance.test_client()


def _register_and_login(client, username, email):
    client.post("/api/auth/register", json={
        "username": username, "email": email, "password": "pass1234"
    })
    res = client.post("/api/auth/login", json={"username": username, "password": "pass1234"})
    return res.get_json()["token"]


def test_delete_account_no_token_returns_401(client):
    """DELETE /api/account with no auth returns 401."""
    res = client.delete("/api/account")
    assert res.status_code == 401


def test_delete_account_invalid_token_returns_401(client):
    """DELETE /api/account with invalid token returns 401."""
    res = client.delete("/api/account", headers={"Authorization": "Bearer bad"})
    assert res.status_code == 401


def test_delete_account_returns_200(client):
    """DELETE /api/account with valid token returns 200."""
    token = _register_and_login(client, "del1user", "del1@example.com")
    res = client.delete("/api/account", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200


def test_delete_account_returns_json(client):
    """DELETE /api/account returns JSON response."""
    token = _register_and_login(client, "del2user", "del2@example.com")
    res = client.delete("/api/account", headers={"Authorization": f"Bearer {token}"})
    assert "application/json" in res.content_type


def test_delete_account_response_has_message(client):
    """DELETE /api/account response contains a 'message' key."""
    token = _register_and_login(client, "del3user", "del3@example.com")
    res = client.delete("/api/account", headers={"Authorization": f"Bearer {token}"})
    data = res.get_json()
    assert "message" in data


def test_deleted_user_cannot_login_again(client):
    """After deletion, login with same credentials fails."""
    token = _register_and_login(client, "del4user", "del4@example.com")
    client.delete("/api/account", headers={"Authorization": f"Bearer {token}"})
    res = client.post("/api/auth/login", json={"username": "del4user", "password": "pass1234"})
    assert res.status_code == 401


def test_deleted_user_cannot_re_register_same_email(client):
    """After deletion, re-registering with same email succeeds (email freed)."""
    token = _register_and_login(client, "del5user", "del5@example.com")
    client.delete("/api/account", headers={"Authorization": f"Bearer {token}"})
    res = client.post("/api/auth/register", json={
        "username": "del5new", "email": "del5@example.com", "password": "pass"
    })
    assert res.status_code == 201


def test_delete_token_no_longer_valid(client):
    """After account deletion, old token returns 401 on protected routes."""
    token = _register_and_login(client, "del6user", "del6@example.com")
    client.delete("/api/account", headers={"Authorization": f"Bearer {token}"})
    res = client.delete("/api/account", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 401
