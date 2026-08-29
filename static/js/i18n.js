/**
 * GramSetu — Trilingual Translation Matrix
 * Languages: English (en), Telugu (te), Hindi (hi)
 */

const I18N = {
  en: {
    // Brand & Header
    brandName: "GramSetu",
    brandTagline: "One Voice, One Photo, One Connected Village",
    navHome: "Home",
    navReport: "Report a Problem",
    navMap: "Problem Map",
    navMyComplaints: "My Complaints",
    navDashboard: "Dashboard",
    navCitizenLogin: "Citizen Login",
    navAuthorityLogin: "Authority Portal",
    navLogout: "Logout",
    langEn: "English",
    langTe: "తెలుగు (Telugu)",
    langHi: "हिन्दी (Hindi)",

    // Hero Landing
    heroTitle: "Smart Rural Problem-to-Solution Network",
    heroSubtitle: "Report local infrastructure grievances with photo evidence, voice in your mother tongue, and GPS coordinates. Direct routing to administrative authorities.",
    heroReportBtn: "📸 Report a Problem Now",
    heroAuthorityBtn: "🏛️ Authority Portal",
    heroTrackBtn: "🗺️ Explore Problem Map",

    // How It Works
    howItWorksTitle: "How GramSetu Works",
    howStep1Title: "1. Capture & Speak",
    howStep1Desc: "Upload real photo evidence, speak in Telugu/Hindi/English, and auto-detect your exact GPS village location.",
    howStep2Title: "2. AI Classification",
    howStep2Desc: "Smart AI assesses category, determines safety priority, and routes the complaint to the exact nodal department.",
    howStep3Title: "3. Hotspot Mapping",
    howStep3Desc: "Clustering algorithms detect recurring village problems and infrastructure failure hotspots.",
    howStep4Title: "4. Rapid Resolution",
    howStep4Desc: "Authorities inspect, update progress on live timeline, and notify the citizen upon verified resolution.",

    // Citizen Dashboard
    welcomeUser: "Welcome to GramSetu,",
    citizenDashboardTitle: "Citizen Civic Portal",
    quickActionsTitle: "Quick Civic Actions",
    actionReportProblem: "Report a Problem",
    actionReportDesc: "Submit infrastructure grievance with photo & voice",
    actionMyComplaints: "My Grievances",
    actionMyComplaintsDesc: "Track resolution status & progress timeline",
    actionProblemMap: "Live Problem Map",
    actionProblemMapDesc: "View village issues & detected hotspots",
    actionNotifications: "Notifications",
    actionNotificationsDesc: "Real-time updates from government departments",

    // Report Wizard
    reportTitle: "Grievance Redressal Submission",
    reportStep1: "1. Photo Evidence",
    reportStep2: "2. GPS Location",
    reportStep3: "3. Voice & Details",
    reportStep4: "4. AI Review & Submit",

    photoLabel: "Real Photograph of the Problem (Strictly Required)",
    photoCaptureBtn: "📷 Open Live Camera",
    photoUploadBtn: "📁 Upload Photo from Device",
    photoCaptureNotice: "Real photograph evidence is mandatory. Stock/AI images are prohibited and filtered out.",
    noPhotoSelected: "No photo evidence selected yet.",
    photoValid: "✓ Photo evidence validated (Max 5MB).",

    locationTitle: "GPS Village / Locality Location",
    locationDetecting: "Detecting your current GPS location...",
    locationDetected: "📍 GPS Location Detected Successfully",
    locationLat: "Latitude",
    locationLon: "Longitude",
    locationAddress: "Detected Locality / Area",
    locationDenied: "Location permission denied. Please enable location access or pinpoint manually below.",
    locationManualSelect: "Click on the map or search to set coordinates manually:",

    voiceTitle: "Speak Your Problem (Voice Input)",
    voiceSpeakBtn: "🎙️ Click to Speak",
    voiceRecording: "🔴 Listening... Speak clearly in your language",
    voiceStopBtn: "⏹️ Stop Recording",
    voiceTranscriptLabel: "Speech-to-Text Transcript (Review & Edit):",
    descLabel: "Problem Description (Telugu, Hindi, or English):",
    descPlaceholder: "Describe the issue (e.g., Streetlight broken for 2 weeks, water pipe leaking, road pothole)...",
    categoryLabel: "Grievance Category:",
    autoSuggestCategory: "🤖 Click to auto-detect category & priority with AI",

    aiAnalysisTitle: "AI Grievance Analysis (Prototype Model)",
    aiCategory: "Suggested Category",
    aiPriority: "Assessed Priority",
    aiReason: "Priority Justification",
    aiDept: "Assigned Department",
    aiDisclaimer: "AI-assisted classification. Authorities can verify and adjust routing.",

    dailyLimitTitle: "Anti-Spam Daily Quota",
    dailyLimitWarning: "⚠️ Daily complaint limit reached. Each citizen can submit a maximum of ONE complaint per day to ensure genuine civic processing.",
    captchaLabel: "Security Verification Challenge:",
    submitBtn: "🚀 Submit Grievance",
    submittingBtn: "Submitting Grievance...",

    // Categories
    catRoads: "Roads & Bridges",
    catElectricity: "Electricity / Streetlights",
    catWater: "Water Supply & Pipeline",
    catSanitation: "Sanitation / Garbage",
    catTransport: "Public Transport",
    catSchool: "Schools & Education",
    catHealth: "Health Centres / Hospitals",
    catAgri: "Agricultural Infrastructure",
    catOther: "Other Local Issue",

    // Priority
    priorityHigh: "🔴 HIGH PRIORITY",
    priorityMedium: "🟠 MEDIUM PRIORITY",
    priorityLow: "🟢 LOW PRIORITY",

    // Status Timeline
    statusSubmitted: "Submitted",
    statusUnderReview: "Under Review",
    statusAssigned: "Assigned",
    statusInProgress: "In Progress",
    statusResolved: "Resolved",
    statusRejected: "Rejected / Invalid",

    // Map & Hotspots
    mapTitle: "Rural Infrastructure Problem Map",
    mapSubtitle: "Live GPS coordinates of citizen grievances and AI-detected infrastructure failure hotspots.",
    mapFilterCategory: "Filter by Category",
    mapFilterStatus: "Filter by Status",
    allCategories: "All Categories",
    allStatuses: "All Statuses",
    hotspotAlertTitle: "Infrastructure Hotspot Alert",
    repeatedIssueAlertTitle: "Repeated Asset Issue Detected",

    // Authority Portal
    authTitle: "Administrative Command Center",
    authSubtitle: "Official departmental dashboard for grievance inspection, triage, and resolution.",
    statTotal: "Total Complaints",
    statPending: "Pending Review",
    statInProgress: "In Progress",
    statResolved: "Resolved",
    statHighPriority: "High Priority",
    statHotspots: "Active Hotspots",
    tableId: "Complaint ID",
    tableCategory: "Category",
    tableLocation: "Location / Village",
    tablePriority: "Priority",
    tableStatus: "Status",
    tableDate: "Date",
    tableAction: "Action",
    btnInspect: "Inspect Details",

    // Inspector Modal
    inspectorTitle: "Grievance Verification & Resolution Dossier",
    citizenEvidencePhoto: "Citizen-Uploaded Photo Evidence",
    noPhotoEvidence: "No photo evidence submitted.",
    demoDataNotice: "⚠️ DEMO DATA — Not a Citizen Submission (Prototype Reference)",
    voiceTranscriptHeader: "Voice Speech-to-Text Transcript",
    updateStatusLabel: "Update Official Status:",
    resolutionNotesLabel: "Resolution Notes (Mandatory for Resolved):",
    resolutionPlaceholder: "Detail the repair team dispatched, parts replaced, and resolution confirmation...",
    saveChangesBtn: "Save Updates",
    flagSpamBtn: "Flag as Suspicious / Spam",
    unflagSpamBtn: "Mark Verified Citizen Submission",

    // Common
    loading: "Loading...",
    close: "Close",
    cancel: "Cancel",
    confirm: "Confirm",
    save: "Save",
    demoAccountNotice: "Demo accounts available for hackathon prototype testing"
  },

  te: {
    // Brand & Header
    brandName: "గ్రామసేతు",
    brandTagline: "ఒకే స్వరం, ఒకే చిత్రం, ఒకే అనుసంధాన గ్రామం",
    navHome: "హోమ్",
    navReport: "సమస్యను నివేదించండి",
    navMap: "సమస్యల మ్యాప్",
    navMyComplaints: "నా ఫిర్యాదులు",
    navDashboard: "డాష్‌బోర్డ్",
    navCitizenLogin: "పౌరుల లాగిన్",
    navAuthorityLogin: "అధికారుల పోర్టల్",
    navLogout: "లాగౌట్",
    langEn: "English",
    langTe: "తెలుగు (Telugu)",
    langHi: "हिन्दी (Hindi)",

    // Hero Landing
    heroTitle: "స్మార్ట్ గ్రామీణ సమస్య-పరిష్కార నెట్‌వర్క్",
    heroSubtitle: "నిజమైన ఫోటో సాక్ష్యం, మీ మాతృభాషలో వాయిస్ మరియు ఖచ్చితమైన GPS లొకేషన్‌తో స్థానిక సమస్యలను నివేదించండి. సంబంధిత ప్రభుత్వ విభాగానికి ప్రత్యక్ష అనుసంధానం.",
    heroReportBtn: "📸 సమస్యను నివేదించండి",
    heroAuthorityBtn: "🏛️ అధికారుల లాగిన్",
    heroTrackBtn: "🗺️ సమస్యల మ్యాప్‌ని చూడండి",

    // How It Works
    howItWorksTitle: "గ్రామసేతు ఎలా పనిచేస్తుంది",
    howStep1Title: "1. ఫోటో & వాయిస్",
    howStep1Desc: "ఫోటోను అప్‌లోడ్ చేయండి, తెలుగులో మాట్లాడండి మరియు ఖచ్చితమైన GPS స్థానాన్ని గుర్తించండి.",
    howStep2Title: "2. AI వర్గీకరణ",
    howStep2Desc: "AI సాంకేతికత సమస్యను విశ్లేషించి, ప్రాధాన్యతను నిర్ణయించి సరైన విభాగానికి పంపుతుంది.",
    howStep3Title: "3. హాట్‌స్పాట్ గుర్తింపు",
    howStep3Desc: "ఒకే ప్రాంతంలో పదేపదే వచ్చే సమస్యలను గుర్తించి అధికారులను అప్రమత్తం చేస్తుంది.",
    howStep4Title: "4. త్వరిత పరిష్కారం",
    howStep4Desc: "అధికారులు సమస్యను పరిష్కరించి లైవ్ టైమ్‌లైన్‌లో పౌరుడికి సమాచారం అందిస్తారు.",

    // Citizen Dashboard
    welcomeUser: "గ్రామసేతుకు స్వాగతం,",
    citizenDashboardTitle: "పౌర సేవల పోర్టల్",
    quickActionsTitle: "త్వరిత సేవలు",
    actionReportProblem: "సమస్యను నివేదించండి",
    actionReportDesc: "ఫోటో మరియు వాయిస్ ద్వారా కొత్త ఫిర్యాదు చేయండి",
    actionMyComplaints: "నా ఫిర్యాదులు",
    actionMyComplaintsDesc: "ఫిర్యాదు పురోగతి మరియు పరిష్కార స్థితిని చూడండి",
    actionProblemMap: "సమస్యల మ్యాప్",
    actionProblemMapDesc: "గ్రామంలోని సమస్యలు మరియు హాట్‌స్పాట్‌లను చూడండి",
    actionNotifications: "నోటిఫికేషన్‌లు",
    actionNotificationsDesc: "ప్రభుత్వ అధికారుల నుండి ప్రత్యక్ష సమాచారం",

    // Report Wizard
    reportTitle: "గ్రామీణ సమస్య నమోదు పత్రం",
    reportStep1: "1. ఫోటో సాక్ష్యం",
    reportStep2: "2. GPS స్థానం",
    reportStep3: "3. వాయిస్ & వివరాలు",
    reportStep4: "4. AI సమీక్ష & సమర్పణ",

    photoLabel: "సమస్య యొక్క నిజమైన ఫోటో (ఖచ్చితంగా అవసరం)",
    photoCaptureBtn: "📷 కెమెరాతో ఫోటో తీయండి",
    photoUploadBtn: "📁 పరికరం నుండి అప్‌లోడ్ చేయండి",
    photoCaptureNotice: "నిజమైన ఫోటో సాక్ష్యం తప్పనిసరి. ఇంటర్నెట్/నకిలీ ఫోటోలు అనుమతించబడవు.",
    noPhotoSelected: "ఇంకా ఫోటో ఎంచుకోలేదు.",
    photoValid: "✓ ఫోటో సాక్ష్యం నిర్ధారించబడింది (గరిష్టంగా 5MB).",

    locationTitle: "GPS గ్రామ / ప్రాంత స్థానం",
    locationDetecting: "మీ ప్రస్తుత GPS స్థానాన్ని గుర్తిస్తోంది...",
    locationDetected: "📍 GPS స్థానం విజయవంతంగా గుర్తించబడింది",
    locationLat: "అక్షాంశం (Latitude)",
    locationLon: "రేఖాంశం (Longitude)",
    locationAddress: "గుర్తించిన ప్రాంతం / గ్రామం",
    locationDenied: "లొకేషన్ అనుమతి నిరాకరించబడింది. దయచేసి అనుమతిని ప్రారంభించండి లేదా మ్యాప్‌లో ఎంచుకోండి.",
    locationManualSelect: "మ్యాప్‌పై క్లిక్ చేసి స్థానాన్ని ఎంచుకోండి:",

    voiceTitle: "మీ సమస్యను మాట్లాడండి (వాయిస్ నమోదు)",
    voiceSpeakBtn: "🎙️ మాట్లాడటానికి క్లిక్ చేయండి",
    voiceRecording: "🔴 వింటోంది... స్పష్టంగా తెలుగులో మాట్లాడండి",
    voiceStopBtn: "⏹️ రికార్డింగ్ ఆపండి",
    voiceTranscriptLabel: "వాయిస్ టెక్స్ట్ (సరిచూసి సవరించవచ్చు):",
    descLabel: "సమస్య వివరణ (తెలుగు, హిందీ లేదా ఇంగ్లీష్):",
    descPlaceholder: "సమస్యను వివరించండి (ఉదా: మా వీధిలో రెండు వారాలుగా స్ట్రీట్ లైట్ పనిచేయడం లేదు, నీటి పైపు పగిలింది)...",
    categoryLabel: "సమస్య వర్గం:",
    autoSuggestCategory: "🤖 AI ద్వారా వర్గం & ప్రాధాన్యతను స్వయంచాలకంగా గుర్తించండి",

    aiAnalysisTitle: "AI సమస్య విశ్లేషణ (నమూనా మోడల్)",
    aiCategory: "సూచించిన వర్గం",
    aiPriority: "నిర్ణయించిన ప్రాధాన్యత",
    aiReason: "ప్రాధాన్యత కారణం",
    aiDept: "కేటాయించిన విభాగం",
    aiDisclaimer: "AI-సహాయక వర్గీకరణ. అధికారులు అవసరమైతే దీనిని మార్చవచ్చు.",

    dailyLimitTitle: "రోజువారీ సమర్పణ పరిమితి",
    dailyLimitWarning: "⚠️ రోజువారీ ఫిర్యాదు పరిమితి ముగిసింది. ఒక పౌరుడు రోజుకు గరిష్టంగా ఒకే ఫిర్యాదును సమర్పించగలరు.",
    captchaLabel: "భద్రతా ధృవీకరణ పరీక్ష:",
    submitBtn: "🚀 ఫిర్యాదును సమర్పించండి",
    submittingBtn: "సమర్పిస్తోంది...",

    // Categories
    catRoads: "రహదారులు & వంతెనలు",
    catElectricity: "విద్యుత్ / స్ట్రీట్ లైట్లు",
    catWater: "తాగునీటి సరఫరా & పైపులు",
    catSanitation: "పారిశుధ్యం / చెత్త తొలగింపు",
    catTransport: "ప్రజా రవాణా",
    catSchool: "పాఠశాలలు & విద్య",
    catHealth: "ఆరోగ్య కేంద్రాలు / ఆసుపత్రులు",
    catAgri: "వ్యవసాయ మౌలిక సదుపాయాలు",
    catOther: "ఇతర సమస్యలు",

    // Priority
    priorityHigh: "🔴 అత్యధిక ప్రాధాన్యత (HIGH)",
    priorityMedium: "🟠 మధ్యస్థ ప్రాధాన్యత (MEDIUM)",
    priorityLow: "🟢 సాధారణ ప్రాధాన్యత (LOW)",

    // Status Timeline
    statusSubmitted: "సమర్పించబడింది",
    statusUnderReview: "సమీక్షలో ఉంది",
    statusAssigned: "కేటాయించబడింది",
    statusInProgress: "పురోగతిలో ఉంది",
    statusResolved: "పరిష్కరించబడింది",
    statusRejected: "తిరస్కరించబడింది",

    // Map & Hotspots
    mapTitle: "గ్రామీణ సమస్యల ఇంటరాక్టివ్ మ్యాప్",
    mapSubtitle: "పౌరులు సమర్పించిన సమస్యలు మరియు AI గుర్తించిన సమస్యల హాట్‌స్పాట్‌ల లైవ్ మ్యాప్.",
    mapFilterCategory: "వర్గం ప్రకారం వడపోత",
    mapFilterStatus: "స్థితి ప్రకారం వడపోత",
    allCategories: "అన్ని వర్గాలు",
    allStatuses: "అన్ని స్థితులు",
    hotspotAlertTitle: "సమస్యల హాట్‌స్పాట్ హెచ్చరిక",
    repeatedIssueAlertTitle: "పదేపదే వస్తున్న సమస్య గుర్తించబడింది",

    // Authority Portal
    authTitle: "అధికారుల నిర్వహణ పోర్టల్",
    authSubtitle: "ఫిర్యాదుల పరిశీలన, విభాగాల కేటాయింపు మరియు పరిష్కార డాష్‌బోర్డ్.",
    statTotal: "మొత్తం ఫిర్యాదులు",
    statPending: "పరిశీలనలో ఉన్నవి",
    statInProgress: "పురోగతిలో ఉన్నవి",
    statResolved: "పరిష్కరించబడినవి",
    statHighPriority: "అత్యధిక ప్రాధాన్యత",
    statHotspots: "యాక్టివ్ హాట్‌స్పాట్‌లు",
    tableId: "ఫిర్యాదు సంఖ్య",
    tableCategory: "వర్గం",
    tableLocation: "గ్రామం / ప్రాంతం",
    tablePriority: "ప్రాధాన్యత",
    tableStatus: "స్థితి",
    tableDate: "తేదీ",
    tableAction: "చర్య",
    btnInspect: "వివరాలు చూడండి",

    // Inspector Modal
    inspectorTitle: "ఫిర్యాదు పరిశీలన & పరిష్కార పత్రం",
    citizenEvidencePhoto: "పౌరుడు అప్‌లోడ్ చేసిన నిజమైన ఫోటో సాక్ష్యం",
    noPhotoEvidence: "ఫోటో సాక్ష్యం సమర్పించబడలేదు.",
    demoDataNotice: "⚠️ డెమో డేటా — ఇది పౌరుల సమర్పణ కాదు (నమూనా సూచన)",
    voiceTranscriptHeader: "వాయిస్ స్పీచ్-టు-టెక్స్ట్ రికార్డు",
    updateStatusLabel: "అధికారిక స్థితిని మార్చండి:",
    resolutionNotesLabel: "పరిష్కార వివరణ (తప్పనిసరి):",
    resolutionPlaceholder: "తీసుకున్న చర్యలు మరియు పరిష్కార వివరాలను రాయండి...",
    saveChangesBtn: "నవీకరణలను భద్రపరచండి",
    flagSpamBtn: "అనుమానాస్పద / స్పామ్‌గా గుర్తించండి",
    unflagSpamBtn: "నిజమైన పౌర ఫిర్యాదుగా నిర్ధారించండి",

    // Common
    loading: "లోడ్ అవుతోంది...",
    close: "మూసివేయి",
    cancel: "రద్దు",
    confirm: "నిర్ధారించు",
    save: "భద్రపరచు",
    demoAccountNotice: "హ్యాకథాన్ టెస్టింగ్ కోసం డెమో ఖాతాలు అందుబాటులో ఉన్నాయి"
  },

  hi: {
    // Brand & Header
    brandName: "ग्रामसेतु",
    brandTagline: "एक आवाज, एक तस्वीर, एक सशक्त गांव",
    navHome: "होम",
    navReport: "समस्या दर्ज करें",
    navMap: "समस्या मानचित्र",
    navMyComplaints: "मेरी शिकायतें",
    navDashboard: "डैशबोर्ड",
    navCitizenLogin: "नागरिक लॉगिन",
    navAuthorityLogin: "अधिकारी पोर्टल",
    navLogout: "लॉगआउट",
    langEn: "English",
    langTe: "తెలుగు (Telugu)",
    langHi: "हिन्दी (Hindi)",

    // Hero Landing
    heroTitle: "स्मार्ट ग्रामीण समस्या-से-समाधान नेटवर्क",
    heroSubtitle: "फोटो साक्ष्य, अपनी मातृभाषा में आवाज और सटीक जीपीएस लोकेशन के साथ ग्रामीण बुनियादी ढांचे की समस्याओं की रिपोर्ट करें। संबंधित विभाग से सीधा समाधान।",
    heroReportBtn: "📸 समस्या दर्ज करें",
    heroAuthorityBtn: "🏛️ अधिकारी लॉगिन",
    heroTrackBtn: "🗺️ समस्या मैप देखें",

    // How It Works
    howItWorksTitle: "ग्रामसेतु कैसे कार्य करता है",
    howStep1Title: "1. फोटो व आवाज",
    howStep1Desc: "समस्या की वास्तविक तस्वीर लें, हिन्दी में बोलें और सटीक जीपीएस लोकेशन दर्ज करें।",
    howStep2Title: "2. AI वर्गीकरण",
    howStep2Desc: "एआई समस्या का विश्लेषण कर प्राथमिकता तय करता है और सही विभाग को भेजता है।",
    howStep3Title: "3. हॉटस्पॉट मैपिंग",
    howStep3Desc: "एक ही क्षेत्र की बार-बार आने वाली समस्याओं को क्लस्टर कर हॉटस्पॉट के रूप में चिन्हित करता है।",
    howStep4Title: "4. त्वरित समाधान",
    howStep4Desc: "अधिकारी त्वरित कार्रवाई कर लाइव टाइमलाइन अपडेट करते हैं और नागरिक को सूचित किया जाता है।",

    // Citizen Dashboard
    welcomeUser: "ग्रामसेतु में आपका स्वागत है,",
    citizenDashboardTitle: "नागरिक सेवा डैशबोर्ड",
    quickActionsTitle: "त्वरित नागरिक सेवाएं",
    actionReportProblem: "समस्या दर्ज करें",
    actionReportDesc: "फोटो और आवाज के साथ नई शिकायत दर्ज करें",
    actionMyComplaints: "मेरी शिकायतें",
    actionMyComplaintsDesc: "शिकायत समाधान स्थिति और टाइमलाइन ट्रैक करें",
    actionProblemMap: "लाइव समस्या मैप",
    actionProblemMapDesc: "गांव की समस्याएं और सक्रिय हॉटस्पॉट देखें",
    actionNotifications: "सूचनाएं",
    actionNotificationsDesc: "विभागों से प्राप्त लाइव अपडेट",

    // Report Wizard
    reportTitle: "ग्रामीण समस्या निवारण प्रपत्र",
    reportStep1: "1. फोटो प्रमाण",
    reportStep2: "2. जीपीएस स्थान",
    reportStep3: "3. आवाज व विवरण",
    reportStep4: "4. AI समीक्षा व सबमिट",

    photoLabel: "समस्या की वास्तविक तस्वीर (अनिवार्य)",
    photoCaptureBtn: "📷 लाइव कैमरा से फोटो लें",
    photoUploadBtn: "📁 डिवाइस से फोटो अपलोड करें",
    photoCaptureNotice: "वास्तविक फोटो प्रमाण अनिवार्य है। इंटरनेट/फर्जी फोटो स्वीकार नहीं की जाएगी।",
    noPhotoSelected: "कोई फोटो चयनित नहीं है।",
    photoValid: "✓ फोटो प्रमाण मान्य (अधिकतम 5MB)।",

    locationTitle: "जीपीएस ग्राम / क्षेत्र स्थान",
    locationDetecting: "आपके वर्तमान जीपीएस स्थान का पता लगाया जा रहा है...",
    locationDetected: "📍 जीपीएस स्थान सफलतापूर्वक प्राप्त हुआ",
    locationLat: "अक्षांश (Latitude)",
    locationLon: "देशांतर (Longitude)",
    locationAddress: "पता लगाया गया क्षेत्र / गांव",
    locationDenied: "लोकेशन अनुमति अस्वीकृत। कृपया अनुमति चालू करें या नीचे मैप में चुनें।",
    locationManualSelect: "मैप पर क्लिक करके स्थान चुनें:",

    voiceTitle: "अपनी समस्या बोलें (वॉयस इनपुट)",
    voiceSpeakBtn: "🎙️ बोलने के लिए क्लिक करें",
    voiceRecording: "🔴 सुन रहा है... स्पष्ट रूप से हिन्दी में बोलें",
    voiceStopBtn: "⏹️ रिकॉर्डिंग रोकें",
    voiceTranscriptLabel: "वॉयस टेक्स्ट (जांचें और संपादित करें):",
    descLabel: "समस्या का विवरण (हिन्दी, तेलुगु या अंग्रेजी):",
    descPlaceholder: "समस्या का विवरण लिखें (उदा: मुख्य मार्ग पर स्ट्रीट लाइट खराब है, पानी की पाइपलाइन टूट गई है)...",
    categoryLabel: "शिकायत श्रेणी:",
    autoSuggestCategory: "🤖 AI द्वारा श्रेणी और प्राथमिकता का स्वतः पता लगाएं",

    aiAnalysisTitle: "AI शिकायत विश्लेषण (प्रोटोटाइप मॉडल)",
    aiCategory: "अनुशंसित श्रेणी",
    aiPriority: "निर्धारित प्राथमिकता",
    aiReason: "प्राथमिकता का कारण",
    aiDept: "आवंटित विभाग",
    aiDisclaimer: "एआई-सहायक वर्गीकरण। अधिकारी आवश्यकतानुसार इसे संशोधित कर सकते हैं।",

    dailyLimitTitle: "दैनिक शिकायत सीमा",
    dailyLimitWarning: "⚠️ दैनिक शिकायत सीमा पूरी हो गई है। प्रत्येक नागरिक प्रतिदिन अधिकतम 1 शिकायत दर्ज कर सकता है।",
    captchaLabel: "सुरक्षा सत्यापन परीक्षा:",
    submitBtn: "🚀 शिकायत दर्ज करें",
    submittingBtn: "दर्ज की जा रही है...",

    // Categories
    catRoads: "सड़कें एवं पुल",
    catElectricity: "बिजली / स्ट्रीट लाइट",
    catWater: "पेयजल आपूर्ति एवं पाइप",
    catSanitation: "स्वच्छता / कचरा निस्तारण",
    catTransport: "सार्वजनिक परिवहन",
    catSchool: "स्कूल एवं शिक्षा",
    catHealth: "स्वास्थ्य केंद्र / अस्पताल",
    catAgri: "कृषि अवसंरचना",
    catOther: "अन्य स्थानीय समस्या",

    // Priority
    priorityHigh: "🔴 उच्च प्राथमिकता (HIGH)",
    priorityMedium: "🟠 मध्यम प्राथमिकता (MEDIUM)",
    priorityLow: "🟢 सामान्य प्राथमिकता (LOW)",

    // Status Timeline
    statusSubmitted: "दर्ज की गई",
    statusUnderReview: "समीक्षाधीन",
    statusAssigned: "आवंटित",
    statusInProgress: "प्रगति पर",
    statusResolved: "समाधान पूर्ण",
    statusRejected: "अस्वीकृत",

    // Map & Hotspots
    mapTitle: "ग्रामीण समस्या इंटरैक्टिव मैप",
    mapSubtitle: "नागरिकों की शिकायतों और एआई द्वारा पहचाने गए बुनियादी ढांचा हॉटस्पॉट का लाइव मानचित्र।",
    mapFilterCategory: "श्रेणी अनुसार फ़िल्टर",
    mapFilterStatus: "स्थिति अनुसार फ़िल्टर",
    allCategories: "सभी श्रेणियां",
    allStatuses: "सभी स्थितियां",
    hotspotAlertTitle: "इन्फ्रास्ट्रक्चर हॉटस्पॉट चेतावनी",
    repeatedIssueAlertTitle: "बार-बार होने वाली समस्या चिन्हित",

    // Authority Portal
    authTitle: "प्रशासनिक नियंत्रण केंद्र",
    authSubtitle: "शिकायत निरीक्षण, आवंटन और त्वरित समाधान डैशबोर्ड।",
    statTotal: "कुल शिकायतें",
    statPending: "समीक्षा हेतु लंबित",
    statInProgress: "प्रगति पर",
    statResolved: "समाधान पूर्ण",
    statHighPriority: "उच्च प्राथमिकता",
    statHotspots: "सक्रिय हॉटस्पॉट",
    tableId: "शिकायत संख्या",
    tableCategory: "श्रेणी",
    tableLocation: "स्थान / गांव",
    tablePriority: "प्राथमिकता",
    tableStatus: "स्थिति",
    tableDate: "दिनांक",
    tableAction: "कार्रवाई",
    btnInspect: "विवरण देखें",

    // Inspector Modal
    inspectorTitle: "शिकायत निरीक्षण एवं समाधान प्रपत्र",
    citizenEvidencePhoto: "नागरिक द्वारा अपलोड किया गया वास्तविक फोटो साक्ष्य",
    noPhotoEvidence: "कोई फोटो साक्ष्य प्रस्तुत नहीं किया गया।",
    demoDataNotice: "⚠️ डेमो डेटा — यह वास्तविक नागरिक प्रस्तुति नहीं है (प्रोटोटाइप संदर्भ)",
    voiceTranscriptHeader: "वॉयस स्पीच-टू-टेक्स्ट रिकॉर्ड",
    updateStatusLabel: "आधिकारिक स्थिति अपडेट करें:",
    resolutionNotesLabel: "समाधान विवरण (अनिवार्य):",
    resolutionPlaceholder: "मरम्मत और समाधान की विस्तृत पुष्टि लिखें...",
    saveChangesBtn: "अपडेट सहेजें",
    flagSpamBtn: "संदिग्ध / स्पैम के रूप में चिन्हित करें",
    unflagSpamBtn: "सत्यापित नागरिक शिकायत दर्ज करें",

    // Common
    loading: "लोड हो रहा है...",
    close: "बंद करें",
    cancel: "रद्द करें",
    confirm: "पुष्टि करें",
    save: "सहेजें",
    demoAccountNotice: "हैकाथॉन प्रोटोटाइप परीक्षण के लिए डेमो खाते उपलब्ध हैं"
  }
};

let CURRENT_LANG = localStorage.getItem("gramsetu_lang") || "en";

function t(key) {
  if (I18N[CURRENT_LANG] && I18N[CURRENT_LANG][key]) {
    return I18N[CURRENT_LANG][key];
  }
  if (I18N["en"] && I18N["en"][key]) {
    return I18N["en"][key];
  }
  return key;
}

function setLanguage(lang) {
  if (!I18N[lang]) return;
  CURRENT_LANG = lang;
  localStorage.setItem("gramsetu_lang", lang);
  document.documentElement.lang = lang;
  applyTranslations();
  // Fire custom event
  window.dispatchEvent(new CustomEvent("languageChanged", { detail: { lang } }));
}

function applyTranslations() {
  document.querySelectorAll("[data-i18n]").forEach(el => {
    const key = el.getAttribute("data-i18n");
    if (key && I18N[CURRENT_LANG][key]) {
      el.textContent = I18N[CURRENT_LANG][key];
    }
  });

  document.querySelectorAll("[data-i18n-placeholder]").forEach(el => {
    const key = el.getAttribute("data-i18n-placeholder");
    if (key && I18N[CURRENT_LANG][key]) {
      el.setAttribute("placeholder", I18N[CURRENT_LANG][key]);
    }
  });

  document.querySelectorAll("[data-i18n-title]").forEach(el => {
    const key = el.getAttribute("data-i18n-title");
    if (key && I18N[CURRENT_LANG][key]) {
      el.setAttribute("title", I18N[CURRENT_LANG][key]);
    }
  });

  // Update language select buttons active state
  document.querySelectorAll(".lang-btn").forEach(btn => {
    if (btn.getAttribute("data-lang") === CURRENT_LANG) {
      btn.classList.add("active");
    } else {
      btn.classList.remove("active");
    }
  });
}
