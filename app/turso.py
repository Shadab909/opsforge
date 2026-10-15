import os
import json
import logging
import urllib.request
import urllib.error
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional
from app.config import Config

logger = logging.getLogger("opsforge.turso")

ENV_FILE = Config.BASE_DIR / ".env"

def load_dotenv():
    """Simple parser to load .env into os.environ without external dependencies."""
    if not ENV_FILE.exists():
        return
    try:
        with open(ENV_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                k = k.strip()
                v = v.strip().strip("'\"")
                if k and k not in os.environ:
                    os.environ[k] = v
    except Exception as e:
        logger.warning(f"Failed to read .env file: {e}")

# Load .env on import
load_dotenv()

def get_turso_credentials() -> Tuple[str, str]:
    """Returns (db_url, auth_token) from environment or .env"""
    db_url = os.environ.get("TURSO_DATABASE_URL", "").strip()
    auth_token = os.environ.get("TURSO_AUTH_TOKEN", "").strip()
    return db_url, auth_token

def is_turso_enabled() -> bool:
    """Checks if Turso credentials are configured."""
    url, token = get_turso_credentials()
    return bool(url and token)

def save_turso_credentials(db_url: str, auth_token: str):
    """Saves Turso credentials to .env file and sets them in current process."""
    clean_url = db_url.strip()
    clean_token = auth_token.strip()
    
    os.environ["TURSO_DATABASE_URL"] = clean_url
    os.environ["TURSO_AUTH_TOKEN"] = clean_token
    
    # Read existing .env lines
    lines = []
    if ENV_FILE.exists():
        with open(ENV_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
    new_lines = []
    has_url = False
    has_token = False
    
    for line in lines:
        if line.strip().startswith("TURSO_DATABASE_URL="):
            new_lines.append(f'TURSO_DATABASE_URL="{clean_url}"\n')
            has_url = True
        elif line.strip().startswith("TURSO_AUTH_TOKEN="):
            new_lines.append(f'TURSO_AUTH_TOKEN="{clean_token}"\n')
            has_token = True
        else:
            new_lines.append(line)
            
    if not has_url:
        new_lines.append(f'TURSO_DATABASE_URL="{clean_url}"\n')
    if not has_token:
        new_lines.append(f'TURSO_AUTH_TOKEN="{clean_token}"\n')
        
    with open(ENV_FILE, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

def clear_turso_credentials():
    """Removes Turso credentials from .env and os.environ."""
    os.environ.pop("TURSO_DATABASE_URL", None)
    os.environ.pop("TURSO_AUTH_TOKEN", None)
    
    if not ENV_FILE.exists():
        return
        
    with open(ENV_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    new_lines = [
        line for line in lines 
        if not line.strip().startswith("TURSO_DATABASE_URL=") 
        and not line.strip().startswith("TURSO_AUTH_TOKEN=")
    ]
    
    with open(ENV_FILE, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

def format_turso_arg(val: Any) -> Dict[str, Any]:
    """Converts a Python value into a Hrana/Turso typed argument."""
    if val is None:
        return {"type": "null"}
    elif isinstance(val, bool):
        return {"type": "integer", "value": "1" if val else "0"}
    elif isinstance(val, int):
        return {"type": "integer", "value": str(val)}
    elif isinstance(val, float):
        return {"type": "float", "value": val}
    else:
        return {"type": "text", "value": str(val)}

def parse_turso_row(cols: List[str], row: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Parses a Turso typed row into a standard Python dict."""
    row_dict = {}
    for col_name, val_obj in zip(cols, row):
        v_type = val_obj.get("type")
        v_val = val_obj.get("value")
        if v_type == "null":
            row_dict[col_name] = None
        elif v_type == "integer":
            row_dict[col_name] = int(v_val)
        elif v_type == "float":
            row_dict[col_name] = float(v_val)
        else:
            row_dict[col_name] = v_val
    return row_dict

def execute_turso_pipeline(statements: List[Any], db_url: str = None, auth_token: str = None) -> List[Dict[str, Any]]:
    """
    Executes a list of SQL statements against Turso HTTP API (/v2/pipeline).
    Each statement can be either:
    - a raw SQL string: "SELECT 1"
    - a dict: {"sql": "SELECT * FROM users WHERE id = ?", "args": [42]}
    """
    url, token = get_turso_credentials()
    db_url = (db_url or url).strip()
    auth_token = (auth_token or token).strip()

    if not db_url or not auth_token:
        raise ValueError("Turso database URL and auth token must be configured.")

    # Convert libsql:// to https://
    http_url = db_url.replace("libsql://", "https://")
    if not http_url.startswith("http://") and not http_url.startswith("https://"):
        http_url = "https://" + http_url
    if not http_url.endswith("/v2/pipeline"):
        http_url = http_url.rstrip("/") + "/v2/pipeline"

    requests_payload = []
    for stmt in statements:
        if isinstance(stmt, str):
            requests_payload.append({
                "type": "execute",
                "stmt": {"sql": stmt}
            })
        elif isinstance(stmt, dict):
            sql = stmt.get("sql", "")
            args = [format_turso_arg(a) for a in stmt.get("args", [])]
            requests_payload.append({
                "type": "execute",
                "stmt": {
                    "sql": sql,
                    "args": args
                }
            })
        elif isinstance(stmt, tuple):
            # (sql, args_list)
            sql, args_raw = stmt
            args = [format_turso_arg(a) for a in args_raw]
            requests_payload.append({
                "type": "execute",
                "stmt": {
                    "sql": sql,
                    "args": args
                }
            })

    requests_payload.append({"type": "close"})

    data = json.dumps({"requests": requests_payload}).encode("utf-8")
    req = urllib.request.Request(
        http_url,
        data=data,
        headers={
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application/json"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=12) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            results = []
            for item in res_data.get("results", []):
                if item.get("type") == "ok":
                    resp = item.get("response", {})
                    if resp.get("type") == "execute":
                        exec_res = resp.get("result", {})
                        cols = [c["name"] for c in exec_res.get("cols", [])]
                        parsed_rows = [parse_turso_row(cols, r) for r in exec_res.get("rows", [])]
                        results.append({
                            "columns": cols,
                            "rows": parsed_rows,
                            "affected_rows": exec_res.get("affected_row_count", 0),
                            "last_insert_rowid": exec_res.get("last_insert_rowid")
                        })
                elif item.get("type") == "error":
                    err_msg = item.get("error", {}).get("message", "Unknown Turso error")
                    raise RuntimeError(f"Turso query error: {err_msg}")
            return results
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"HTTP {e.code}: {error_body or e.reason}")
    except Exception as e:
        raise RuntimeError(f"Connection failed: {str(e)}")

def test_connection(db_url: str = None, auth_token: str = None) -> Tuple[bool, str]:
    """Tests connection to Turso by executing SELECT 1."""
    try:
        res = execute_turso_pipeline(["SELECT 1 as test_col;"], db_url, auth_token)
        if res and res[0]["rows"] and res[0]["rows"][0].get("test_col") == 1:
            return True, "Successfully connected to Turso database!"
        return True, "Connection established successfully."
    except Exception as e:
        return False, str(e)

def init_turso_schema(db_url: str = None, auth_token: str = None):
    """Creates tables in Turso database if they don't exist."""
    stmts = [
        """
        CREATE TABLE IF NOT EXISTS profiles (
            username TEXT PRIMARY KEY,
            display_name TEXT NOT NULL,
            password_hash TEXT,
            preferences TEXT,
            created_at TEXT,
            last_active TEXT
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS chunk_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            topic_slug TEXT NOT NULL,
            module_slug TEXT NOT NULL,
            chunk_slug TEXT NOT NULL,
            content_read BOOLEAN DEFAULT 0,
            read_at TEXT,
            quiz_passed BOOLEAN DEFAULT 0,
            best_score INTEGER DEFAULT 0,
            attempts INTEGER DEFAULT 0,
            UNIQUE(username, topic_slug, module_slug, chunk_slug)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS quiz_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            topic_slug TEXT NOT NULL,
            module_slug TEXT NOT NULL,
            chunk_slug TEXT NOT NULL,
            score INTEGER NOT NULL,
            total_questions INTEGER NOT NULL,
            correct_count INTEGER NOT NULL,
            answers TEXT,
            attempted_at TEXT DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(username, topic_slug, module_slug, chunk_slug, attempted_at)
        );
        """
    ]
    execute_turso_pipeline(stmts, db_url, auth_token)

def sync_local_to_turso(username: str) -> Dict[str, Any]:
    """Uploads local profile and progress.db records for `username` into Turso."""
    import sqlite3
    from app.config import Config
    
    init_turso_schema()
    
    user_dir = Config.USER_DATA_DIR / username
    if not user_dir.exists():
        return {"status": "error", "message": f"User directory for {username} does not exist."}
        
    p_path = user_dir / "profile.json"
    db_path = user_dir / "progress.db"
    
    stmts = []
    synced_items = {"profile": 0, "progress_rows": 0, "quiz_attempts": 0}
    
    # 1. Sync Profile
    if p_path.exists():
        try:
            with open(p_path, "r", encoding="utf-8") as f:
                p_data = json.load(f)
                stmts.append({
                    "sql": """
                    INSERT INTO profiles (username, display_name, password_hash, preferences, created_at, last_active)
                    VALUES (?, ?, ?, ?, ?, ?)
                    ON CONFLICT(username) DO UPDATE SET
                        display_name = excluded.display_name,
                        password_hash = COALESCE(excluded.password_hash, profiles.password_hash),
                        preferences = excluded.preferences,
                        last_active = excluded.last_active;
                    """,
                    "args": [
                        p_data.get("username", username),
                        p_data.get("display_name", username.capitalize()),
                        p_data.get("password_hash"),
                        json.dumps(p_data.get("preferences", {})),
                        p_data.get("created_at"),
                        p_data.get("last_active")
                    ]
                })
                synced_items["profile"] = 1
        except Exception as e:
            logger.error(f"Error reading profile for sync: {e}")

    # 2. Sync Progress DB
    if db_path.exists():
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        
        # Sync chunk_progress
        cur.execute("SELECT * FROM chunk_progress")
        for row in cur.fetchall():
            stmts.append({
                "sql": """
                INSERT INTO chunk_progress (username, topic_slug, module_slug, chunk_slug, content_read, read_at, quiz_passed, best_score, attempts)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(username, topic_slug, module_slug, chunk_slug) DO UPDATE SET
                    content_read = MAX(chunk_progress.content_read, excluded.content_read),
                    read_at = COALESCE(chunk_progress.read_at, excluded.read_at),
                    quiz_passed = MAX(chunk_progress.quiz_passed, excluded.quiz_passed),
                    best_score = MAX(chunk_progress.best_score, excluded.best_score),
                    attempts = MAX(chunk_progress.attempts, excluded.attempts);
                """,
                "args": [
                    username,
                    row["topic_slug"],
                    row["module_slug"],
                    row["chunk_slug"],
                    row["content_read"],
                    row["read_at"],
                    row["quiz_passed"],
                    row["best_score"],
                    row["attempts"]
                ]
            })
            synced_items["progress_rows"] += 1
            
        # Sync quiz attempts
        cur.execute("SELECT * FROM quiz_attempts")
        for row in cur.fetchall():
            stmts.append({
                "sql": """
                INSERT INTO quiz_attempts (username, topic_slug, module_slug, chunk_slug, score, total_questions, correct_count, answers, attempted_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(username, topic_slug, module_slug, chunk_slug, attempted_at) DO NOTHING;
                """,
                "args": [
                    username,
                    row["topic_slug"],
                    row["module_slug"],
                    row["chunk_slug"],
                    row["score"],
                    row["total_questions"],
                    row["correct_count"],
                    row["answers"],
                    row["attempted_at"]
                ]
            })
            synced_items["quiz_attempts"] += 1
            
        conn.close()
        
    if stmts:
        # Send in batches of 50 to avoid HTTP payload limits
        batch_size = 50
        for i in range(0, len(stmts), batch_size):
            execute_turso_pipeline(stmts[i:i + batch_size])
            
    return {"status": "success", "synced": synced_items}

def sync_turso_to_local(username: str) -> Dict[str, Any]:
    """Downloads profile and progress records for `username` from Turso into local files."""
    import sqlite3
    from app.config import Config
    
    user_dir = Config.USER_DATA_DIR / username
    user_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Fetch profile from Turso
    p_res = execute_turso_pipeline([{
        "sql": "SELECT * FROM profiles WHERE username = ?;",
        "args": [username]
    }])
    if p_res and p_res[0]["rows"]:
        turso_p = p_res[0]["rows"][0]
        pref_raw = turso_p.get("preferences")
        pref = json.loads(pref_raw) if isinstance(pref_raw, str) else (pref_raw or {})
        profile_data = {
            "username": turso_p["username"],
            "display_name": turso_p["display_name"],
            "password_hash": turso_p.get("password_hash"),
            "preferences": pref,
            "created_at": turso_p.get("created_at"),
            "last_active": turso_p.get("last_active")
        }
        with open(user_dir / "profile.json", "w", encoding="utf-8") as f:
            json.dump(profile_data, f, indent=2)

    # 2. Fetch chunk_progress from Turso
    db_path = user_dir / "progress.db"
    conn = sqlite3.connect(db_path)
    # Ensure tables exist locally
    from app.database import init_db_tables
    init_db_tables(conn)
    cur = conn.cursor()

    cp_res = execute_turso_pipeline([{
        "sql": "SELECT * FROM chunk_progress WHERE username = ?;",
        "args": [username]
    }])
    if cp_res and cp_res[0]["rows"]:
        for r in cp_res[0]["rows"]:
            cur.execute("""
                INSERT INTO chunk_progress (topic_slug, module_slug, chunk_slug, content_read, read_at, quiz_passed, best_score, attempts)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(topic_slug, module_slug, chunk_slug) DO UPDATE SET
                    content_read = MAX(chunk_progress.content_read, excluded.content_read),
                    read_at = COALESCE(chunk_progress.read_at, excluded.read_at),
                    quiz_passed = MAX(chunk_progress.quiz_passed, excluded.quiz_passed),
                    best_score = MAX(chunk_progress.best_score, excluded.best_score),
                    attempts = MAX(chunk_progress.attempts, excluded.attempts)
            """, (r["topic_slug"], r["module_slug"], r["chunk_slug"], r["content_read"], r["read_at"], r["quiz_passed"], r["best_score"], r["attempts"]))

    # 3. Fetch quiz_attempts from Turso
    qa_res = execute_turso_pipeline([{
        "sql": "SELECT * FROM quiz_attempts WHERE username = ? ORDER BY attempted_at DESC LIMIT 50;",
        "args": [username]
    }])
    if qa_res and qa_res[0]["rows"]:
        for r in qa_res[0]["rows"]:
            cur.execute("""
                INSERT OR IGNORE INTO quiz_attempts (topic_slug, module_slug, chunk_slug, score, total_questions, correct_count, answers, attempted_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (r["topic_slug"], r["module_slug"], r["chunk_slug"], r["score"], r["total_questions"], r["correct_count"], r["answers"], r["attempted_at"]))

    conn.commit()
    conn.close()
    return {"status": "success"}

