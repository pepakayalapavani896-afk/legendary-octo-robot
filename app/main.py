import os
import uuid
import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any

from fastapi import FastAPI, Request, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.config import (
    STATIC_DIR, TEMPLATES_DIR, UPLOADS_DIR, MAX_FILE_SIZE_BYTES,
    ALLOWED_EXTENSIONS, ALLOWED_MIME_TYPES, APP_NAME, APP_TAGLINE
)
from app.database import (
    init_db, get_db_cursor, dict_from_row, dicts_from_rows, generate_next_complaint_id
)
from app.auth import (
    hash_password, verify_password, create_access_token,
    get_current_user, get_current_user_optional, require_citizen, require_authority
)
from app.ai_engine import analyze_complaint_ai
from app.spam_detector import (
    check_daily_submission_limit, compute_image_hash, check_duplicate_image, check_excessive_submissions
)
from app.geo_utils import (
    reverse_geocode_location, detect_hotspots, detect_repeated_resources
)
from app.seed_data import seed_demo_data

# Initialize FastAPI App
app = FastAPI(
    title=APP_NAME,
    description="Smart Rural Problem-to-Solution Network (SIH Prototype)",
    version="1.0.0"
)

# Enable CORS for local testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files and uploads
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
app.mount("/uploads", StaticFiles(directory=str(UPLOADS_DIR)), name="uploads")

@app.on_event("startup")
def on_startup():
    init_db()
    seed_demo_data()

# ----------------- Request Models -----------------
class RegisterRequest(BaseModel):
    name: str
    email: str
    mobile: str
    password: str
    village: Optional[str] = ""
    preferred_language: Optional[str] = "en"

class LoginRequest(BaseModel):
    identifier: str  # email or mobile
    password: str

class AIAnalysisRequest(BaseModel):
    description: str
    voice_transcript: Optional[str] = ""
    language: Optional[str] = "en"

class StatusUpdateRequest(BaseModel):
    status: str
    resolution_notes: Optional[str] = None
    department: Optional[str] = None
    priority: Optional[str] = None

class AssignDepartmentRequest(BaseModel):
    department: str
    notes: Optional[str] = None

class FlagSpamRequest(BaseModel):
    spam_flag: int  # 0 or 1
    reason: Optional[str] = None

# ----------------- Main Landing / SPA Route -----------------
@app.get("/", response_class=HTMLResponse)
async def serve_index():
    index_file = TEMPLATES_DIR / "index.html"
    if not index_file.exists():
        return HTMLResponse("<h1>GramSetu is initializing...</h1>", status_code=200)
    with open(index_file, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read(), status_code=200)

# ----------------- Authentication Endpoints -----------------
@app.post("/api/auth/register")
async def register(req: RegisterRequest):
    name = req.name.strip()
    email = req.email.strip().lower()
    mobile = req.mobile.strip()
    password = req.password

    if len(password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters long.")
    if not mobile or len(mobile) < 10:
        raise HTTPException(status_code=400, detail="Please enter a valid 10-digit mobile number.")

    pwd_hash = hash_password(password)

    with get_db_cursor() as cur:
        cur.execute("SELECT id FROM users WHERE email = ? OR mobile = ?", (email, mobile))
        if cur.fetchone():
            raise HTTPException(status_code=400, detail="Account with this email or mobile already exists.")

        cur.execute("""
            INSERT INTO users (name, email, mobile, password_hash, role, village, preferred_language)
            VALUES (?, ?, ?, ?, 'citizen', ?, ?)
        """, (name, email, mobile, pwd_hash, req.village or "Local Village", req.preferred_language or "en"))
        user_id = cur.lastrowid

    token = create_access_token({"sub": user_id, "role": "citizen", "email": email})
    return {
        "success": True,
        "token": token,
        "user": {
            "id": user_id,
            "name": name,
            "email": email,
            "mobile": mobile,
            "role": "citizen",
            "village": req.village,
            "preferred_language": req.preferred_language or "en"
        }
    }

@app.post("/api/auth/login")
async def login(req: LoginRequest):
    identifier = req.identifier.strip().lower()
    password = req.password

    with get_db_cursor() as cur:
        cur.execute("SELECT * FROM users WHERE email = ? OR mobile = ?", (identifier, identifier))
        user_row = cur.fetchone()

        if not user_row:
            raise HTTPException(status_code=400, detail="Invalid login credentials.")

        user = dict_from_row(user_row)
        if not verify_password(user["password_hash"], password):
            raise HTTPException(status_code=400, detail="Invalid password.")

    token = create_access_token({"sub": user["id"], "role": user["role"], "email": user["email"]})
    return {
        "success": True,
        "token": token,
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "mobile": user["mobile"],
            "role": user["role"],
            "department": user.get("department"),
            "village": user.get("village"),
            "preferred_language": user.get("preferred_language", "en")
        }
    }

@app.post("/api/auth/authority-login")
async def authority_login(req: LoginRequest):
    identifier = req.identifier.strip().lower()
    password = req.password

    with get_db_cursor() as cur:
        cur.execute("SELECT * FROM users WHERE (email = ? OR mobile = ?) AND role IN ('authority', 'admin')", (identifier, identifier))
        user_row = cur.fetchone()

        if not user_row:
            raise HTTPException(status_code=400, detail="Authority credentials not found or unauthorized role.")

        user = dict_from_row(user_row)
        if not verify_password(user["password_hash"], password):
            raise HTTPException(status_code=400, detail="Incorrect authority password.")

    token = create_access_token({"sub": user["id"], "role": user["role"], "email": user["email"]})
    return {
        "success": True,
        "token": token,
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "mobile": user["mobile"],
            "role": user["role"],
            "department": user.get("department"),
            "village": user.get("village"),
            "preferred_language": user.get("preferred_language", "en")
        }
    }

@app.get("/api/auth/me")
async def get_me(user: Dict[str, Any] = Depends(get_current_user)):
    return {"success": True, "user": user}

# ----------------- AI & Anti-Spam Endpoints -----------------
@app.post("/api/complaints/analyze-ai")
async def analyze_complaint(req: AIAnalysisRequest):
    result = analyze_complaint_ai(
        description=req.description,
        voice_transcript=req.voice_transcript or "",
        language=req.language or "en"
    )
    return {"success": True, "analysis": result}

@app.get("/api/complaints/check-limit")
async def check_user_daily_limit(user: Dict[str, Any] = Depends(get_current_user)):
    if user.get("role") in ("authority", "admin"):
        return {"allowed": True, "message": "Authority accounts have unlimited reporting quota."}
    
    allowed, message = check_daily_submission_limit(user["id"])
    return {"allowed": allowed, "message": message}

# ----------------- Citizen Complaint Submission -----------------
@app.post("/api/complaints/submit")
async def submit_complaint(
    description: str = Form(...),
    voice_transcript: Optional[str] = Form(""),
    category: str = Form(...),
    ai_category: Optional[str] = Form(""),
    priority: str = Form("MEDIUM"),
    priority_reason: Optional[str] = Form(""),
    latitude: float = Form(...),
    longitude: float = Form(...),
    location_name: str = Form(...),
    department: str = Form(...),
    photo: Optional[UploadFile] = File(None),
    user: Dict[str, Any] = Depends(get_current_user)
):
    user_id = user["id"]

    # 1. Enforce 1 Complaint Per User Per Day (for citizens)
    if user.get("role") == "citizen":
        allowed, msg = check_daily_submission_limit(user_id)
        if not allowed:
            raise HTTPException(status_code=429, detail=msg)

    # 2. Check identical spam text
    is_text_spam, spam_note = check_excessive_submissions(user_id, description)

    # Generate unique Complaint ID
    complaint_id = generate_next_complaint_id()

    # 3. Handle Citizen Photo (Strict Rule: real uploaded photo linked to this complaint)
    saved_file_name = None
    saved_file_path = None
    file_type = None
    file_size = 0
    image_hash = None
    is_duplicate_img = False

    if photo and photo.filename:
        # Validate extension
        ext = Path(photo.filename).suffix.lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(status_code=400, detail=f"Unsupported file format '{ext}'. Allowed: JPG, PNG, WebP.")

        # Read bytes & validate size
        photo_bytes = await photo.read()
        file_size = len(photo_bytes)
        if file_size > MAX_FILE_SIZE_BYTES:
            raise HTTPException(status_code=400, detail="Uploaded photo exceeds maximum 5 MB limit.")

        if file_size > 0:
            # Generate unique server-side filename strictly associated with complaint_id
            safe_filename = f"citizen-uploaded-photo-for-{complaint_id}{ext}"
            file_dest = UPLOADS_DIR / safe_filename
            with open(file_dest, "wb") as f:
                f.write(photo_bytes)

            saved_file_name = safe_filename
            saved_file_path = f"/uploads/{safe_filename}"
            file_type = photo.content_type or f"image/{ext.lstrip('.')}"
            image_hash = compute_image_hash(photo_bytes)

            # Check duplicate image
            is_dup, existing_cid = check_duplicate_image(image_hash)
            if is_dup:
                is_duplicate_img = True

    # Determine spam & duplicate flags
    spam_flag = 1 if (is_duplicate_img or is_text_spam) else 0
    duplicate_flag = 1 if is_duplicate_img else 0
    initial_status = "Under Review" if spam_flag == 1 else "Submitted"

    # Insert complaint into database
    with get_db_cursor() as cur:
        cur.execute("""
            INSERT INTO complaints (
                complaint_id, user_id, description, voice_transcript, category, ai_category,
                priority, priority_reason, latitude, longitude, location_name, department,
                status, spam_flag, duplicate_flag, is_demo
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0)
        """, (
            complaint_id, user_id, description.strip(), voice_transcript.strip() if voice_transcript else "",
            category, ai_category or category, priority, priority_reason or "Reported by citizen",
            latitude, longitude, location_name, department, initial_status, spam_flag, duplicate_flag
        ))

        # If photo was uploaded, insert into complaint_images
        if saved_file_name:
            cur.execute("""
                INSERT INTO complaint_images (
                    complaint_id, file_name, file_path, file_type, file_size, image_hash
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (complaint_id, saved_file_name, saved_file_path, file_type, file_size, image_hash))

        # Insert notification for the citizen
        cur.execute("""
            INSERT INTO notifications (user_id, complaint_id, title_en, title_te, title_hi, message_en, message_te, message_hi)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            complaint_id,
            f"Complaint #{complaint_id} Submitted Successfully",
            f"ఫిర్యాదు #{complaint_id} విజయవంతంగా సమర్పించబడింది",
            f"शिकायत #{complaint_id} सफलतापूर्वक दर्ज की गई",
            f"Your complaint regarding '{category}' has been registered and routed to {department}.",
            f"'{category}' పై మీ ఫిర్యాదు నమోదు చేయబడింది మరియు {department} కు పంపబడింది.",
            f"'{category}' पर आपकी शिकायत दर्ज कर {department} को अग्रेषित कर दी गई है।"
        ))

    return {
        "success": True,
        "complaint_id": complaint_id,
        "status": initial_status,
        "spam_flag": spam_flag,
        "duplicate_flag": duplicate_flag,
        "has_photo": bool(saved_file_path),
        "photo_url": saved_file_path,
        "message": "Grievance submitted successfully. Tracking timeline is active."
    }

# ----------------- Citizen Complaint List & Notifications -----------------
@app.get("/api/complaints/my")
async def get_my_complaints(user: Dict[str, Any] = Depends(get_current_user)):
    with get_db_cursor() as cur:
        cur.execute("""
            SELECT c.*, ci.file_path as image_url, ci.file_name as image_name
            FROM complaints c
            LEFT JOIN complaint_images ci ON c.complaint_id = ci.complaint_id
            WHERE c.user_id = ?
            ORDER BY c.created_at DESC
        """, (user["id"],))
        rows = cur.fetchall()
        return {"success": True, "complaints": dicts_from_rows(rows)}

@app.get("/api/notifications")
async def get_notifications(user: Dict[str, Any] = Depends(get_current_user)):
    with get_db_cursor() as cur:
        cur.execute("""
            SELECT * FROM notifications 
            WHERE user_id = ? 
            ORDER BY created_at DESC LIMIT 30
        """, (user["id"],))
        rows = cur.fetchall()
        return {"success": True, "notifications": dicts_from_rows(rows)}

@app.post("/api/notifications/read-all")
async def mark_notifications_read(user: Dict[str, Any] = Depends(get_current_user)):
    with get_db_cursor() as cur:
        cur.execute("UPDATE notifications SET is_read = 1 WHERE user_id = ?", (user["id"],))
        return {"success": True}

# ----------------- Authority Portal Endpoints -----------------
@app.get("/api/authority/stats")
async def get_authority_stats(user: Dict[str, Any] = Depends(require_authority)):
    with get_db_cursor() as cur:
        # Total counts
        cur.execute("SELECT COUNT(*) as total FROM complaints")
        total = cur.fetchone()["total"]

        cur.execute("SELECT COUNT(*) as pending FROM complaints WHERE status IN ('Submitted', 'Under Review')")
        pending = cur.fetchone()["pending"]

        cur.execute("SELECT COUNT(*) as in_progress FROM complaints WHERE status IN ('Assigned', 'In Progress')")
        in_progress = cur.fetchone()["in_progress"]

        cur.execute("SELECT COUNT(*) as resolved FROM complaints WHERE status = 'Resolved'")
        resolved = cur.fetchone()["resolved"]

        cur.execute("SELECT COUNT(*) as high_priority FROM complaints WHERE priority = 'HIGH' AND status != 'Resolved'")
        high_priority = cur.fetchone()["high_priority"]

        cur.execute("SELECT COUNT(*) as spam_count FROM complaints WHERE spam_flag = 1")
        spam_count = cur.fetchone()["spam_count"]

        # Category breakdown
        cur.execute("""
            SELECT category, COUNT(*) as count 
            FROM complaints 
            GROUP BY category 
            ORDER BY count DESC
        """)
        categories = dicts_from_rows(cur.fetchall())

        # Department breakdown
        cur.execute("""
            SELECT department, COUNT(*) as count 
            FROM complaints 
            GROUP BY department 
            ORDER BY count DESC
        """)
        departments = dicts_from_rows(cur.fetchall())

        # Detect active hotspots
        cur.execute("SELECT * FROM complaints WHERE status != 'Resolved'")
        all_active = dicts_from_rows(cur.fetchall())
        hotspots = detect_hotspots(all_active)
        repeated = detect_repeated_resources(all_active)

        return {
            "success": True,
            "stats": {
                "total": total,
                "pending": pending,
                "in_progress": in_progress,
                "resolved": resolved,
                "high_priority": high_priority,
                "spam_count": spam_count,
                "hotspots_count": len(hotspots),
                "repeated_count": len(repeated)
            },
            "category_breakdown": categories,
            "department_breakdown": departments,
            "hotspots": hotspots,
            "repeated_issues": repeated
        }

@app.get("/api/authority/complaints")
async def get_authority_complaints(
    status_filter: Optional[str] = None,
    category_filter: Optional[str] = None,
    priority_filter: Optional[str] = None,
    search: Optional[str] = None,
    user: Dict[str, Any] = Depends(require_authority)
):
    # Citizen Privacy Rule: Do NOT join users table or expose citizen personal identity (name, phone, email).
    # Authorities only see location_name, coordinates, category, description, status, photo evidence, and timestamps.
    query = """
        SELECT c.id, c.complaint_id, c.description, c.voice_transcript, c.category, c.ai_category,
               c.priority, c.priority_reason, c.latitude, c.longitude, c.location_name, c.department,
               c.status, c.resolution_notes, c.spam_flag, c.duplicate_flag, c.is_demo,
               c.created_at, c.updated_at,
               ci.file_path as image_url, ci.file_name as image_name
        FROM complaints c
        LEFT JOIN complaint_images ci ON c.complaint_id = ci.complaint_id
        WHERE 1=1
    """
    params = []

    if status_filter and status_filter != "all":
        query += " AND c.status = ?"
        params.append(status_filter)

    if category_filter and category_filter != "all":
        query += " AND c.category = ?"
        params.append(category_filter)

    if priority_filter and priority_filter != "all":
        query += " AND c.priority = ?"
        params.append(priority_filter)

    if search:
        s = f"%{search.strip()}%"
        query += " AND (c.complaint_id LIKE ? OR c.description LIKE ? OR c.location_name LIKE ? OR c.category LIKE ? OR c.department LIKE ?)"
        params.extend([s, s, s, s, s])

    query += " ORDER BY c.created_at DESC"

    with get_db_cursor() as cur:
        cur.execute(query, params)
        rows = cur.fetchall()
        return {"success": True, "complaints": dicts_from_rows(rows)}

@app.get("/api/authority/complaints/{complaint_id}")
async def get_complaint_detail(complaint_id: str, user: Dict[str, Any] = Depends(require_authority)):
    with get_db_cursor() as cur:
        # Citizen Privacy Rule: No personal identity (name, phone, email) exposed to authority.
        # Only location, GPS coordinates, category, evidence photo, and grievance details are provided.
        cur.execute("""
            SELECT c.id, c.complaint_id, c.description, c.voice_transcript, c.category, c.ai_category,
                   c.priority, c.priority_reason, c.latitude, c.longitude, c.location_name, c.department,
                   c.status, c.resolution_notes, c.spam_flag, c.duplicate_flag, c.is_demo,
                   c.created_at, c.updated_at,
                   ci.file_path as image_url, ci.file_name as image_name, ci.file_size as image_size, ci.uploaded_at as image_uploaded_at
            FROM complaints c
            LEFT JOIN complaint_images ci ON c.complaint_id = ci.complaint_id
            WHERE c.complaint_id = ?
        """, (complaint_id,))
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Complaint record not found.")

        complaint = dict_from_row(row)

        # Audit logs
        cur.execute("""
            SELECT * FROM audit_logs WHERE complaint_id = ? ORDER BY created_at ASC
        """, (complaint_id,))
        audit_logs = dicts_from_rows(cur.fetchall())
        complaint["audit_logs"] = audit_logs

        return {"success": True, "complaint": complaint}

@app.put("/api/authority/complaints/{complaint_id}/status")
async def update_complaint_status(
    complaint_id: str,
    req: StatusUpdateRequest,
    user: Dict[str, Any] = Depends(require_authority)
):
    new_status = req.status.strip() if req.status else None
    resolution_notes = req.resolution_notes.strip() if req.resolution_notes else ""
    department = req.department.strip() if req.department else None
    priority = req.priority.strip() if req.priority else None

    if new_status == "Resolved" and not resolution_notes:
        raise HTTPException(
            status_code=400,
            detail="Resolution note is mandatory when closing and marking a grievance as Resolved."
        )

    with get_db_cursor() as cur:
        cur.execute("SELECT * FROM complaints WHERE complaint_id = ?", (complaint_id,))
        comp = cur.fetchone()
        if not comp:
            raise HTTPException(status_code=404, detail="Complaint not found.")

        old_status = comp["status"]
        old_dept = comp["department"]
        old_priority = comp["priority"]
        user_id = comp["user_id"]
        category = comp["category"]

        final_status = new_status or old_status
        final_dept = department or old_dept
        final_priority = priority or old_priority
        final_resolution_notes = resolution_notes if (final_status == "Resolved" or resolution_notes) else comp["resolution_notes"]

        cur.execute("""
            UPDATE complaints 
            SET status = ?, resolution_notes = ?, department = ?, priority = ?, updated_at = CURRENT_TIMESTAMP
            WHERE complaint_id = ?
        """, (final_status, final_resolution_notes, final_dept, final_priority, complaint_id))

        # Log audit action
        audit_notes_parts = []
        if final_status != old_status:
            audit_notes_parts.append(f"Status changed from '{old_status}' to '{final_status}'.")
        if final_dept != old_dept:
            audit_notes_parts.append(f"Department reassigned from '{old_dept}' to '{final_dept}'.")
        if final_priority != old_priority:
            audit_notes_parts.append(f"Priority adjusted from '{old_priority}' to '{final_priority}'.")
        if resolution_notes:
            audit_notes_parts.append(f"Notes: {resolution_notes}")

        audit_summary = " ".join(audit_notes_parts) if audit_notes_parts else "Updated by authority."

        cur.execute("""
            INSERT INTO audit_logs (complaint_id, action_by, action_type, old_status, new_status, notes)
            VALUES (?, ?, 'STATUS_UPDATE', ?, ?, ?)
        """, (complaint_id, user["name"], old_status, final_status, audit_summary))

        # Dispatch notification to citizen
        title_en = f"Complaint #{complaint_id} Status: {final_status}"
        title_te = f"ఫిర్యాదు #{complaint_id} స్థితి: {final_status}"
        title_hi = f"शिकायत #{complaint_id} स्थिति: {final_status}"

        msg_en = f"Status updated to '{final_status}' by {final_dept}." + (f" Resolution: {final_resolution_notes}" if final_status == 'Resolved' else "")
        msg_te = f"మీ ఫిర్యాదు స్థితి '{final_status}' గా {final_dept} ద్వారా మార్చబడింది." + (f" పరిష్కారం: {final_resolution_notes}" if final_status == 'Resolved' else "")
        msg_hi = f"आपकी शिकायत की स्थिति '{final_status}' ({final_dept}) कर दी गई है।" + (f" समाधान: {final_resolution_notes}" if final_status == 'Resolved' else "")

        cur.execute("""
            INSERT INTO notifications (user_id, complaint_id, title_en, title_te, title_hi, message_en, message_te, message_hi)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (user_id, complaint_id, title_en, title_te, title_hi, msg_en, msg_te, msg_hi))

    return {
        "success": True,
        "complaint_id": complaint_id,
        "status": final_status,
        "department": final_dept,
        "priority": final_priority,
        "resolution_notes": final_resolution_notes
    }

@app.put("/api/authority/complaints/{complaint_id}/assign")
async def assign_department(
    complaint_id: str,
    req: AssignDepartmentRequest,
    user: Dict[str, Any] = Depends(require_authority)
):
    with get_db_cursor() as cur:
        cur.execute("SELECT user_id, department, status FROM complaints WHERE complaint_id = ?", (complaint_id,))
        comp = cur.fetchone()
        if not comp:
            raise HTTPException(status_code=404, detail="Complaint not found.")

        old_dept = comp["department"]
        old_status = comp["status"]
        user_id = comp["user_id"]

        # Only change status to Assigned if it was previously Submitted or Under Review; otherwise preserve status
        new_status = "Assigned" if old_status in ("Submitted", "Under Review") else old_status

        cur.execute("""
            UPDATE complaints 
            SET department = ?, status = ?, updated_at = CURRENT_TIMESTAMP
            WHERE complaint_id = ?
        """, (req.department, new_status, complaint_id))

        cur.execute("""
            INSERT INTO audit_logs (complaint_id, action_by, action_type, old_status, new_status, notes)
            VALUES (?, ?, 'DEPARTMENT_REASSIGN', ?, ?, ?)
        """, (complaint_id, user["name"], old_status, new_status, f"Reassigned from {old_dept} to {req.department}. {req.notes or ''}"))

        # Notification
        cur.execute("""
            INSERT INTO notifications (user_id, complaint_id, title_en, title_te, title_hi, message_en, message_te, message_hi)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id, complaint_id,
            f"Assigned to {req.department}",
            f"{req.department} కు కేటాయించబడింది",
            f"{req.department} को सौंपा गया",
            f"Grievance #{complaint_id} assigned to {req.department}.",
            f"ఫిర్యాదు #{complaint_id} {req.department} కు కేటాయించబడింది.",
            f"शिकायत #{complaint_id} {req.department} को सौंपी गई।"
        ))

    return {"success": True, "department": req.department, "status": new_status}

@app.put("/api/authority/complaints/{complaint_id}/flag-spam")
async def flag_spam(
    complaint_id: str,
    req: FlagSpamRequest,
    user: Dict[str, Any] = Depends(require_authority)
):
    with get_db_cursor() as cur:
        cur.execute("""
            UPDATE complaints SET spam_flag = ?, updated_at = CURRENT_TIMESTAMP WHERE complaint_id = ?
        """, (req.spam_flag, complaint_id))

        cur.execute("""
            INSERT INTO audit_logs (complaint_id, action_by, action_type, notes)
            VALUES (?, ?, 'SPAM_FLAG_TOGGLE', ?)
        """, (complaint_id, user["name"], f"Spam flag set to {req.spam_flag}. Reason: {req.reason or 'Authority review'}"))

    return {"success": True, "spam_flag": req.spam_flag}

# ----------------- Problem Map & Reverse Geo Endpoints -----------------
@app.get("/api/map/complaints")
async def get_map_complaints():
    with get_db_cursor() as cur:
        cur.execute("""
            SELECT c.id, c.complaint_id, c.category, c.priority, c.latitude, c.longitude, 
                   c.location_name, c.status, c.is_demo, c.spam_flag, c.created_at,
                   ci.file_path as image_url, ci.file_name as image_name
            FROM complaints c
            LEFT JOIN complaint_images ci ON c.complaint_id = ci.complaint_id
            WHERE c.status != 'Rejected'
        """)
        complaints = dicts_from_rows(cur.fetchall())
        hotspots = detect_hotspots(complaints)
        repeated = detect_repeated_resources(complaints)

        return {
            "success": True,
            "complaints": complaints,
            "hotspots": hotspots,
            "repeated_resources": repeated
        }

@app.get("/api/geo/reverse")
async def reverse_geocode(lat: float, lon: float):
    result = reverse_geocode_location(lat, lon)
    return {"success": True, "location": result}
