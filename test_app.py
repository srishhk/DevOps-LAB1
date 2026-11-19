import pytest

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def test_index_returns_message(client):
    res = client.get("/")
    assert res.status_code == 200
    assert "Lab 1" in res.get_json()["message"]


def test_health_is_up(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json()["status"] == "UP"


def test_info_has_version(client):
    data = client.get("/api/info").get_json()
    assert data["app"] == "lab1-flask-app"
    assert "version" in data


def test_add(client):
    assert client.get("/api/add/2/3").get_json()["result"] == 5


def test_unknown_route_is_404(client):
    assert client.get("/does-not-exist").status_code == 404
