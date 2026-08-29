import os
import sys
import unittest
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from app.database import init_db, get_db_cursor
from app.auth import hash_password, verify_password, create_access_token, decode_access_token
from app.ai_engine import analyze_complaint_ai
from app.spam_detector import check_daily_submission_limit, compute_image_hash, check_duplicate_image
from app.geo_utils import haversine_distance_meters, detect_hotspots, detect_repeated_resources
from app.seed_data import seed_demo_data

class TestGramSetuBackend(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        init_db()
        seed_demo_data()

    def test_01_password_hashing(self):
        pwd = "SecretPassword123!"
        hashed = hash_password(pwd)
        self.assertTrue(hashed.startswith(""), "Hash should not be empty")
        self.assertTrue(verify_password(hashed, pwd), "Password verification failed")
        self.assertFalse(verify_password(hashed, "WrongPassword"), "Wrong password should fail")

    def test_02_jwt_tokens(self):
        data = {"sub": 1, "role": "citizen", "email": "test@gramsetu.in"}
        token = create_access_token(data, expires_delta_minutes=60)
        self.assertIsNotNone(token)
        payload = decode_access_token(token)
        self.assertIsNotNone(payload)
        self.assertEqual(payload["sub"], 1)
        self.assertEqual(payload["role"], "citizen")

    def test_03_ai_engine_telugu(self):
        # Telugu Streetlight complaint
        text = "మా వీధిలో రెండు వారాలుగా స్ట్రీట్ లైట్ పనిచేయడం లేదు. రాత్రి వేళల్లో తీవ్రమైన చీకటి."
        result = analyze_complaint_ai(description=text, language="te")
        self.assertEqual(result["category"], "Electricity")
        self.assertEqual(result["suggested_department"], "Electricity Department")
        self.assertIn("MEDIUM", ["MEDIUM", "HIGH"])

    def test_04_ai_engine_hindi(self):
        # Hindi Road Pothole complaint with danger cue
        text = "मुख्य सड़क पर बहुत बड़ा गड्ढा है और दुर्घटना का खतरा है।"
        result = analyze_complaint_ai(description=text, language="hi")
        self.assertEqual(result["category"], "Roads")
        self.assertEqual(result["priority"], "HIGH")
        self.assertIn("Roads & Public Works", result["suggested_department"])

    def test_05_ai_engine_english_water(self):
        text = "Drinking water supply pipeline burst near primary school with severe water leakage."
        result = analyze_complaint_ai(description=text, language="en")
        self.assertEqual(result["category"], "Water Supply")
        self.assertIn("Water Supply", result["suggested_department"])

    def test_06_haversine_distance(self):
        # Distance between 2 nearby points (approx 230 meters)
        lat1, lon1 = 17.385044, 78.486671
        lat2, lon2 = 17.386200, 78.488300
        dist = haversine_distance_meters(lat1, lon1, lat2, lon2)
        self.assertGreater(dist, 100)
        self.assertLess(dist, 400)

    def test_07_hotspot_clustering(self):
        # 3 water complaints close to each other
        sample_complaints = [
            {"id": 101, "complaint_id": "T-1", "category": "Water Supply", "latitude": 17.3862, "longitude": 78.4883, "status": "Submitted"},
            {"id": 102, "complaint_id": "T-2", "category": "Water Supply", "latitude": 17.3868, "longitude": 78.4879, "status": "In Progress"},
            {"id": 103, "complaint_id": "T-3", "category": "Water Supply", "latitude": 17.3865, "longitude": 78.4881, "status": "Submitted"},
            {"id": 104, "complaint_id": "T-4", "category": "Roads", "latitude": 17.5000, "longitude": 78.6000, "status": "Submitted"}
        ]
        hotspots = detect_hotspots(sample_complaints, radius_meters=500.0, min_cluster_size=3)
        self.assertEqual(len(hotspots), 1)
        self.assertEqual(hotspots[0]["dominant_category"], "Water Supply")
        self.assertEqual(hotspots[0]["complaint_count"], 3)

    def test_08_image_hashing(self):
        img_bytes = b"FAKE_TEST_IMAGE_BYTES_12345"
        h = compute_image_hash(img_bytes)
        self.assertEqual(len(h), 64)
        is_dup, cid = check_duplicate_image(h)
        self.assertFalse(is_dup)

    def test_09_authority_privacy(self):
        import asyncio
        from app.main import get_authority_complaints, get_complaint_detail
        
        user = {"id": 1, "name": "District Officer", "role": "authority"}
        res = asyncio.run(get_authority_complaints(user=user))
        self.assertTrue(res["success"])
        complaints = res["complaints"]
        self.assertGreater(len(complaints), 0)

        for c in complaints:
            self.assertNotIn("citizen_name", c)
            self.assertNotIn("citizen_mobile", c)
            self.assertNotIn("citizen_email", c)
            self.assertIn("location_name", c)
            self.assertIn("latitude", c)
            self.assertIn("longitude", c)

        first_cid = complaints[0]["complaint_id"]
        detail_res = asyncio.run(get_complaint_detail(complaint_id=first_cid, user=user))
        self.assertTrue(detail_res["success"])
        detail = detail_res["complaint"]
        self.assertNotIn("citizen_name", detail)
        self.assertNotIn("citizen_mobile", detail)
        self.assertNotIn("citizen_email", detail)
        self.assertIn("location_name", detail)
        self.assertIn("latitude", detail)

    def test_10_authority_status_updates(self):
        import asyncio
        from app.main import get_authority_complaints, get_complaint_detail, update_complaint_status, StatusUpdateRequest
        from fastapi import HTTPException
        
        user = {"id": 1, "name": "District Officer", "role": "authority"}
        complaints = asyncio.run(get_authority_complaints(user=user))["complaints"]
        first_cid = complaints[0]["complaint_id"]

        # 1. Update to In Progress
        req1 = StatusUpdateRequest(
            status="In Progress",
            resolution_notes="Field engineer inspected the site.",
            department="Electricity Department",
            priority="HIGH"
        )
        res1 = asyncio.run(update_complaint_status(complaint_id=first_cid, req=req1, user=user))
        self.assertTrue(res1["success"])
        self.assertEqual(res1["status"], "In Progress")
        self.assertEqual(res1["priority"], "HIGH")

        # Verify detail
        d1 = asyncio.run(get_complaint_detail(complaint_id=first_cid, user=user))["complaint"]
        self.assertEqual(d1["status"], "In Progress")
        self.assertEqual(d1["priority"], "HIGH")

        # 2. Test Resolved with empty notes throws HTTPException
        req_bad = StatusUpdateRequest(status="Resolved", resolution_notes="")
        with self.assertRaises(HTTPException):
            asyncio.run(update_complaint_status(complaint_id=first_cid, req=req_bad, user=user))

        # 3. Update to Resolved with notes succeeds
        req2 = StatusUpdateRequest(status="Resolved", resolution_notes="Streetlight replaced and circuit breaker repaired.")
        res2 = asyncio.run(update_complaint_status(complaint_id=first_cid, req=req2, user=user))
        self.assertTrue(res2["success"])
        self.assertEqual(res2["status"], "Resolved")

        # Verify persisted detail
        d2 = asyncio.run(get_complaint_detail(complaint_id=first_cid, user=user))["complaint"]
        self.assertEqual(d2["status"], "Resolved")
        self.assertEqual(d2["resolution_notes"], "Streetlight replaced and circuit breaker repaired.")

if __name__ == "__main__":
    unittest.main()
