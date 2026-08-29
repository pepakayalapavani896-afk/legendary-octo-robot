import math
import requests
from typing import Dict, Any, List, Optional
from collections import defaultdict

# In-memory reverse geocoding cache to minimize external network requests
GEO_CACHE: Dict[str, Dict[str, Any]] = {}

def haversine_distance_meters(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate the great-circle distance between two points on the Earth in meters."""
    R = 6371000.0  # Earth radius in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2.0) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * \
        math.sin(delta_lambda / 2.0) ** 2
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))

    return R * c

def reverse_geocode_location(lat: float, lon: float) -> Dict[str, str]:
    """
    Reverse geocode real GPS latitude & longitude into village/locality/district.
    Uses OpenStreetMap Nominatim with safe fallback and cache.
    """
    cache_key = f"{round(lat, 4)},{round(lon, 4)}"
    if cache_key in GEO_CACHE:
        return GEO_CACHE[cache_key]

    headers = {
        "User-Agent": "GramSetu-CivicTech-App/1.0 (Smart India Hackathon Prototype)"
    }
    url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}&zoom=18&addressdetails=1"

    try:
        resp = requests.get(url, headers=headers, timeout=3.5)
        if resp.status_code == 200:
            data = resp.json()
            addr = data.get("address", {})
            locality = addr.get("suburb") or addr.get("village") or addr.get("neighbourhood") or \
                       addr.get("hamlet") or addr.get("town") or addr.get("city_district") or \
                       addr.get("county") or "Local Area"
            district = addr.get("state_district") or addr.get("district") or addr.get("city") or ""
            state = addr.get("state", "")
            postcode = addr.get("postcode", "")

            full_display = f"{locality}"
            if district and district != locality:
                full_display += f", {district}"
            if state:
                full_display += f", {state}"
            if postcode:
                full_display += f" ({postcode})"

            result = {
                "locality": locality,
                "district": district,
                "state": state,
                "postcode": postcode,
                "full_address": full_display,
                "source": "OpenStreetMap Real GPS"
            }
            GEO_CACHE[cache_key] = result
            return result
    except Exception:
        pass

    # Fallback to accurate coordinate display if network call times out
    fallback = {
        "locality": f"Coordinates ({round(lat, 4)}° N, {round(lon, 4)}° E)",
        "district": "Detected GPS Area",
        "state": "",
        "postcode": "",
        "full_address": f"GPS Location: {round(lat, 5)}° N, {round(lon, 5)}° E",
        "source": "Direct GPS Coordinates"
    }
    GEO_CACHE[cache_key] = fallback
    return fallback

def detect_hotspots(complaints: List[Dict[str, Any]], radius_meters: float = 500.0, min_cluster_size: int = 3) -> List[Dict[str, Any]]:
    """
    Geospatial Clustering Algorithm:
    Identifies geographic clusters where >= min_cluster_size complaints exist within radius_meters.
    Distinguishes genuine clusters vs single complaints.
    """
    hotspots = []
    visited_ids = set()

    for i, c1 in enumerate(complaints):
        if c1["id"] in visited_ids or c1.get("status") == "Resolved":
            continue

        lat1, lon1 = c1.get("latitude"), c1.get("longitude")
        if lat1 is None or lon1 is None:
            continue

        cluster_members = [c1]
        category_counts = defaultdict(int)
        category_counts[c1["category"]] += 1

        for j, c2 in enumerate(complaints):
            if i == j or c2.get("status") == "Resolved":
                continue
            lat2, lon2 = c2.get("latitude"), c2.get("longitude")
            if lat2 is None or lon2 is None:
                continue

            dist = haversine_distance_meters(lat1, lon1, lat2, lon2)
            if dist <= radius_meters:
                cluster_members.append(c2)
                category_counts[c2["category"]] += 1

        if len(cluster_members) >= min_cluster_size:
            # Dominant category in cluster
            dominant_cat = max(category_counts.items(), key=lambda x: x[1])
            avg_lat = sum(m["latitude"] for m in cluster_members) / len(cluster_members)
            avg_lon = sum(m["longitude"] for m in cluster_members) / len(cluster_members)
            
            for m in cluster_members:
                visited_ids.add(m["id"])

            hotspots.append({
                "hotspot_id": f"HS-{len(hotspots)+1}",
                "latitude": round(avg_lat, 6),
                "longitude": round(avg_lon, 6),
                "radius_meters": radius_meters,
                "complaint_count": len(cluster_members),
                "dominant_category": dominant_cat[0],
                "dominant_category_count": dominant_cat[1],
                "location_name": c1.get("location_name", "Detected Cluster Area"),
                "member_ids": [m["complaint_id"] for m in cluster_members],
                "alert_title": f"🚨 Infrastructure Hotspot Detected: {len(cluster_members)} {dominant_cat[0]} Complaints within {int(radius_meters)}m",
                "recommendation": "Multiple citizens reported recurring local problems in this sector. Prioritize site inspection and root-cause repair."
            })

    return hotspots

def detect_repeated_resources(complaints: List[Dict[str, Any]], distance_threshold: float = 300.0) -> List[Dict[str, Any]]:
    """
    Identifies specific repeated grievances on the exact same resource/asset.
    """
    repeated_groups = []
    seen = set()

    for i, c1 in enumerate(complaints):
        if c1["id"] in seen:
            continue
        lat1, lon1 = c1.get("latitude"), c1.get("longitude")
        cat1 = c1.get("category")
        if lat1 is None or lon1 is None:
            continue

        group = [c1]
        for j, c2 in enumerate(complaints):
            if i == j or c2["id"] in seen:
                continue
            lat2, lon2 = c2.get("latitude"), c2.get("longitude")
            cat2 = c2.get("category")
            if lat2 is None or lon2 is None or cat1 != cat2:
                continue

            dist = haversine_distance_meters(lat1, lon1, lat2, lon2)
            if dist <= distance_threshold:
                group.append(c2)

        if len(group) >= 2:
            for g in group:
                seen.add(g["id"])
            repeated_groups.append({
                "category": cat1,
                "location_name": c1.get("location_name", "Local Area"),
                "count": len(group),
                "complaint_ids": [g["complaint_id"] for g in group],
                "message": f"🚨 REPEATED ISSUE DETECTED: {len(group)} reports concerning {cat1} within {int(distance_threshold)}m of {c1.get('location_name', 'this location')}. Consider prioritizing inspection."
            })

    return repeated_groups
