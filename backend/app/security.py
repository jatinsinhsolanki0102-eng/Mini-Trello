"""Token creation/validation and the login-required decorator."""
import datetime

import jwt
from flask import current_app, g, jsonify, request

from app.models import User, db


def _get_secret():
    return current_app.config["SECRET_KEY"]


def create_token(user_id):
    """Create a signed JWT for the given user id (30-day expiry)."""
    payload = {
        "uid": user_id,
        "iat": datetime.datetime.now(datetime.timezone.utc),
        "exp": datetime.datetime.now(datetime.timezone.utc)
        + datetime.timedelta(days=30),
    }
    return jwt.encode(payload, _get_secret(), algorithm="HS256")


def extract_token(request_headers):
    """Pull the raw Bearer token from the Authorization header."""
    auth = request_headers.get("Authorization", "")
    if auth.startswith("Bearer "):
        return auth[len("Bearer "):]
    return None


def authenticate(request_headers):
    """Return the User for a valid token, or None if missing/invalid."""
    token = extract_token(request_headers)
    if not token:
        return None
    try:
        payload = jwt.decode(token, _get_secret(), algorithms=["HS256"])
    except jwt.PyJWTError:
        return None
    return db.session.get(User, payload.get("uid"))


def require_auth(fn):
    """Decorator: resolve the current user and require a valid token."""
    def wrapper(*args, **kwargs):
        user = authenticate(request.headers)
        if user is None:
            return jsonify({"error": "Authentication required"}), 401
        g.current_user = user
        return fn(*args, **kwargs)
    wrapper.__name__ = fn.__name__
    return wrapper