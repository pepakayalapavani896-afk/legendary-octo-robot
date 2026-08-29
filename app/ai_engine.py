import re
from typing import Dict, Any

# Multi-lingual keyword maps and heuristics for Telugu, Hindi, English
CATEGORIES_TAXONOMY = {
    "Electricity": {
        "dept": "Electricity Department",
        "keywords": [
            # English
            "electricity", "power", "current", "streetlight", "street light", "light", "transformer", 
            "wire", "spark", "blackout", "pole", "fuse", "voltage", "meter",
            # Telugu
            "స్ట్రీట్ లైట్", "స్ట్రీట్లైట్", "కరెంట్", "విద్యుత్", "వెలుగు", "ట్రాన్స్‌ఫార్మర్", 
            "తీగలు", "స్తంభం", "వోల్టేజ్", "స్పార్క్", "చీకటి", "పవర్", "లైట్లు"
            # Hindi
            "बिजली", "स्ट्रीट लाइट", "लाइट", "करंट", "ट्रांसफार्मर", "तार", "खंभा", "वोल्टेज", "अंधेरा", "पावर"
        ],
        "high_priority_cues": [
            "spark", "fire", "hanging wire", "shock", "fallen pole", "exploded", "danger",
            "తీగ తెగిపడింది", "షాక్", "మంటలు", "ప్రమాదం", "కరెంట్ షాక్", "ట్రాన్స్‌ఫార్మర్ పేలింది",
            "तार टूटा", "शॉर्ट सर्किट", "आग", "खतरा", "करंट लग रहा", "झूलता तार"
        ]
    },
    "Roads": {
        "dept": "Roads & Public Works Department (PWD)",
        "keywords": [
            # English
            "road", "pothole", "potholes", "tar", "concrete", "bridge", "culvert", "divider", "pavement", "crack",
            # Telugu
            "రోడ్డు", "గుంతలు", "గుంత", "రహదారి", "వంతెన", "తారు రోడ్డు", "సిమెంట్ రోడ్డు", "రవాణా మార్గం",
            # Hindi
            "सड़क", "गड्ढा", "गड्ढे", "मार्ग", "पुल", "डामर", "खराब रास्ता", "फुटपाथ"
        ],
        "high_priority_cues": [
            "bridge collapsed", "deep pothole", "accident", "cave-in", "blocked completely", "deadly",
            "వంతెన కూలింది", "పెద్ద గుంత", "ప్రమాదాలు", "రహదారి మూసివేత",
            "पुल धंस गया", "बड़ा गड्ढा", "दुर्घटना", "सड़क धंस गई"
        ]
    },
    "Water Supply": {
        "dept": "Rural Water Supply & Sanitation Department",
        "keywords": [
            # English
            "water", "pipeline", "pipe", "tap", "borewell", "handpump", "drinking water", "tank", "leakage", "contamination",
            # Telugu
            "నీరు", "నీళ్ళు", "తాగునీరు", "పైపు", "పైప్‌లైన్", "నల్లా", "బోరు", "చేతిపంపు", "వాటర్ ట్యాంక్", "లీకేజీ",
            # Hindi
            "पानी", "नल", "पाइप", "बोरवेल", "हैंडपंप", "पेयजल", "टंकी", "लीकेज", "गंदा पानी"
        ],
        "high_priority_cues": [
            "contaminated", "smelly water", "toxic", "burst pipe", "epidemic", "no water 10 days",
            "కలుషిత నీరు", "వాసన", "పైప్ పగిలింది", "రోగాల బారిన",
            "जहरीला पानी", "पाइप फट गया", "गंदा बदबूदार पानी", "बीमारी"
        ]
    },
    "Sanitation": {
        "dept": "Panchayat Sanitation Department",
        "keywords": [
            # English
            "garbage", "drain", "drainage", "trash", "waste", "filth", "mosquito", "smell", "dump", "cleaning", "manhole",
            # Telugu
            "చెత్త", "మురుగు", "కాలువ", "డ్రైనేజీ", "దుర్వాసన", "చెత్తకుండీ", "దోమలు", "పరిశుభ్రత", "మ్యాన్‌హోల్",
            # Hindi
            "कचरा", "कूड़ा", "नाली", "नालियां", "गंदगी", "बदबू", "मच्छर", "मैनहोल", "सफाई"
        ],
        "high_priority_cues": [
            "open manhole", "overflowing sewage", "choked drainage disease", "toxic waste",
            "మ్యాన్‌హోల్ తెరిచి ఉంది", "మురుగు ముంచెత్తుతోంది", "తీవ్రమైన దుర్వాసన",
            "खुला मैनहोल", "गटर का पानी घर में", "गंभीर बीमारी का खतरा"
        ]
    },
    "Public Transport": {
        "dept": "State Transport Department",
        "keywords": [
            # English
            "bus", "transport", "bus stop", "shelter", "auto", "route", "timing", "station",
            # Telugu
            "బస్సు", "రవాణా", "బస్టాప్", "బస్ షెల్టర్", "బస్సు రూటు", "సమయపాలన",
            # Hindi
            "बस", "परिवहन", "बस स्टॉप", "बस स्टैंड", "रूट", "गाड़ी"
        ],
        "high_priority_cues": ["accident prone", "breakdown", "ప్రమాదం", "दुर्घटना"]
    },
    "Schools": {
        "dept": "School Education Department",
        "keywords": [
            # English
            "school", "classroom", "teacher", "blackboard", "bench", "midday meal", "toilet", "student", "playground",
            # Telugu
            "పాఠశాల", "బడి", "తరగతి గది", "ఉపాధ్యాయులు", "మధ్యాహ్న భోజనం", "టాయిలెట్లు", "విద్యార్థులు",
            # Hindi
            "स्कूल", "विद्यालय", "कक्षा", "अध्यापक", "मध्याह्न भोजन", "शौचालय", "छात्र"
        ],
        "high_priority_cues": [
            "roof leaking", "wall collapse risk", "no toilet for girls", "unsafe building",
            "పైకప్పు కూలేలా ఉంది", "బాలికల టాయిలెట్ లేదు",
            "छत टपक रही", "दीवार गिरने का खतरा", "शौचालय नहीं"
        ]
    },
    "Health Centres": {
        "dept": "Health & Family Welfare Department",
        "keywords": [
            # English
            "health", "hospital", "clinic", "doctor", "nurse", "medicine", "phc", "ambulance", "dispensary",
            # Telugu
            "ఆరోగ్య కేంద్రం", "ఆసుపత్రి", "వైద్యుడు", "మందులు", "పీహెచ్‌సీ", "నర్సు", "అంబులెన్స్",
            # Hindi
            "स्वास्थ्य केंद्र", "अस्पताल", "दवाखाना", "डॉक्टर", "दवाइयां", "नर्स", "पीएचसी", "एम्बुलेंस"
        ],
        "high_priority_cues": [
            "emergency", "no doctor", "no antivenom", "critical patient", "outbreak",
            "డాక్టర్ లేరు", "అత్యవసరం", "విష నిరోధక మందు లేదు",
            "डॉक्टर अनुपस्थित", "आपातकालीन", "दवा नहीं"
        ]
    },
    "Agricultural Infrastructure": {
        "dept": "Agriculture & Irrigation Department",
        "keywords": [
            # English
            "agriculture", "crop", "canal", "irrigation", "pump", "farmer", "fertilizer", "mandi", "seed",
            # Telugu
            "వ్యవసాయం", "పంట", "కాలువ", "నీటిపారుదల", "రైతు", "ఎరువులు", "విత్తనాలు", "ధాన్యం",
            # Hindi
            "कृषि", "खेती", "फसल", "नहर", "सिंचाई", "किसान", "खाद", "मंडी", "बीज"
        ],
        "high_priority_cues": [
            "canal breach", "flooded crops", "severe drought", "కాలువ గండి పడింది", "పంట మునిగిపోయింది", "नहर टूट गई"
        ]
    }
}

def analyze_complaint_ai(description: str, voice_transcript: str = "", language: str = "en") -> Dict[str, Any]:
    """
    AI-assisted multi-lingual classification engine.
    Analyzes citizen text / voice transcript in English, Telugu, or Hindi.
    Returns predicted Category, Priority, Priority Reason, Suggested Department, and Summary.
    """
    combined_text = f"{description or ''} {voice_transcript or ''}".strip().lower()
    if not combined_text:
        return {
            "category": "Other",
            "priority": "LOW",
            "priority_reason": "General inquiry / low impact issue",
            "suggested_department": "District Grievance Cell",
            "summary": "General inquiry submitted by citizen.",
            "confidence_score": 0.5,
            "is_ai_assisted": True
        }

    matched_category = "Other"
    max_matches = 0
    suggested_dept = "District Grievance Cell"
    is_high_priority = False
    priority_reason = "Standard civic grievance requiring routine administrative resolution."

    # Score category matching
    for cat_name, cat_data in CATEGORIES_TAXONOMY.items():
        matches = 0
        for kw in cat_data["keywords"]:
            if kw.lower() in combined_text:
                matches += 1
        
        if matches > max_matches:
            max_matches = matches
            matched_category = cat_name
            suggested_dept = cat_data["dept"]

    # Check priority heuristics
    if matched_category in CATEGORIES_TAXONOMY:
        for cue in CATEGORIES_TAXONOMY[matched_category]["high_priority_cues"]:
            if cue.lower() in combined_text:
                is_high_priority = True
                priority_reason = "Potential immediate public safety impact or critical infrastructure failure detected."
                break

    # Additional generic high priority terms across languages
    danger_signals = [
        "danger", "emergency", "fatal", "accident", "spark", "fire", "urgent",
        "ప్రమాదం", "షాక్", "అత్యవసరం", "కూలిపోయింది", "ప్రాణాపాయం",
        "खतरा", "आग", "दुर्घटना", "आपातकालीन", "तुरंत"
    ]
    for sig in danger_signals:
        if sig in combined_text:
            is_high_priority = True
            priority_reason = "High severity cue identified in grievance description."
            break

    if is_high_priority:
        priority = "HIGH"
    elif max_matches > 0:
        priority = "MEDIUM"
        if matched_category == "Electricity":
            priority_reason = "Reported disruption to public lighting / power facility."
        elif matched_category == "Water Supply":
            priority_reason = "Impact on essential drinking water / pipeline supply."
        elif matched_category == "Roads":
            priority_reason = "Disruption to local vehicular or pedestrian transit."
        elif matched_category == "Sanitation":
            priority_reason = "Public health & hygiene maintenance requirement."
        else:
            priority_reason = "Civic facility requires administrative inspection and scheduled repair."
    else:
        priority = "LOW"
        priority_reason = "Routine community maintenance issue with low immediate safety impact."

    # Language tailored summary
    summary = ""
    clean_desc = description.strip() if description else voice_transcript.strip()
    truncated = clean_desc[:120] + ("..." if len(clean_desc) > 120 else "")
    
    if language == "te":
        summary = f"{matched_category} సమస్య: {truncated}"
    elif language == "hi":
        summary = f"{matched_category} समस्या: {truncated}"
    else:
        summary = f"Citizen reported {matched_category.lower()} issue: {truncated}"

    return {
        "category": matched_category,
        "priority": priority,
        "priority_reason": priority_reason,
        "suggested_department": suggested_dept,
        "summary": summary,
        "confidence_score": 0.88 if max_matches > 0 else 0.62,
        "is_ai_assisted": True,
        "disclaimer": "AI-assisted classification (Prototype Model). Authority can adjust priority or department if required."
    }
