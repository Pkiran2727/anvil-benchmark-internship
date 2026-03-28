"""Task 7 Tests — Search on GET /api/items."""
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
        "SECRET_KEY": "test-secret-t7",
    })
    with app.app_context():
        db.create_all()
        c = app.test_client()
        # Register + login to create items
        c.post("/api/auth/register", json={"username": "t7u", "email": "t7@e.com", "password": "pass"})
        res = c.post("/api/auth/login", json={"username": "t7u", "password": "pass"})
        tok = res.get_json()["token"]
        headers = {"Authorization": f"Bearer {tok}"}
        c.post("/api/items", json={"name": "Python Tutorial"}, headers=headers)
        c.post("/api/items", json={"name": "Flask Guide"}, headers=headers)
        c.post("/api/items", json={"name": "python basics"}, headers=headers)
        c.post("/api/items", json={"name": "Advanced SQL"}, headers=headers)
        yield c


def test_items_no_query_returns_all(client):
    """GET /api/items with no query returns all items."""
    res = client.get("/api/items")
    assert res.status_code == 200
    assert len(res.get_json()) == 4


def test_items_search_returns_200(client):
    """GET /api/items?q=python returns 200."""
    res = client.get("/api/items?q=python")
    assert res.status_code == 200


def test_items_search_filters_by_name(client):
    """?q=python returns only items with 'python' in name."""
    res = client.get("/api/items?q=python")
    items = res.get_json()
    assert len(items) == 2


def test_items_search_is_case_insensitive(client):
    """Search is case-insensitive: ?q=PYTHON matches 'python basics'."""
    res = client.get("/api/items?q=PYTHON")
    items = res.get_json()
    assert len(items) == 2


def test_items_search_partial_match(client):
    """Partial match: ?q=flask returns 'Flask Guide'."""
    res = client.get("/api/items?q=flask")
    items = res.get_json()
    assert len(items) == 1
    assert items[0]["name"] == "Flask Guide"


def test_items_search_no_match_returns_empty(client):
    """?q=nonexistent returns empty list."""
    res = client.get("/api/items?q=nonexistent123")
    assert res.get_json() == []


def test_items_search_empty_q_returns_all(client):
    """?q= (empty) returns all items."""
    res = client.get("/api/items?q=")
    assert len(res.get_json()) == 4


def test_items_response_is_list(client):
    """Response is always a JSON list."""
    res = client.get("/api/items?q=sql")
    assert isinstance(res.get_json(), list)
