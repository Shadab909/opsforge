#!/usr/bin/env python3
"""
🔥 OpsForge — DevOps Learning & Practice Dashboard
Run this script from terminal:
    python run.py
"""

import sys
import time
import argparse
import threading
import webbrowser
from app import create_app
from app.config import Config
from app.database import list_profiles

def open_browser(url):
    """Wait for server to start, then launch browser."""
    time.sleep(1.2)
    try:
        webbrowser.open(url)
    except Exception:
        pass

def main():
    parser = argparse.ArgumentParser(description="OpsForge — DevOps Learning Dashboard")
    parser.add_argument("--port", type=int, default=5000, help="Port to run server on (default: 5000)")
    parser.add_argument("--host", default="127.0.0.1", help="Host interface (default: 127.0.0.1)")
    parser.add_argument("--dev", action="store_true", help="Run with Flask development server (debug enabled)")
    parser.add_argument("--prod", action="store_true", help="Force production WSGI mode (Waitress/Gunicorn)")
    parser.add_argument("--threads", type=int, default=4, help="Number of threads for production server (default: 4)")
    parser.add_argument("--no-browser", action="store_true", help="Do not automatically open the browser")
    args = parser.parse_args()

    # Determine mode: prod by default unless --dev is explicitly passed
    is_prod = args.prod or (not args.dev and os.environ.get("FLASK_ENV") != "development")

    app = create_app()
    app.config["PORT"] = args.port
    app.config["HOST"] = args.host
    app.config["DEBUG"] = not is_prod

    profiles = list_profiles()
    profiles_count = len(profiles)

    url = f"http://{args.host}:{args.port}"

    from app.turso import is_turso_enabled, get_turso_credentials
    turso_status = "🟢 Turso Cloud Sync (Active)" if is_turso_enabled() else "⚪ Local SQLite Mode"

    print("==================================================================")
    print("  🔥 OpsForge — DevOps Learning & Practice Dashboard")
    print("==================================================================")
    print(f"  • Mode:         {'Production (Waitress WSGI)' if is_prod else 'Development (Flask Debug)'}")
    print(f"  • Address:      {url}")
    print(f"  • Sync:         {turso_status}")
    print(f"  • Profiles:     {profiles_count} profile(s) found in user_data/")
    print(f"  • Press Ctrl+C to stop the server")
    print("==================================================================\n")

    if not args.no_browser and not os.environ.get("OPSFORGE_NO_BROWSER"):
        threading.Thread(target=open_browser, args=(url,), daemon=True).start()

    try:
        if is_prod:
            try:
                from waitress import serve
                serve(app, host=args.host, port=args.port, threads=args.threads)
            except ImportError:
                print("⚠️ Waitress not found, falling back to standard server.")
                app.run(host=args.host, port=args.port, debug=False)
        else:
            app.run(host=args.host, port=args.port, debug=True)
    except KeyboardInterrupt:
        print("\n👋 OpsForge stopped gracefully. See you soon!")

if __name__ == "__main__":
    main()

