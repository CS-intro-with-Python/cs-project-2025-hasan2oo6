import sqlite3
import json
from typing import Any, Dict, List, Optional

DB_PATH = "contests.db"

def _conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db() -> None:
    conn = _conn()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS contests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at INTEGER NOT NULL,
        start_time INTEGER,
        duration_minutes INTEGER NOT NULL,
        handles_json TEXT NOT NULL,
        problems_json TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

def create_contest(created_at: int, duration_minutes: int, handles: List[str], problems: List[Dict[str, Any]]) -> int:
    conn = _conn()
    cur = conn.cursor()
    cur.execute("""
      INSERT INTO contests (created_at, start_time, duration_minutes, handles_json, problems_json)
      VALUES (?, NULL, ?, ?, ?)
    """, (created_at, duration_minutes, json.dumps(handles), json.dumps(problems)))
    conn.commit()
    cid = cur.lastrowid
    conn.close()
    return int(cid)

def get_contest(contest_id: int) -> Optional[Dict[str, Any]]:
    conn = _conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM contests WHERE id = ?", (contest_id,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    return {
        "id": row["id"],
        "created_at": row["created_at"],
        "start_time": row["start_time"],
        "duration_minutes": row["duration_minutes"],
        "handles": json.loads(row["handles_json"]),
        "problems": json.loads(row["problems_json"]),
    }

def list_contests(limit: int = 20) -> List[Dict[str, Any]]:
    conn = _conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM contests ORDER BY id DESC LIMIT ?", (limit,))
    rows = cur.fetchall()
    conn.close()

    out = []
    for r in rows:
        out.append({
            "id": r["id"],
            "created_at": r["created_at"],
            "start_time": r["start_time"],
            "duration_minutes": r["duration_minutes"],
            "handles": json.loads(r["handles_json"]),
            "problems": json.loads(r["problems_json"]),
        })
    return out

def start_contest(contest_id: int, start_time: int) -> None:
    conn = _conn()
    cur = conn.cursor()
    cur.execute("UPDATE contests SET start_time = ? WHERE id = ?", (start_time, contest_id))
    conn.commit()
    conn.close()
