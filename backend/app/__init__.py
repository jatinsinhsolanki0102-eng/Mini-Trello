from flask import Flask, jsonify
from flask_cors import CORS

from app.config import Config
from app.models import db
from app.routes.auth import auth_bp
from app.routes.tasks import tasks_bp


def create_app(config_object=Config):
    """Application factory. Creates and configures the Flask app."""
    app = Flask(__name__)
    app.config.from_object(config_object)

    CORS(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}})

    db.init_app(app)
    app.register_blueprint(tasks_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    with app.app_context():
        db.create_all()

    @app.get("/")
    def home():
        return jsonify(
            {
                "message": "Mini-Trello API",
                "endpoints": [
                    "/api/auth/register",
                    "/api/auth/login",
                    "/api/auth/me",
                    "/api/tasks",
                ],
            }
        )

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Route not found"}), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({"error": "Internal server error"}), 500

    return app