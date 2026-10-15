from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.database import (
    list_profiles,
    create_profile,
    get_profile,
    update_last_active,
    verify_profile_password,
    update_profile
)

auth_bp = Blueprint("auth", __name__, url_prefix="/profile")

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        username = session.get("username")
        if not username:
            return redirect(url_for("auth.select_profile"))
        profile = get_profile(username)
        if not profile:
            session.pop("username", None)
            flash("Session expired or profile updated. Please sign in.", "info")
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
    password = request.form.get("password", "")
    
    profile = get_profile(username)
    if not profile:
        flash("Profile not found.", "error")
        return redirect(url_for("auth.select_profile"))

    # If profile has a password set, verify it
    if profile.get("password_hash"):
        if not verify_profile_password(username, password):
            flash("Invalid password for profile @" + username + ". Please try again.", "error")
            return redirect(url_for("auth.select_profile"))

    session["username"] = profile["username"]
    update_last_active(profile["username"])
    flash(f"Welcome back, {profile['display_name']}!", "success")
    return redirect(url_for("dashboard.index"))

@auth_bp.route("/create", methods=["POST"])
def new_profile():
    username = request.form.get("username", "").strip().lower().replace(" ", "_")
    display_name = request.form.get("display_name", "").strip() or username.capitalize()
    password = request.form.get("password", "").strip()
    
    if not username:
        flash("Username cannot be empty.", "error")
        return redirect(url_for("auth.select_profile"))

    if not password:
        flash("Password cannot be empty.", "error")
        return redirect(url_for("auth.select_profile"))

    existing = get_profile(username)
    if existing:
        flash("A profile with this username already exists.", "error")
        return redirect(url_for("auth.select_profile"))

    profile = create_profile(username, display_name=display_name, password=password)
    session["username"] = profile["username"]
    flash(f"Profile created! Welcome to OpsForge, {profile['display_name']}.", "success")
    return redirect(url_for("dashboard.index"))

@auth_bp.route("/edit", methods=["GET", "POST"])
@login_required
def edit_profile():
    username = session.get("username")
    profile = get_profile(username)
    if not profile:
        flash("Profile not found.", "error")
        return redirect(url_for("auth.select_profile"))

    if request.method == "POST":
        display_name = request.form.get("display_name", "").strip()
        current_password = request.form.get("current_password", "")
        new_password = request.form.get("new_password", "").strip()

        success, msg = update_profile(
            username=username,
            display_name=display_name,
            new_password=new_password if new_password else None,
            current_password=current_password if (new_password or profile.get("password_hash")) else None
        )

        if success:
            flash(msg, "success")
            return redirect(url_for("dashboard.index"))
        else:
            flash(msg, "error")

    return render_template("profile_edit.html", profile=profile)

@auth_bp.route("/logout")
def logout():
    session.pop("username", None)
    flash("Switched out of profile.", "info")
    return redirect(url_for("auth.select_profile"))
