import os
import json
import sqlite3
import logging
from datetime import datetime
from pathlib import Path
from werkzeug.security import generate_password_hash, check_password_hash
from app.config import Config
from app.turso import is_turso_enabled, execute_turso_pipeline, init_turso_schema

logger = logging.getLogger("opsforge.database")

def get_user_dir(username: str) -> Path:
    user_dir = Config.USER_DATA_DIR / username
    user_dir.mkdir(parents=True, exist_ok=True)
    return user_dir

def get_db_path(username: str) -> Path:
    return get_user_dir(username) / "progress.db"

def get_profile_path(username: str) -> Path:
    return get_user_dir(username) / "profile.json"

def get_db(username: str) -> sqlite3.Connection:
    db_path = get_db_path(username)
    is_new = not db_path.exists()
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    if is_new:
        init_db_tables(conn)
    return conn

def init_db_tables(conn: sqlite3.Connection):
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chunk_progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic_slug TEXT NOT NULL,
        module_slug TEXT NOT NULL,
        chunk_slug TEXT NOT NULL,
        content_read BOOLEAN DEFAULT 0,
        read_at TEXT,
        quiz_passed BOOLEAN DEFAULT 0,
        best_score INTEGER DEFAULT 0,
        attempts INTEGER DEFAULT 0,
        UNIQUE(topic_slug, module_slug, chunk_slug)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS quiz_attempts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic_slug TEXT NOT NULL,
        module_slug TEXT NOT NULL,
        chunk_slug TEXT NOT NULL,
        score INTEGER NOT NULL,
        total_questions INTEGER NOT NULL,
        correct_count INTEGER NOT NULL,
        answers TEXT,
        attempted_at TEXT DEFAULT CURRENT_TIMESTAMP
    );
    """)
    conn.commit()

def init_user_db(username: str):
    """Initializes tables in user_data/<username>/progress.db and Turso if enabled"""
    conn = get_db(username)
    init_db_tables(conn)
    conn.close()
    if is_turso_enabled():
        try:
            init_turso_schema()
        except Exception as e:
            logger.warning(f"Could not init Turso schema: {e}")

def list_profiles():
    """Lists all available profiles from user_data/ directory, merged with Turso if active"""
    local_profiles = {}
    if Config.USER_DATA_DIR.exists():
        for item in Config.USER_DATA_DIR.iterdir():
            if item.is_dir() and (item / "profile.json").exists():
                try:
                    with open(item / "profile.json", "r", encoding="utf-8") as f:
                        data = json.load(f)
                        local_profiles[data["username"]] = data
                except Exception:
                    pass

    # If Turso is enabled, fetch remote profiles and merge
    if is_turso_enabled():
        try:
            res = execute_turso_pipeline(["SELECT * FROM profiles;"])
            if res and res[0]["rows"]:
                for r in res[0]["rows"]:
                    uname = r["username"]
                    pref_raw = r.get("preferences")
                    pref = json.loads(pref_raw) if isinstance(pref_raw, str) else (pref_raw or {})
                    turso_data = {
                        "username": uname,
                        "display_name": r["display_name"],
                        "password_hash": r.get("password_hash"),
                        "preferences": pref,
                        "created_at": r.get("created_at"),
                        "last_active": r.get("last_active")
                    }
                    # Save or update to local cache
                    u_dir = get_user_dir(uname)
                    with open(u_dir / "profile.json", "w", encoding="utf-8") as f:
                        json.dump(turso_data, f, indent=2)
                    local_profiles[uname] = turso_data
        except Exception as e:
            logger.warning(f"Failed to fetch profiles from Turso: {e}")

    profiles = list(local_profiles.values())
    profiles.sort(key=lambda x: x.get("last_active", ""), reverse=True)
    return profiles

def get_profile(username: str):
    if is_turso_enabled():
        try:
            res = execute_turso_pipeline([{
                "sql": "SELECT * FROM profiles WHERE username = ?;",
                "args": [username]
            }])
            if res and res[0]["rows"]:
                r = res[0]["rows"][0]
                pref_raw = r.get("preferences")
                pref = json.loads(pref_raw) if isinstance(pref_raw, str) else (pref_raw or {})
                profile_data = {
                    "username": r["username"],
                    "display_name": r["display_name"],
                    "password_hash": r.get("password_hash"),
                    "preferences": pref,
                    "created_at": r.get("created_at"),
                    "last_active": r.get("last_active")
                }
                # Update local cache
                u_dir = get_user_dir(username)
                with open(u_dir / "profile.json", "w", encoding="utf-8") as f:
                    json.dump(profile_data, f, indent=2)
                return profile_data
        except Exception as e:
            logger.warning(f"Turso get_profile error: {e}")

    # Fallback to local file
    p_path = get_profile_path(username)
    if p_path.exists():
        try:
            with open(p_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None
    return None

def verify_profile_password(username: str, password: str) -> bool:
    p = get_profile(username)
    if not p:
        return False
    stored_hash = p.get("password_hash")
    if not stored_hash:
        return True
    return check_password_hash(stored_hash, password)

def create_profile(username: str, display_name: str = None, password: str = None, preferences: dict = None):
    clean_username = username.strip().lower().replace(" ", "_")
    user_dir = get_user_dir(clean_username)
    now = datetime.now().isoformat()
    pwd_hash = generate_password_hash(password) if password else None
    prefs = preferences or {"theme": "dark", "passing_score": 70}
    
    profile_data = {
        "username": clean_username,
        "display_name": display_name or clean_username.capitalize(),
        "password_hash": pwd_hash,
        "created_at": now,
        "last_active": now,
        "preferences": prefs
    }
    
    # Save local
    with open(user_dir / "profile.json", "w", encoding="utf-8") as f:
        json.dump(profile_data, f, indent=2)
    init_user_db(clean_username)

    # Save to Turso if enabled
    if is_turso_enabled():
        try:
            execute_turso_pipeline([{
                "sql": """
                INSERT INTO profiles (username, display_name, password_hash, preferences, created_at, last_active)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(username) DO UPDATE SET
                    display_name = excluded.display_name,
                    password_hash = excluded.password_hash,
                    preferences = excluded.preferences,
                    last_active = excluded.last_active;
                """,
                "args": [clean_username, profile_data["display_name"], pwd_hash, json.dumps(prefs), now, now]
            }])
        except Exception as e:
            logger.error(f"Failed to create profile in Turso: {e}")

    return profile_data

def update_profile(username: str, display_name: str = None, new_password: str = None, current_password: str = None) -> tuple:
    p = get_profile(username)
    if not p:
        return False, "Profile not found."

    stored_hash = p.get("password_hash")
    if stored_hash:
        if not current_password or not check_password_hash(stored_hash, current_password):
            return False, "Current password is incorrect."

    if display_name and display_name.strip():
        p["display_name"] = display_name.strip()

    if new_password and new_password.strip():
        p["password_hash"] = generate_password_hash(new_password.strip())

    now = datetime.now().isoformat()
    p["last_active"] = now

    # Save local
    with open(get_profile_path(username), "w", encoding="utf-8") as f:
        json.dump(p, f, indent=2)

    # Update Turso if enabled
    if is_turso_enabled():
        try:
            execute_turso_pipeline([{
                "sql": """
                UPDATE profiles 
                SET display_name = ?, password_hash = ?, last_active = ?
                WHERE username = ?;
                """,
                "args": [p["display_name"], p.get("password_hash"), now, username]
            }])
        except Exception as e:
            logger.error(f"Failed to update profile in Turso: {e}")

    return True, "Profile updated successfully!"

def update_last_active(username: str):
    p = get_profile(username)
    now = datetime.now().isoformat()
    if p:
        p["last_active"] = now
        with open(get_profile_path(username), "w", encoding="utf-8") as f:
            json.dump(p, f, indent=2)
            
    if is_turso_enabled():
        try:
            execute_turso_pipeline([{
                "sql": "UPDATE profiles SET last_active = ? WHERE username = ?;",
                "args": [now, username]
            }])
        except Exception as e:
            logger.debug(f"Turso update_last_active error: {e}")

def get_chunk_progress(username: str, topic_slug: str, module_slug: str, chunk_slug: str):
    if is_turso_enabled():
        try:
            res = execute_turso_pipeline([{
                "sql": """
                SELECT topic_slug, module_slug, chunk_slug, content_read, read_at, quiz_passed, best_score, attempts
                FROM chunk_progress 
                WHERE username = ? AND topic_slug = ? AND module_slug = ? AND chunk_slug = ?;
                """,
                "args": [username, topic_slug, module_slug, chunk_slug]
            }])
            if res and res[0]["rows"]:
                return res[0]["rows"][0]
        except Exception as e:
            logger.warning(f"Turso get_chunk_progress error: {e}")

    # Local fallback
    conn = get_db(username)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM chunk_progress 
        WHERE topic_slug = ? AND module_slug = ? AND chunk_slug = ?
    """, (topic_slug, module_slug, chunk_slug))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return {
        "topic_slug": topic_slug,
        "module_slug": module_slug,
        "chunk_slug": chunk_slug,
        "content_read": 0,
        "read_at": None,
        "quiz_passed": 0,
        "best_score": 0,
        "attempts": 0
    }

def mark_chunk_read(username: str, topic_slug: str, module_slug: str, chunk_slug: str):
    now = datetime.now().isoformat()

    # Always update local
    conn = get_db(username)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO chunk_progress (topic_slug, module_slug, chunk_slug, content_read, read_at)
        VALUES (?, ?, ?, 1, ?)
        ON CONFLICT(topic_slug, module_slug, chunk_slug) DO UPDATE SET
            content_read = 1,
            read_at = COALESCE(read_at, excluded.read_at)
    """, (topic_slug, module_slug, chunk_slug, now))
    conn.commit()
    conn.close()

    # Update Turso if active
    if is_turso_enabled():
        try:
            execute_turso_pipeline([{
                "sql": """
                INSERT INTO chunk_progress (username, topic_slug, module_slug, chunk_slug, content_read, read_at)
                VALUES (?, ?, ?, ?, 1, ?)
                ON CONFLICT(username, topic_slug, module_slug, chunk_slug) DO UPDATE SET
                    content_read = 1,
                    read_at = COALESCE(chunk_progress.read_at, excluded.read_at);
                """,
                "args": [username, topic_slug, module_slug, chunk_slug, now]
            }])
        except Exception as e:
            logger.error(f"Turso mark_chunk_read error: {e}")

    return True

def save_quiz_attempt(username: str, topic_slug: str, module_slug: str, chunk_slug: str,
                      score: int, total_questions: int, correct_count: int,
                      answers: dict, passing_score: int = 70):
    now = datetime.now().isoformat()
    passed = 1 if score >= passing_score else 0

    # 1. Save local
    conn = get_db(username)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO quiz_attempts (topic_slug, module_slug, chunk_slug, score, total_questions, correct_count, answers, attempted_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (topic_slug, module_slug, chunk_slug, score, total_questions, correct_count, json.dumps(answers), now))

    cursor.execute("""
        INSERT INTO chunk_progress (topic_slug, module_slug, chunk_slug, content_read, read_at, quiz_passed, best_score, attempts)
        VALUES (?, ?, ?, 1, ?, ?, ?, 1)
        ON CONFLICT(topic_slug, module_slug, chunk_slug) DO UPDATE SET
            quiz_passed = MAX(quiz_passed, excluded.quiz_passed),
            best_score = MAX(best_score, excluded.best_score),
            attempts = attempts + 1
    """, (topic_slug, module_slug, chunk_slug, now, passed, score))
    conn.commit()
    conn.close()

    # 2. Save to Turso
    if is_turso_enabled():
        try:
            execute_turso_pipeline([
                {
                    "sql": """
                    INSERT INTO quiz_attempts (username, topic_slug, module_slug, chunk_slug, score, total_questions, correct_count, answers, attempted_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
                    """,
                    "args": [username, topic_slug, module_slug, chunk_slug, score, total_questions, correct_count, json.dumps(answers), now]
                },
                {
                    "sql": """
                    INSERT INTO chunk_progress (username, topic_slug, module_slug, chunk_slug, content_read, read_at, quiz_passed, best_score, attempts)
                    VALUES (?, ?, ?, ?, 1, ?, ?, ?, 1)
                    ON CONFLICT(username, topic_slug, module_slug, chunk_slug) DO UPDATE SET
                        quiz_passed = MAX(chunk_progress.quiz_passed, excluded.quiz_passed),
                        best_score = MAX(chunk_progress.best_score, excluded.best_score),
                        attempts = chunk_progress.attempts + 1;
                    """,
                    "args": [username, topic_slug, module_slug, chunk_slug, now, passed, score]
                }
            ])
        except Exception as e:
            logger.error(f"Turso save_quiz_attempt error: {e}")

    return {"passed": bool(passed), "score": score, "best_score": score}

def get_module_progress(username: str, topic_slug: str, module_slug: str, chunks: list):
    """Calculates overall progress for a module based on its chunks"""
    if not chunks:
        return {"percentage": 0, "status": "Not Started", "completed_count": 0, "total": 0}

    rows = {}
    if is_turso_enabled():
        try:
            res = execute_turso_pipeline([{
                "sql": """
                SELECT chunk_slug, content_read, quiz_passed, best_score 
                FROM chunk_progress 
                WHERE username = ? AND topic_slug = ? AND module_slug = ?;
                """,
                "args": [username, topic_slug, module_slug]
            }])
            if res and res[0]["rows"] is not None:
                rows = {r["chunk_slug"]: r for r in res[0]["rows"]}
        except Exception as e:
            logger.warning(f"Turso get_module_progress error: {e}")

    # Fallback to local if Turso rows empty or disabled
    if not rows:
        conn = get_db(username)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT chunk_slug, content_read, quiz_passed, best_score 
            FROM chunk_progress 
            WHERE topic_slug = ? AND module_slug = ?
        """, (topic_slug, module_slug))
        rows = {r["chunk_slug"]: dict(r) for r in cursor.fetchall()}
        conn.close()

    total = len(chunks)
    completed = 0
    in_progress = 0

    for ch in chunks:
        ch_slug = ch["slug"]
        prog = rows.get(ch_slug, {})
        if prog.get("quiz_passed"):
            completed += 1
        elif prog.get("content_read"):
            in_progress += 1

    percentage = round((completed / total) * 100) if total > 0 else 0
    if completed == total and total > 0:
        status = "Completed"
    elif completed > 0 or in_progress > 0:
        status = "In Progress"
    else:
        status = "Not Started"

    return {
        "percentage": percentage,
        "status": status,
        "completed_count": completed,
        "total": total,
        "chunks_map": rows
    }

def get_recent_activity(username: str, limit: int = 5):
    if is_turso_enabled():
        try:
            res = execute_turso_pipeline([{
                "sql": """
                SELECT topic_slug, module_slug, chunk_slug, score, total_questions, correct_count, attempted_at
                FROM quiz_attempts
                WHERE username = ?
                ORDER BY attempted_at DESC
                LIMIT ?;
                """,
                "args": [username, limit]
            }])
            if res and res[0]["rows"] is not None:
                return res[0]["rows"]
        except Exception as e:
            logger.warning(f"Turso get_recent_activity error: {e}")

    conn = get_db(username)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM quiz_attempts
        ORDER BY attempted_at DESC
        LIMIT ?
    """, (limit,))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

