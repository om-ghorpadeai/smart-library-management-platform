import pytest
from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Enterprise Smart Library" in response.data


def test_health_endpoint(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json["status"] == "UP"


def test_books_endpoint(client):
    response = client.get("/api/books")
    assert response.status_code == 200
    assert len(response.json) == 5


def test_borrow_book(client):
    response = client.post("/api/books/1/borrow")
    assert response.status_code == 200
    assert response.json["book"]["available"] is False


def test_unknown_book(client):
    response = client.post("/api/books/999/borrow")
    assert response.status_code == 404


def test_return_book(client):
    response = client.post("/api/books/1/return")
    assert response.status_code == 200
    assert response.json["book"]["available"] is True
