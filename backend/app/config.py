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

# Normalise a bare Postgres URL (e.g. Supabase/Neon) to a form SQLAlchemy
# can use with psycopg2. Also drops Supabase's "pgbouncer=true" marker,
# which is only meant for their connection pooler and confuses the driver.
def _normalize_database_url(url):
    if url.startswith("postgres://"):
        url = "postgresql+psycopg2://" + url[len("postgres://"):]
    elif url.startswith("postgresql://"):
        url = "postgresql+psycopg2://" + url[len("postgresql://"):]
    if "pgbouncer" in url:
        url = url.replace("?pgbouncer=true", "").replace("&pgbouncer=true", "")
    return url

_DEFAULT_CORS_ORIGINS = "http://localhost:5173,http://127.0.0.1:5173,http://localhost:5174,http://127.0.0.1:5174"


class Config:
    """Base application configuration (read from environment variables)."""

    TESTING = False
    DEBUG = os.environ.get("FLASK_DEBUG", "1") == "1"

    # Used to sign login tokens. Override in production via SECRET_KEY env var.
    SECRET_KEY = os.environ.get("SECRET_KEY", "mini-trello-dev-secret-change-me")

    DATABASE_URL = _normalize_database_url(_DEFAULT_DATABASE_URL)
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JSON_SORT_KEYS = False

    CORS_ORIGINS = [
        origin.strip() for origin in os.environ.get("CORS_ORIGINS", _DEFAULT_CORS_ORIGINS).split(",")
    ]