import hashlib
import datetime
from typing import Tuple, Dict, Any, Optional
from app.database import get_db_cursor

def check_daily_submission_limit(user_id: int) -> Tuple[bool, str]:
    """
    Rule: Each authenticated citizen can submit a maximum of ONE complaint per day.
    Returns: (is_allowed: bool, message: str)
    """
    today_str = datetime.date.today().isoformat()  # YYYY-MM-DD
    with get_db_cursor() as cur:
        # SQLite strftime('%Y-%m-%d', created_at)
        cur.execute("""
            SELECT COUNT(*) as today_count 
            FROM complaints 
            WHERE user_id = ? AND DATE(created_at) = DATE('now', 'localtime')
        """, (user_id,))
        row = cur.fetchone()
        count = row["today_count"] if row else 0

        # Also fallback check with python string matching if SQLite local date differs
        if count == 0:
            cur.execute("""
                SELECT created_at FROM complaints 
                WHERE user_id = ? ORDER BY created_at DESC LIMIT 1
            """, (user_id,))
            last = cur.fetchone()
            if last and last["created_at"]:
                last_date = str(last["created_at"])[:10]
                if last_date == today_str:
                    count = 1

        if count >= 1:
            return False, "⚠️ Daily complaint limit reached. You can submit another complaint tomorrow."
        
        return True, "Allowed"

def compute_image_hash(image_bytes: bytes) -> str:
    """Compute SHA-256 / MD5 digest of the image binary data."""
    return hashlib.sha256(image_bytes).hexdigest()

def check_duplicate_image(image_hash: str) -> Tuple[bool, Optional[str]]:
    """
    Check if the uploaded image hash exists in previous complaints.
    Returns: (is_duplicate: bool, existing_complaint_id: Optional[str])
    """
    if not image_hash:
        return False, None

    with get_db_cursor() as cur:
        cur.execute("""
            SELECT complaint_id FROM complaint_images 
            WHERE image_hash = ? LIMIT 1
        """, (image_hash,))
        row = cur.fetchone()
        if row:
            return True, row["complaint_id"]
        return False, None

def check_excessive_submissions(user_id: int, description: str) -> Tuple[bool, str]:
    """
    Check for identical text spam from the same user.
    """
    with get_db_cursor() as cur:
        cur.execute("""
            SELECT complaint_id FROM complaints 
            WHERE user_id = ? AND description = ? AND created_at >= datetime('now', '-7 days')
            LIMIT 1
        """, (user_id, description.strip()))
        row = cur.fetchone()
        if row:
            return True, f"Identical grievance description previously submitted in {row['complaint_id']}"
        return False, ""
