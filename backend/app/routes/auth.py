from flask import Blueprint, g, jsonify, request

from app.models import User, db
from app.security import create_token, require_auth

auth_bp = Blueprint("auth", __name__)


def cleaned_text(value):
    if not isinstance(value, str):
        return None
    value = value.strip()
    return value if value else None


@auth_bp.post("/register")
def register():
    """POST /api/auth/register -> create an account, return a token."""
    data = request.get_json(silent=True)
    if data is None or not isinstance(data, dict):
        return jsonify({"error": "Request body must be valid JSON"}), 400

    username = cleaned_text(data.get("username"))
    password = data.get("password")

    if not username:
        return jsonify({"error": "Username is required"}), 400
    if len(username) > 50:
        return jsonify({"error": "Username must be 50 characters or fewer"}), 400
    if not isinstance(password, str) or len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters"}), 400

    exists = db.session.query(User.id).filter_by(username=username).first()
    if exists is not None:
        return jsonify({"error": "That username is already taken"}), 409

    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return (
        jsonify(
            {
                "token": create_token(user.id),
                "user": user.to_dict(),
            }
        ),
        201,
    )


@auth_bp.post("/login")
def login():
    """POST /api/auth/login -> verify credentials, return a token."""
    data = request.get_json(silent=True)
    if data is None or not isinstance(data, dict):
        return jsonify({"error": "Request body must be valid JSON"}), 400

    username = cleaned_text(data.get("username"))
    password = data.get("password")

    if not username or not isinstance(password, str) or not password:
        return jsonify({"error": "Username and password are required"}), 400

    user = User.query.filter_by(username=username).first()
    if user is None or not user.check_password(password):
        return jsonify({"error": "Invalid username or password"}), 401

    return jsonify({"token": create_token(user.id), "user": user.to_dict()})


@auth_bp.get("/me")
@require_auth
def me():
    """GET /api/auth/me -> details about the logged-in user."""
    return jsonify({"user": g.current_user.to_dict()})