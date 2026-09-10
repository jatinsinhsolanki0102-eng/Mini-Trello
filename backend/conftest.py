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