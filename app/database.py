import sqlite3
import datetime
from contextlib import contextmanager
from typing import Generator, Any, Dict, List, Optional
from app.config import DATABASE_PATH

@contextmanager
def get_db_cursor() -> Generator[sqlite3.Cursor, None, None]:
    """Provide a transactional cursor to the SQLite database."""
    conn = sqlite3.connect(str(DATABASE_PATH), timeout=15.0)
    conn.row_factory = sqlite3.Row
    # Enable foreign keys
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()
    try:
        yield cursor
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def dict_from_row(row: Optional[sqlite3.Row]) -> Optional[Dict[str, Any]]:
    """Convert an sqlite3.Row to a plain dictionary."""
    if row is None:
        return None
    return dict(row)

def dicts_from_rows(rows: List[sqlite3.Row]) -> List[Dict[str, Any]]:
    """Convert a list of sqlite3.Row objects to a list of dictionaries."""
    return [dict(r) for r in rows]

def init_db():
    """Create tables and indexes if they do not exist."""
    with get_db_cursor() as cur:
        # Users Table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                mobile TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'citizen', -- 'citizen' or 'authority'
                department TEXT,                      -- for authority: e.g. 'Electricity', 'PWD/Roads', 'Water'
                village TEXT,                         -- for citizen: village / ward / locality
                preferred_language TEXT DEFAULT 'en', -- 'en', 'te', 'hi'
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Complaints Table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS complaints (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                complaint_id TEXT UNIQUE NOT NULL,    -- GS-2026-00001
                user_id INTEGER NOT NULL,
                description TEXT NOT NULL,
                voice_transcript TEXT,
                category TEXT NOT NULL,               -- e.g. 'Electricity', 'Roads', 'Water'
                ai_category TEXT,
                priority TEXT NOT NULL DEFAULT 'MEDIUM', -- 'HIGH', 'MEDIUM', 'LOW'
                priority_reason TEXT,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                location_name TEXT NOT NULL,
                department TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Submitted', -- 'Submitted', 'Under Review', 'Assigned', 'In Progress', 'Resolved', 'Rejected'
                resolution_notes TEXT,
                spam_flag INTEGER DEFAULT 0,          -- 0 = Normal, 1 = Suspicious/Duplicate
                duplicate_flag INTEGER DEFAULT 0,
                is_demo INTEGER DEFAULT 0,            -- 0 = Real Citizen, 1 = Seeded Demo
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)

        # Complaint Images Table (Strict 1-to-1 or 1-to-many link to complaint_id)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS complaint_images (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                complaint_id TEXT NOT NULL,
                file_name TEXT NOT NULL,
                file_path TEXT NOT NULL,
                file_type TEXT NOT NULL,
                file_size INTEGER NOT NULL,
                image_hash TEXT,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (complaint_id) REFERENCES complaints(complaint_id) ON DELETE CASCADE
            )
        """)

        # Notifications Table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                complaint_id TEXT,
                title_en TEXT NOT NULL,
                title_te TEXT NOT NULL,
                title_hi TEXT NOT NULL,
                message_en TEXT NOT NULL,
                message_te TEXT NOT NULL,
                message_hi TEXT NOT NULL,
                is_read INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)

        # Audit Logs Table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                complaint_id TEXT NOT NULL,
                action_by TEXT NOT NULL,
                action_type TEXT NOT NULL,
                old_status TEXT,
                new_status TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Indexes for fast lookup & query performance
        cur.execute("CREATE INDEX IF NOT EXISTS idx_complaints_user ON complaints(user_id)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_complaints_status ON complaints(status)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_complaints_category ON complaints(category)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_complaints_created ON complaints(created_at)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_images_complaint_id ON complaint_images(complaint_id)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_images_hash ON complaint_images(image_hash)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_notifications_user ON notifications(user_id)")

def generate_next_complaint_id() -> str:
    """Generate sequential format ID like GS-2026-00001."""
    current_year = datetime.datetime.now().year
    with get_db_cursor() as cur:
        cur.execute("SELECT COUNT(*) as count FROM complaints")
        row = cur.fetchone()
        count = row["count"] if row else 0
        next_num = count + 1
        return f"GS-{current_year}-{next_num:05d}"
