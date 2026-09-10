import pytest

from app import create_app
from app.config import Config
from app.models import db


class TestConfig(Config):
    TESTING = True
    DEBUG = False


def _make_config(db_file):
    class _C(TestConfig):
        DATABASE_URL = f"sqlite:///{db_file.as_posix()}"
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{db_file.as_posix()}"

    return _C


@pytest.fixture()
def app(tmp_path):
    db_file = tmp_path / "test_tasks.db"
    application = create_app(_make_config(db_file))
    with application.app_context():
        db.session.remove()
        db.drop_all()
        db.create_all()
    yield application
    with application.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def token(client):
    """Register a fresh account and return its auth token."""
    response = client.post(
        "/api/auth/register",
        json={"username": "alice", "password": "secret123"},
    )
    assert response.status_code == 201
    return response.get_json()["token"]


@pytest.fixture()
def auth(token):
    """Authorization header for an authenticated test user."""
    return {"Authorization": f"Bearer {token}"}