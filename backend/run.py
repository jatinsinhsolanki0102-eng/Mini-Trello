import os

from dotenv import load_dotenv

from app import create_app

# Load environment variables from .env (if present) so that DATABASE_URL,
# CORS_ORIGINS etc. can be configured without hardcoding secrets.
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", 5000)), debug=True)