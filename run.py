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
    parser.add_argument("--no-browser", action="store_true", help="Do not automatically open the browser")
    args = parser.parse_args()

    app = create_app()
    app.config["PORT"] = args.port
    app.config["HOST"] = args.host

    profiles = list_profiles()
    profiles_count = len(profiles)

    url = f"http://{args.host}:{args.port}"

    print("==================================================================")
    print("  🔥 OpsForge — DevOps Learning & Practice Dashboard")
    print("==================================================================")
    print(f"  • Status:       Running locally (offline)")
    print(f"  • Address:      {url}")
    print(f"  • Profiles:     {profiles_count} local profile(s) found in user_data/")
    print(f"  • Press Ctrl+C to stop the server")
    print("==================================================================\n")

    if not args.no_browser:
        threading.Thread(target=open_browser, args=(url,), daemon=True).start()

    try:
        app.run(host=args.host, port=args.port, debug=True)
    except KeyboardInterrupt:
        print("\n👋 OpsForge stopped gracefully. See you soon!")

if __name__ == "__main__":
    main()
