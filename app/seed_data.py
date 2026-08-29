from app.database import get_db_cursor
from app.auth import hash_password

def seed_demo_data():
    """Populate demo authority & citizen accounts and demo reference complaints."""
    with get_db_cursor() as cur:
        # Check if users already exist
        cur.execute("SELECT COUNT(*) as count FROM users")
        if cur.fetchone()["count"] > 0:
            return  # Already seeded

        # 1. Authority Accounts (Clearly designated prototype accounts)
        authorities = [
            ("Central District Administrator", "admin@gramsetu.gov.in", "9900000001", hash_password("admin123"), "authority", "District Administrative Cell", "District HQ", "en"),
            ("Electrical Division Officer", "officer.electricity@gramsetu.gov.in", "9900000002", hash_password("demo123"), "authority", "Electricity Department", "Power Grid Sub-Division", "te"),
            ("PWD Roads Executive Engineer", "officer.pwd@gramsetu.gov.in", "9900000003", hash_password("demo123"), "authority", "Roads & Public Works Department (PWD)", "PWD Circle", "hi"),
            ("Water Supply Superintending Officer", "officer.water@gramsetu.gov.in", "9900000004", hash_password("demo123"), "authority", "Rural Water Supply & Sanitation Department", "Water Board", "en"),
            ("Panchayat Sanitation Inspector", "officer.sanitation@gramsetu.gov.in", "9900000005", hash_password("demo123"), "authority", "Panchayat Sanitation Department", "Rural Block Office", "te")
        ]
        cur.executemany("""
            INSERT INTO users (name, email, mobile, password_hash, role, department, village, preferred_language)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, authorities)

        # 2. Demo Citizen Accounts
        citizens = [
            ("Ravi Kumar (Demo Citizen)", "citizen@gramsetu.in", "9876543210", hash_password("citizen123"), "citizen", None, "Gandhi Nagar Ward 3", "te"),
            ("Priya Sharma (Demo Citizen)", "priya@gramsetu.in", "9876543211", hash_password("citizen123"), "citizen", None, "Shanti Nagar", "hi"),
            ("Anand Varma (Demo Citizen)", "anand@gramsetu.in", "9876543212", hash_password("citizen123"), "citizen", None, "Subhash Ward", "en")
        ]
        cur.executemany("""
            INSERT INTO users (name, email, mobile, password_hash, role, department, village, preferred_language)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, citizens)

        # Get citizen user ID
        cur.execute("SELECT id FROM users WHERE email = 'citizen@gramsetu.in'")
        citizen_id = cur.fetchone()["id"]
        cur.execute("SELECT id FROM users WHERE email = 'priya@gramsetu.in'")
        priya_id = cur.fetchone()["id"]

        # 3. Seed Reference Complaints (All marked is_demo = 1 for SIH transparency)
        demo_complaints = [
            (
                "GS-2026-00001",
                citizen_id,
                "మా వీధిలో రెండు వారాలుగా స్ట్రీట్ లైట్ పనిచేయడం లేదు. రాత్రి వేళల్లో తీవ్రమైన చీకటి మరియు భద్రత సమస్య.",
                "మా వీధిలో రెండు వారాలుగా స్ట్రీట్ లైట్ పనిచేయడం లేదు",
                "Electricity",
                "Electricity",
                "MEDIUM",
                "Reported disruption to public lighting / power facility.",
                17.385044,
                78.486671,
                "Old City Sector 4, Hyderabad, Telangana",
                "Electricity Department",
                "Under Review",
                None,
                0,
                0,
                1
            ),
            (
                "GS-2026-00002",
                priya_id,
                "मुख्य रास्ते पर बड़ा गड्ढा होने से कई गाड़ियां फिसल रही हैं। तुरंत मरम्मत की आवश्यकता है।",
                "मुख्य रास्ते पर बड़ा गड्ढा होने से गाड़ियां फिसल रही हैं",
                "Roads",
                "Roads",
                "HIGH",
                "Potential immediate public safety impact or accident risk.",
                17.387120,
                78.489150,
                "Main Bazaar Road, Hyderabad, Telangana",
                "Roads & Public Works Department (PWD)",
                "Assigned",
                None,
                0,
                0,
                1
            ),
            (
                "GS-2026-00003",
                citizen_id,
                "Water supply pipeline burst near the community center. Pure drinking water is continuously leaking onto the road.",
                "Drinking water pipe burst near community center",
                "Water Supply",
                "Water Supply",
                "HIGH",
                "Impact on essential drinking water / pipeline supply.",
                17.386200,
                78.488300,
                "Community Center Lane, Sector 4, Hyderabad",
                "Rural Water Supply & Sanitation Department",
                "In Progress",
                "Field maintenance team dispatched with replacement pipeline section.",
                0,
                0,
                1
            ),
            (
                "GS-2026-00004",
                priya_id,
                "Low water pressure and muddy water coming from residential tap connections since 3 days.",
                "Water pressure low and cloudy water",
                "Water Supply",
                "Water Supply",
                "MEDIUM",
                "Impact on essential drinking water / pipeline supply.",
                17.386800,
                78.487900,
                "Lane 2, Sector 4, Hyderabad",
                "Rural Water Supply & Sanitation Department",
                "In Progress",
                None,
                0,
                0,
                1
            ),
            (
                "GS-2026-00005",
                citizen_id,
                "Another water pipe valve leak causing localized water logging on the street corner.",
                "Water valve leaking on street corner",
                "Water Supply",
                "Water Supply",
                "MEDIUM",
                "Impact on essential drinking water / pipeline supply.",
                17.386500,
                78.488100,
                "Crossroad 3, Sector 4, Hyderabad",
                "Rural Water Supply & Sanitation Department",
                "Submitted",
                None,
                0,
                0,
                1
            ),
            (
                "GS-2026-00006",
                priya_id,
                "Open garbage collection point overflowing on the school boundary wall. Strong bad odor and stray animals.",
                "Garbage overflowing near primary school",
                "Sanitation",
                "Sanitation",
                "MEDIUM",
                "Public health & hygiene maintenance requirement.",
                17.389500,
                78.485200,
                "Primary School Road, Hyderabad",
                "Panchayat Sanitation Department",
                "Resolved",
                "Sanitation team cleared 3 tons of garbage and placed closed covered bins.",
                0,
                0,
                1
            )
        ]

        cur.executemany("""
            INSERT INTO complaints (
                complaint_id, user_id, description, voice_transcript, category, ai_category,
                priority, priority_reason, latitude, longitude, location_name, department,
                status, resolution_notes, spam_flag, duplicate_flag, is_demo
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, demo_complaints)

        # 4. Seed sample notifications for citizen
        demo_notifications = [
            (
                citizen_id,
                "GS-2026-00003",
                "Complaint Status Updated: In Progress",
                "ఫిర్యాదు స్థితి నవీకరించబడింది: పురోగతిలో ఉంది",
                "शिकायत की स्थिति अपडेट: प्रगति पर है",
                "Your Water Supply complaint #GS-2026-00003 is currently being worked on by the Rural Water Supply team.",
                "మీ నీటి సరఫరా ఫిర్యాదు #GS-2026-00003 పై గ్రామీణ నీటి సరఫరా విభాగం పనిచేస్తోంది.",
                "आपकी जल आपूर्ति शिकायत #GS-2026-00003 पर फील्ड टीम कार्य कर रही है।"
            ),
            (
                citizen_id,
                "GS-2026-00001",
                "Complaint Assigned to Electricity Department",
                "ఫిర్యాదు విద్యుత్ విభాగానికి కేటాయించబడింది",
                "शिकायत बिजली विभाग को सौंपी गई",
                "Streetlight grievance #GS-2026-00001 has been assigned to Electrical Division Officer.",
                "స్ట్రీట్ లైట్ సమస్య #GS-2026-00001 విద్యుత్ విభాగానికి కేటాయించబడింది.",
                "स्ट्रीट लाइट शिकायत #GS-2026-00001 बिजली विभाग अधिकारी को सौंपी गई।"
            )
        ]
        cur.executemany("""
            INSERT INTO notifications (user_id, complaint_id, title_en, title_te, title_hi, message_en, message_te, message_hi)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, demo_notifications)
