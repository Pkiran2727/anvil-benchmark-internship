"""Task 5 Tests — Email format validation on register."""
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
        "SECRET_KEY": "test-secret-t5",
    })
    with app.app_context():
        db.create_all()
        with app.test_client() as c:
            yield c


def test_invalid_email_no_at_returns_400(client):
    """Email without @ returns 400."""
    res = client.post("/api/auth/register", json={
        "username": "u1", "email": "notanemail", "password": "pass"
    })
    assert res.status_code == 400


def test_invalid_email_no_domain_returns_400(client):
    """Email with @ but no domain returns 400."""
    res = client.post("/api/auth/register", json={
        "username": "u2", "email": "user@", "password": "pass"
    })
    assert res.status_code == 400


def test_invalid_email_no_local_returns_400(client):
    """Email starting with @ returns 400."""
    res = client.post("/api/auth/register", json={
        "username": "u3", "email": "@domain.com", "password": "pass"
    })
    assert res.status_code == 400


def test_invalid_email_missing_dot_in_domain_returns_400(client):
    """Email domain without dot returns 400."""
    res = client.post("/api/auth/register", json={
        "username": "u4", "email": "user@nodot", "password": "pass"
    })
    assert res.status_code == 400


def test_valid_email_registers_successfully(client):
    """Valid email returns 201."""
    res = client.post("/api/auth/register", json={
        "username": "validuser", "email": "valid@example.com", "password": "pass"
    })
    assert res.status_code == 201


def test_valid_email_with_subdomains_accepted(client):
    """Valid email with subdomain returns 201."""
    res = client.post("/api/auth/register", json={
        "username": "subdomain", "email": "user@mail.example.co.uk", "password": "pass"
    })
    assert res.status_code == 201


def test_valid_email_with_plus_accepted(client):
    """Valid email with + tag returns 201."""
    res = client.post("/api/auth/register", json={
        "username": "plususer", "email": "user+tag@example.com", "password": "pass"
    })
    assert res.status_code == 201


def test_missing_email_still_returns_400(client):
    """Missing email field still returns 400 (existing validation)."""
    res = client.post("/api/auth/register", json={
        "username": "noemail", "password": "pass"
    })
    assert res.status_code == 400
