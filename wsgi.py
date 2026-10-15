#!/usr/bin/env python3
"""WSGI entry point for OpsForge production server."""
import os
from app import create_app

# Disable debug in production
app = create_app()
app.config["DEBUG"] = False

if __name__ == "__main__":
    # If run directly as python wsgi.py, use waitress or gunicorn
    port = int(os.environ.get("PORT", 5000))
    host = os.environ.get("HOST", "127.0.0.1")
    try:
        from waitress import serve
        print(f"🔥 OpsForge production server running via Waitress at http://{host}:{port}")
        serve(app, host=host, port=port, threads=4)
    except ImportError:
        app.run(host=host, port=port, debug=False)
