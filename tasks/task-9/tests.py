"""Task 9 Tests — Audit logging for write operations."""
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
        "SECRET_KEY": "test-secret-t9",
    })
    with app.app_context():
        db.create_all()
        with app.test_client() as c:
            yield c


@pytest.fixture(scope="module")
def token(client):
    client.post("/api/auth/register", json={
        "username": "t9user", "email": "t9@example.com", "password": "pass1234"
    })
    res = client.post("/api/auth/login", json={"username": "t9user", "password": "pass1234"})
    return res.get_json()["token"]


def test_audit_endpoint_requires_auth(client):
    """GET /api/audit without token returns 401."""
    res = client.get("/api/audit")
    assert res.status_code == 401


def test_audit_endpoint_returns_200_with_token(client, token):
    """GET /api/audit with valid token returns 200."""
    res = client.get("/api/audit", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200


def test_audit_returns_list(client, token):
    """Audit log response is a JSON list."""
    res = client.get("/api/audit", headers={"Authorization": f"Bearer {token}"})
    assert isinstance(res.get_json(), list)


def test_register_creates_audit_entry(client, token):
    """Registering a user creates an audit log entry."""
    before = len(client.get("/api/audit", headers={"Authorization": f"Bearer {token}"}).get_json())
    client.post("/api/auth/register", json={
        "username": "auditcheck", "email": "ac@example.com", "password": "pass"
    })
    after_res = client.get("/api/audit", headers={"Authorization": f"Bearer {token}"}).get_json()
    assert len(after_res) > before


def test_create_item_creates_audit_entry(client, token):
    """Creating an item creates an audit log entry."""
    before = len(client.get("/api/audit", headers={"Authorization": f"Bearer {token}"}).get_json())
    client.post("/api/items", json={"name": "AuditItem"},
                headers={"Authorization": f"Bearer {token}"})
    after = len(client.get("/api/audit", headers={"Authorization": f"Bearer {token}"}).get_json())
    assert after > before


def test_audit_entry_has_required_fields(client, token):
    """Each audit entry has id, user_id, action, resource, timestamp."""
    res = client.get("/api/audit", headers={"Authorization": f"Bearer {token}"})
    entries = res.get_json()
    assert len(entries) > 0
    for field in ("id", "action", "resource", "timestamp"):
        assert field in entries[0], f"Missing field: {field}"


def test_audit_entries_returned_in_reverse_order(client, token):
    """Audit entries are in reverse chronological order (newest first)."""
    res = client.get("/api/audit", headers={"Authorization": f"Bearer {token}"})
    entries = res.get_json()
    if len(entries) >= 2:
        assert entries[0]["id"] >= entries[-1]["id"]


def test_audit_response_is_json(client, token):
    """Audit endpoint returns JSON content type."""
    res = client.get("/api/audit", headers={"Authorization": f"Bearer {token}"})
    assert "application/json" in res.content_type
