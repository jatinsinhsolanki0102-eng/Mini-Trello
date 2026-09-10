"""Vercel serverless entry point for the Mini-Trello Flask backend.

Vercel runs this file as a WSGI app. The `create_app()` factory is applied
on import so route definitions, CORS and database initialisation are shared
with local development (backend/run.py).
"""
import os
import sys

# Make the Flask application package importable:
#   /api/index.py  ->  ../backend/app
_BACKEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "backend")
if _BACKEND_DIR not in sys.path:
    sys.path.insert(0, _BACKEND_DIR)

from app import create_app  # noqa: E402

app = create_app()