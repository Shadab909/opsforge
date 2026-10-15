from flask import Blueprint, render_template, session, redirect, url_for, abort, jsonify
from app.routes.auth import login_required
from app.content_loader import get_topic, get_modules, get_module, get_chunk
from app.database import get_module_progress, get_chunk_progress, mark_chunk_read

modules_bp = Blueprint("modules", __name__)

@modules_bp.route("/<topic_slug>/")
@login_required
def topic_view(topic_slug):
    topic = get_topic(topic_slug)
    if not topic:
        abort(404)

    username = session.get("username")
    modules_list = get_modules(topic_slug)
    
    enhanced_modules = []
    total_mods = len(modules_list)
    completed_mods = 0

    for m in modules_list:
        chunks = m.get("chunks", [])
        prog = get_module_progress(username, topic_slug, m["slug"], chunks)
        if prog["status"] == "Completed":
            completed_mods += 1
        enhanced_modules.append({
            "meta": m,
            "progress": prog
        })

    overall_percentage = round((completed_mods / total_mods) * 100) if total_mods > 0 else 0

    return render_template(
        "topic.html",
        topic=topic,
        modules=enhanced_modules,
        overall_percentage=overall_percentage
    )

@modules_bp.route("/<topic_slug>/<module_slug>/")
@login_required
def module_view(topic_slug, module_slug):
    topic = get_topic(topic_slug)
    module = get_module(topic_slug, module_slug)
    if not topic or not module:
        abort(404)

    username = session.get("username")
    chunks = module.get("chunks", [])
    module_prog = get_module_progress(username, topic_slug, module_slug, chunks)
    
    # Enrich chunks with individual progress
    enhanced_chunks = []
    for idx, ch in enumerate(chunks, start=1):
        c_prog = get_chunk_progress(username, topic_slug, module_slug, ch["slug"])
        enhanced_chunks.append({
            "index": idx,
            "slug": ch["slug"],
            "title": ch["title"],
            "estimated_time": ch.get("estimated_time", 5),
            "has_hands_on": ch.get("has_hands_on", False),
            "progress": c_prog
        })

    return render_template(
        "module.html",
        topic=topic,
        module=module,
        chunks=enhanced_chunks,
        module_prog=module_prog
    )

@modules_bp.route("/<topic_slug>/<module_slug>/<chunk_slug>/")
@login_required
def chunk_view(topic_slug, module_slug, chunk_slug):
    topic = get_topic(topic_slug)
    module = get_module(topic_slug, module_slug)
    chunk = get_chunk(topic_slug, module_slug, chunk_slug)
    
    if not topic or not module or not chunk:
        abort(404)

    username = session.get("username")
    progress = get_chunk_progress(username, topic_slug, module_slug, chunk_slug)

    # Calculate prev and next chunk
    chunks = module.get("chunks", [])
    prev_chunk = None
    next_chunk = None
    
    for i, ch in enumerate(chunks):
        if ch["slug"] == chunk_slug:
            if i > 0:
                prev_chunk = chunks[i - 1]
            if i < len(chunks) - 1:
                next_chunk = chunks[i + 1]
            break

    return render_template(
        "chunk.html",
        topic=topic,
        module=module,
        chunk=chunk,
        progress=progress,
        prev_chunk=prev_chunk,
        next_chunk=next_chunk
    )

@modules_bp.route("/<topic_slug>/<module_slug>/<chunk_slug>/mark-read", methods=["POST"])
@login_required
def mark_read(topic_slug, module_slug, chunk_slug):
    username = session.get("username")
    mark_chunk_read(username, topic_slug, module_slug, chunk_slug)
    return jsonify({"success": True, "status": "read"})
