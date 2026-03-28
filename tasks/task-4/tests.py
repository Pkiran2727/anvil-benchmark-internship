"""Task 4 Tests — GET /api/users with pagination."""
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
        "SECRET_KEY": "test-secret-t4",
    })
    with app.app_context():
        db.create_all()
        c = app.test_client()
        # Seed 15 users
        for i in range(1, 16):
            c.post("/api/auth/register", json={
                "username": f"user{i:03d}", "email": f"u{i}@example.com", "password": "pass"
            })
        yield c


def test_users_endpoint_returns_200(client):
    """GET /api/users returns 200."""
    res = client.get("/api/users")
    assert res.status_code == 200


def test_users_response_has_required_keys(client):
    """Response includes users, total, pages, current_page."""
    res = client.get("/api/users")
    data = res.get_json()
    for key in ("users", "total", "pages", "current_page"):
        assert key in data, f"Missing key: {key}"


def test_users_is_list(client):
    """users field is a list."""
    res = client.get("/api/users")
    assert isinstance(res.get_json()["users"], list)


def test_users_default_per_page_is_10(client):
    """Default pagination returns at most 10 users."""
    res = client.get("/api/users")
    assert len(res.get_json()["users"]) <= 10


def test_users_total_count_correct(client):
    """total reflects all seeded users."""
    res = client.get("/api/users")
    assert res.get_json()["total"] == 15


def test_users_per_page_param_respected(client):
    """?per_page=5 returns 5 users."""
    res = client.get("/api/users?per_page=5")
    assert len(res.get_json()["users"]) == 5


def test_users_page_2_different_from_page_1(client):
    """Page 2 returns different users than page 1."""
    r1 = client.get("/api/users?page=1&per_page=5").get_json()["users"]
    r2 = client.get("/api/users?page=2&per_page=5").get_json()["users"]
    ids1 = {u["id"] for u in r1}
    ids2 = {u["id"] for u in r2}
    assert ids1.isdisjoint(ids2), "Pages should not overlap"


def test_users_current_page_field_matches_param(client):
    """current_page in response matches requested page."""
    res = client.get("/api/users?page=2&per_page=5")
    assert res.get_json()["current_page"] == 2
