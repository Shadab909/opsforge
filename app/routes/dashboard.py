from flask import Blueprint, render_template, session, redirect, url_for
from app.routes.auth import login_required
from app.content_loader import get_topics, get_modules
from app.database import get_profile, get_module_progress, get_recent_activity

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/")
@login_required
def index():
    username = session.get("username")
    profile = get_profile(username)
    if not profile:
        return redirect(url_for("auth.select_profile"))

    topics_list = get_topics()
    topics_with_progress = []

    total_modules_all = 0
    completed_modules_all = 0
    quizzes_passed_all = 0

    for t in topics_list:
        mods = get_modules(t["slug"])
        t_total_mods = len(mods)
        t_completed_mods = 0

        for m in mods:
            chunks = m.get("chunks", [])
            m_prog = get_module_progress(username, t["slug"], m["slug"], chunks)
            if m_prog["status"] == "Completed":
                t_completed_mods += 1
            # Count passed chunks
            for ch_slug, ch_data in m_prog.get("chunks_map", {}).items():
                if ch_data.get("quiz_passed"):
                    quizzes_passed_all += 1

        t_percentage = round((t_completed_mods / t_total_mods) * 100) if t_total_mods > 0 else 0
        total_modules_all += t_total_mods
        completed_modules_all += t_completed_mods

        topics_with_progress.append({
            "name": t.get("name", t["slug"]),
            "slug": t["slug"],
            "description": t.get("description", ""),
            "icon": t.get("icon", "📦"),
            "total_modules": t_total_mods,
            "completed_modules": t_completed_mods,
            "percentage": t_percentage
        })

    recent_attempts = get_recent_activity(username, limit=5)

    stats = {
        "total_modules": total_modules_all,
        "completed_modules": completed_modules_all,
        "quizzes_passed": quizzes_passed_all,
        "completion_rate": round((completed_modules_all / total_modules_all) * 100) if total_modules_all > 0 else 0
    }

    return render_template(
        "dashboard.html",
        topics=topics_with_progress,
        recent_activity=recent_attempts,
        stats=stats
    )
