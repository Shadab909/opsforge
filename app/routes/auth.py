from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.database import list_profiles, create_profile, get_profile, update_last_active

auth_bp = Blueprint("auth", __name__, url_prefix="/profile")

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("username"):
            return redirect(url_for("auth.select_profile"))
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route("/select")
def select_profile():
    profiles = list_profiles()
    return render_template("profile_select.html", profiles=profiles)

@auth_bp.route("/switch", methods=["POST"])
def switch_profile():
    username = request.form.get("username", "").strip()
    profile = get_profile(username)
    if profile:
        session["username"] = profile["username"]
        update_last_active(profile["username"])
        flash(f"Welcome back, {profile['display_name']}!", "success")
        return redirect(url_for("dashboard.index"))
    flash("Profile not found.", "error")
    return redirect(url_for("auth.select_profile"))

@auth_bp.route("/create", methods=["POST"])
def new_profile():
    username = request.form.get("username", "").strip()
    display_name = request.form.get("display_name", "").strip() or username.capitalize()
    
    if not username:
        flash("Username cannot be empty.", "error")
        return redirect(url_for("auth.select_profile"))

    existing = get_profile(username)
    if existing:
        flash("A profile with this username already exists.", "error")
        return redirect(url_for("auth.select_profile"))

    profile = create_profile(username, display_name)
    session["username"] = profile["username"]
    flash(f"Profile created! Welcome to OpsForge, {profile['display_name']}.", "success")
    return redirect(url_for("dashboard.index"))

@auth_bp.route("/logout")
def logout():
    session.pop("username", None)
    flash("Switched out of profile.", "info")
    return redirect(url_for("auth.select_profile"))
