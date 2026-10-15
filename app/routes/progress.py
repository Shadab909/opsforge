from flask import Blueprint, jsonify, session
from app.routes.auth import login_required
from app.content_loader import get_modules, get_module
from app.database import get_module_progress

progress_bp = Blueprint("progress", __name__, url_prefix="/api/progress")

@progress_bp.route("/<topic_slug>/<module_slug>")
@login_required
def module_progress_api(topic_slug, module_slug):
    username = session.get("username")
    mod = get_module(topic_slug, module_slug)
    if not mod:
        return jsonify({"error": "Module not found"}), 404
        
    chunks = mod.get("chunks", [])
    prog = get_module_progress(username, topic_slug, module_slug, chunks)
    return jsonify(prog)
