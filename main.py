# main.py
"""
Root ASGI entry point for InternGuide API.
Re-exports `app` from `app.main` for hosting environments (like Render or Docker)
that default to `uvicorn main:app`.
"""

from app.main import app

__all__ = ["app"]
