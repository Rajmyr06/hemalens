from fastapi.testclient import TestClient

from app.main import app


def test_research_page_is_available() -> None:
    with TestClient(app) as client:
        response = client.get("/research")

    assert response.status_code == 200
    assert "Research transparency" in response.text


def test_about_page_is_available() -> None:
    with TestClient(app) as client:
        response = client.get("/about")

    assert response.status_code == 200
    assert "About HemaLens" in response.text


def test_landing_navigation_uses_page_routes() -> None:
    with TestClient(app) as client:
        response = client.get("/")

    assert response.status_code == 200
    assert 'href="/research"' in response.text
    assert 'href="/about"' in response.text
