"""Task 10 Tests — GET /api/health endpoint."""
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
        "SECRET_KEY": "test-secret-t10",
    })
    with app.app_context():
        db.create_all()
        with app.test_client() as c:
            yield c


def test_health_returns_200(client):
    """GET /api/health returns 200."""
    res = client.get("/api/health")
    assert res.status_code == 200


def test_health_no_auth_required(client):
    """GET /api/health does not require a token."""
    res = client.get("/api/health")
    assert res.status_code != 401


def test_health_returns_json(client):
    """GET /api/health returns JSON content type."""
    res = client.get("/api/health")
    assert "application/json" in res.content_type


def test_health_has_status_key(client):
    """Response has 'status' key."""
    res = client.get("/api/health")
    assert "status" in res.get_json()


def test_health_has_database_key(client):
    """Response has 'database' key."""
    res = client.get("/api/health")
    assert "database" in res.get_json()


def test_health_status_is_ok_when_db_connected(client):
    """status is 'ok' when DB is reachable."""
    res = client.get("/api/health")
    assert res.get_json()["status"] == "ok"


def test_health_database_is_ok_when_connected(client):
    """database is 'ok' when DB is reachable."""
    res = client.get("/api/health")
    assert res.get_json()["database"] == "ok"


def test_health_endpoint_is_fast(client):
    """Health endpoint responds without error on multiple calls."""
    for _ in range(5):
        res = client.get("/api/health")
        assert res.status_code == 200
