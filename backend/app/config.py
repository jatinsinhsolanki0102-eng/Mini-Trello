import os

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# Default database URL.
# For local development SQLite is used so the project runs with zero setup.
# To use MySQL, set DATABASE_URL like:
#   mysql+pymysql://root:your_password@localhost:3306/mini_trello
_DEFAULT_DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "sqlite:///" + os.path.join(BASE_DIR, "mini_trello.db"),
)

# Normalise a bare Postgres URL (e.g. Neon's "postgresql://..." or
# "postgres://...") to a form SQLAlchemy can use with psycopg2.
def _normalize_database_url(url):
    if url.startswith("postgres://"):
        return "postgresql+psycopg2://" + url[len("postgres://"):]
    if url.startswith("postgresql://"):
        return "postgresql+psycopg2://" + url[len("postgresql://"):]
    return url

_DEFAULT_CORS_ORIGINS = "http://localhost:5173,http://127.0.0.1:5173,http://localhost:5174,http://127.0.0.1:5174"


class Config:
    """Base application configuration (read from environment variables)."""

    TESTING = False
    DEBUG = os.environ.get("FLASK_DEBUG", "1") == "1"

    DATABASE_URL = _normalize_database_url(_DEFAULT_DATABASE_URL)
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JSON_SORT_KEYS = False

    CORS_ORIGINS = [
        origin.strip() for origin in os.environ.get("CORS_ORIGINS", _DEFAULT_CORS_ORIGINS).split(",")
    ]