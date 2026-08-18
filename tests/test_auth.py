import pytest
from pathlib import Path

from app import create_app


@pytest.fixture()
def app(tmp_path):
    test_db = tmp_path / "test.db"

    app = create_app({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,
        "SECRET_KEY": "test-secret-key",
        "SESSION_COOKIE_SECURE": False,
        "DATABASE": str(test_db),
    })

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


def test_login_page(client):
    response = client.get("/login")

    assert response.status_code == 200
    assert b"Login" in response.data


def test_register_page(client):
    response = client.get("/register")

    assert response.status_code == 200


def test_dashboard_requires_login(client):
    response = client.get("/dashboard")

    assert response.status_code in (302, 303)
    assert "/login" in response.headers.get("Location", "")


def test_logout_requires_login(client):
    response = client.post("/logout")

    assert response.status_code in (302, 303)
    assert "/login" in response.headers.get("Location", "")


def test_home_page(client):
    response = client.get("/")

    assert response.status_code in (200, 302, 303)
