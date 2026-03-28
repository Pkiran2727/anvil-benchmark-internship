"""Task 8 Tests — Rate limiting on POST /api/auth/login."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "flask-task-api"))

import pytest
from app import create_app
from models import db


@pytest.fixture(scope="function")
def client():
    """Fresh client per test to reset rate-limit state."""
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SECRET_KEY": "test-secret-t8",
    })
    with app.app_context():
        db.create_all()
        app.test_client().post("/api/auth/register", json={
            "username": "rateuser", "email": "rate@example.com", "password": "pass1234"
        })
        with app.test_client() as c:
            yield c


def test_login_within_limit_returns_200_or_401(client):
    """First login attempt is not rate-limited."""
    res = client.post("/api/auth/login", json={"username": "rateuser", "password": "pass1234"})
    assert res.status_code in (200, 401)


def test_login_valid_credentials_not_blocked_initially(client):
    """Valid credentials in first 5 attempts succeed."""
    res = client.post("/api/auth/login", json={"username": "rateuser", "password": "pass1234"})
    assert res.status_code == 200


def test_login_rate_limit_triggers_429_after_5(client):
    """After 5 attempts, 6th returns 429."""
    for _ in range(5):
        client.post("/api/auth/login", json={"username": "rateuser", "password": "wrong"})
    res = client.post("/api/auth/login", json={"username": "rateuser", "password": "wrong"})
    assert res.status_code == 429


def test_rate_limit_error_has_error_key(client):
    """429 response contains 'error' key."""
    for _ in range(5):
        client.post("/api/auth/login", json={"username": "rateuser", "password": "wrong"})
    res = client.post("/api/auth/login", json={"username": "rateuser", "password": "wrong"})
    assert "error" in (res.get_json() or {})


def test_get_items_not_rate_limited(client):
    """Rate limiting does not affect GET /api/items."""
    for _ in range(10):
        res = client.get("/api/items")
        assert res.status_code == 200


def test_register_not_rate_limited_by_login_limit(client):
    """Rate limiting on login does not block register endpoint."""
    for _ in range(6):
        client.post("/api/auth/login", json={"username": "rateuser", "password": "wrong"})
    res = client.post("/api/auth/register", json={
        "username": "newuser99", "email": "new99@example.com", "password": "pass"
    })
    assert res.status_code in (201, 409)  # not 429


def test_fifth_attempt_still_processed(client):
    """The 5th attempt is still processed (not blocked)."""
    for _ in range(4):
        client.post("/api/auth/login", json={"username": "rateuser", "password": "wrong"})
    res = client.post("/api/auth/login", json={"username": "rateuser", "password": "pass1234"})
    assert res.status_code == 200  # 5th attempt with correct creds succeeds


def test_sixth_attempt_returns_429(client):
    """6th attempt always returns 429 regardless of credentials."""
    for _ in range(5):
        client.post("/api/auth/login", json={"username": "rateuser", "password": "wrong"})
    res = client.post("/api/auth/login", json={"username": "rateuser", "password": "pass1234"})
    assert res.status_code == 429
