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

from flask import jsonify
from app.turso import (
    is_turso_enabled,
    get_turso_credentials,
    save_turso_credentials,
    clear_turso_credentials,
    test_connection,
    init_turso_schema,
    sync_local_to_turso,
    sync_turso_to_local
)

@auth_bp.route("/cloud-sync", methods=["GET", "POST"])
def cloud_sync():
    current_url, current_token = get_turso_credentials()
    active = is_turso_enabled()
    username = session.get("username")

    if request.method == "POST":
        db_url = request.form.get("db_url", "").strip()
        auth_token = request.form.get("auth_token", "").strip()

        if not db_url or not auth_token:
            flash("Both Database URL and Auth Token are required.", "error")
            return render_template("cloud_sync.html", db_url=db_url, auth_token=auth_token, is_active=active)

        # Test connection before saving
        success, msg = test_connection(db_url, auth_token)
        if not success:
            flash(f"Connection failed: {msg}", "error")
            return render_template("cloud_sync.html", db_url=db_url, auth_token=auth_token, is_active=active)

        # Save credentials
        save_turso_credentials(db_url, auth_token)
        
        # Initialize tables
        try:
            init_turso_schema(db_url, auth_token)
        except Exception as e:
            flash(f"Connected, but table initialization failed: {e}", "error")
            return redirect(url_for("auth.cloud_sync"))

        # If user is logged in, automatically sync their local data to Turso
        if username:
            try:
                sync_res = sync_local_to_turso(username)
                flash(f"🎉 Connected to Turso! Synced {sync_res['synced']['progress_rows']} progress entries & {sync_res['synced']['quiz_attempts']} quiz attempts to cloud.", "success")
            except Exception as e:
                flash(f"Connected to Turso, but initial sync had an issue: {e}", "warning")
        else:
            flash("🎉 Successfully connected to Turso Cloud Database! Your profiles will sync across devices.", "success")

        return redirect(url_for("auth.cloud_sync"))

    return render_template("cloud_sync.html", db_url=current_url, auth_token=current_token, is_active=active)

@auth_bp.route("/cloud-sync/test", methods=["POST"])
def test_sync_connection():
    data = request.get_json(silent=True) or request.form
    db_url = data.get("db_url")
    auth_token = data.get("auth_token")

    if not db_url or not auth_token:
        curr_url, curr_token = get_turso_credentials()
        db_url = db_url or curr_url
        auth_token = auth_token or curr_token

    if not db_url or not auth_token:
        return jsonify({"success": False, "message": "Missing URL or Token."})

    success, msg = test_connection(db_url, auth_token)
    return jsonify({"success": success, "message": msg})

@auth_bp.route("/cloud-sync/sync-now", methods=["POST"])
def sync_now():
    username = session.get("username")
    if not username:
        return jsonify({"success": False, "message": "You must be logged in to sync personal progress."}), 401

    if not is_turso_enabled():
        return jsonify({"success": False, "message": "Turso is not configured."}), 400

    try:
        res = sync_local_to_turso(username)
        # Also refresh local cache from cloud
        sync_turso_to_local(username)
        return jsonify({"success": True, "message": "Sync completed successfully!", "details": res.get("synced", {})})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@auth_bp.route("/cloud-sync/disconnect", methods=["POST"])
def disconnect_sync():
    clear_turso_credentials()
    flash("Disconnected from Turso. OpsForge is now in local offline mode.", "info")
    return redirect(url_for("auth.cloud_sync"))

