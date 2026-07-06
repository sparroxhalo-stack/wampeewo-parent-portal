import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import requests
import base64
import os
import time
import random
from datetime import datetime

# ---------------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------------
st.set_page_config(page_title="Wampeewo Ntakke — Parent Portal", page_icon="🛡️", layout="wide")

NAVY        = "#06264D"
BLUE        = "#0B4F9E"
SKY         = "#EAF3FC"
BG          = "#F4F6F9"
CRIMSON     = "#C8102E"
CRIMSON_DARK= "#8C0B20"
GOLD        = "#D7A33D"
INK         = "#10182B"
SLATE       = "#5B6B82"
WHITE       = "#FFFFFF"
GREEN       = "#1FAF54"

LOGO_PATH = "logo.png"

def get_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

logo_b64 = get_base64(LOGO_PATH)

# ---------------------------------------------------------------
# STYLES
# ---------------------------------------------------------------
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap');
html,body,[class*="css"]{{font-family:'Inter',sans-serif;}}
h1,h2,h3,h4{{font-family:'Poppins',sans-serif;}}
.stApp{{background-color:{BG};}}
#MainMenu{{visibility:hidden;}} footer{{visibility:hidden;}}
.block-container{{padding-bottom:100px!important;padding-top:1.2rem!important;max-width:720px;}}

/* Top bar */
.topbar{{display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;}}
.topbar .brand{{display:flex;align-items:center;gap:10px;}}
.topbar .brand img{{width:38px;height:38px;border-radius:50%;object-fit:contain;background:white;padding:2px;box-shadow:0 2px 8px rgba(0,0,0,.12);}}
.topbar .brand .fallback{{width:38px;height:38px;border-radius:50%;background:{NAVY};color:white;font-size:9px;font-weight:800;display:flex;align-items:center;justify-content:center;}}
.topbar .brand .name{{font-family:'Poppins',sans-serif;font-weight:800;font-size:15px;color:{NAVY};line-height:1.1;}}
.topbar .brand .tag{{font-size:10.5px;color:{SLATE};}}
.bell-wrap{{position:relative;}}
.bell-badge{{position:absolute;top:-6px;right:-6px;background:{GREEN};color:white;border-radius:50%;font-size:10px;font-weight:800;width:18px;height:18px;display:flex;align-items:center;justify-content:center;}}

/* Hero banner */
.hero-banner{{
    background:linear-gradient(135deg,{NAVY} 0%,{BLUE} 100%);
    border-radius:18px;padding:28px 24px;margin-bottom:14px;color:white;
    display:flex;align-items:center;gap:18px;position:relative;overflow:hidden;
    box-shadow:0 10px 30px rgba(6,38,77,.25);
}}
.hero-banner::after{{content:"";position:absolute;right:-40px;top:-40px;width:180px;height:180px;border-radius:50%;background:rgba(255,255,255,.06);}}
.hero-banner img{{width:70px;height:70px;border-radius:50%;background:white;padding:4px;object-fit:contain;box-shadow:0 4px 14px rgba(0,0,0,.25);position:relative;z-index:1;flex-shrink:0;}}
.hero-banner .fallback-badge{{width:70px;height:70px;border-radius:50%;background:rgba(255,255,255,.15);display:flex;align-items:center;justify-content:center;font-weight:800;font-size:11px;color:white;flex-shrink:0;}}
.hero-text{{position:relative;z-index:1;}}
.hero-text h2{{margin:0;font-size:19px;font-weight:800;}}
.hero-text .sub{{color:rgba(255,255,255,.75);font-size:12px;margin-top:3px;}}
.hero-text .motto{{color:{GOLD};font-style:italic;font-weight:600;font-size:12.5px;margin-top:2px;}}

/* Grid */
.grid-card{{background:white;border-radius:18px;padding:18px 14px 8px 14px;margin-bottom:14px;box-shadow:0 2px 12px rgba(15,30,51,.06);border:1px solid #ECEFF3;}}
.grid-item{{text-align:center;padding:8px 2px 14px 2px;}}
.grid-item .ic{{width:50px;height:50px;border-radius:14px;margin:0 auto 8px auto;display:flex;align-items:center;justify-content:center;font-size:22px;}}
.grid-item .lbl{{font-size:11.5px;font-weight:600;color:{INK};line-height:1.25;}}

/* Cards */
.card{{background:white;border-radius:16px;padding:18px 20px;box-shadow:0 2px 10px rgba(15,30,51,.06);border:1px solid #ECEFF3;margin-bottom:12px;}}
.acct-card{{background:white;border-radius:18px;padding:18px 20px;margin-bottom:14px;box-shadow:0 2px 12px rgba(15,30,51,.06);border:1px solid #ECEFF3;}}
.stat-line{{font-size:12px;color:{SLATE};}}
.stat-big{{font-family:'Poppins',sans-serif;font-weight:800;font-size:18px;}}
.warn{{color:{CRIMSON};font-weight:700;font-size:11.5px;}}
.section-label{{font-family:'Poppins',sans-serif;font-weight:700;font-size:12px;text-transform:uppercase;letter-spacing:.08em;color:{SLATE};margin:4px 0 10px 0;}}

/* Notices */
.notice-card{{background:white;border-radius:14px;padding:16px 18px;margin-bottom:10px;border-left:5px solid {BLUE};box-shadow:0 2px 10px rgba(15,30,51,.05);}}
.notice-card.emergency{{border-left-color:{CRIMSON};background:#FDF2F3;}}
.notice-card.fees{{border-left-color:{GOLD};}}
.notice-card.exam{{border-left-color:{NAVY};}}
.notice-card.event{{border-left-color:#2E86C1;}}
.pill{{display:inline-block;padding:3px 11px;border-radius:999px;font-size:10.5px;font-weight:700;text-transform:uppercase;letter-spacing:.05em;}}
.pill-emergency{{background:{CRIMSON};color:white;}}
.pill-meeting{{background:{BLUE};color:white;}}
.pill-exam{{background:{NAVY};color:white;}}
.pill-fees{{background:{GOLD};color:#3a2a05;}}
.pill-event{{background:#2E86C1;color:white;}}
.notice-title{{font-weight:700;color:{INK};margin:8px 0 4px 0;font-size:15px;}}

/* Story strip */
.story-strip{{display:flex;gap:14px;padding:4px 2px 10px 2px;overflow-x:auto;}}
.story-circle{{width:64px;height:64px;border-radius:50%;flex-shrink:0;display:flex;align-items:center;justify-content:center;font-size:24px;border:3px solid {GOLD};}}
.story-label{{font-size:10.5px;text-align:center;color:{INK};font-weight:600;margin-top:5px;width:70px;}}

/* Dark banner */
.dark-banner{{background:{NAVY};color:white;border-radius:14px;padding:14px 18px;display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;font-weight:600;font-size:13.5px;}}

/* Achievement card */
.ach-card{{background:white;border-radius:16px;padding:18px;margin-bottom:12px;border:1px solid #ECEFF3;box-shadow:0 2px 10px rgba(15,30,51,.06);display:flex;gap:14px;align-items:flex-start;}}
.ach-icon{{font-size:22px;width:46px;height:46px;border-radius:12px;flex-shrink:0;display:flex;align-items:center;justify-content:center;}}

/* Bottom nav — TikTok style */
div[data-testid="stVerticalBlockBorderWrapper"]:has(div.navmarker){{
    position:fixed;bottom:0;left:0;right:0;z-index:999;
    background:#111;
    padding:0 0 calc(env(safe-area-inset-bottom)) 0;
    max-width:720px;margin:0 auto;border:none!important;
    box-shadow:0 -1px 0 rgba(255,255,255,.08);
}}
div[data-testid="stVerticalBlockBorderWrapper"]:has(div.navmarker)>div{{border:none!important;background:transparent!important;}}
.navmarker{{display:none;}}

/* Override every button inside the nav */
div[data-testid="stVerticalBlockBorderWrapper"]:has(div.navmarker) button{{
    background:transparent!important;border:none!important;box-shadow:none!important;
    color:rgba(255,255,255,.55)!important;font-size:10px!important;font-weight:600!important;
    padding:10px 4px 8px 4px!important;border-radius:0!important;
    display:flex!important;flex-direction:column!important;align-items:center!important;
    gap:3px!important;width:100%!important;letter-spacing:.01em;
}}
div[data-testid="stVerticalBlockBorderWrapper"]:has(div.navmarker) button:hover{{
    color:white!important;background:transparent!important;
}}
/* Active nav item — white + underline */
div[data-testid="stVerticalBlockBorderWrapper"]:has(div.navmarker) button[kind="primary"]{{
    color:white!important;border-bottom:2px solid white!important;
}}
/* Center Pay button */
div[data-testid="stVerticalBlockBorderWrapper"]:has(div.navmarker) button.pay-center{{
    background:linear-gradient(135deg,{BLUE},{CRIMSON})!important;
    border-radius:14px!important;width:54px!important;height:40px!important;
    color:white!important;font-size:22px!important;padding:0!important;
    box-shadow:0 4px 18px rgba(11,79,158,.5)!important;
}}
.stButton button{{border-radius:10px;font-weight:600;}}
[data-testid="stChatMessage"]{{background:white;border-radius:14px;border:1px solid #ECEFF3;box-shadow:0 2px 8px rgba(15,30,51,.05);}}

/* ---- Splash ---- */
@keyframes fadeUp{{from{{opacity:0;transform:translateY(14px);}}to{{opacity:1;transform:translateY(0);}}}}
@keyframes logoPulse{{0%{{transform:scale(0.8);opacity:0;}}60%{{transform:scale(1.05);opacity:1;}}100%{{transform:scale(1);opacity:1;}}}}
@keyframes loadFill{{from{{width:0%;}}to{{width:100%;}}}}
@keyframes dotFade{{0%,100%{{opacity:0;}}50%{{opacity:1;}}}}
@keyframes fadeIn{{from{{opacity:0;}}to{{opacity:1;}}}}

.splash-wrap{{
    background:radial-gradient(circle at 30% 20%,{BLUE} 0%,{NAVY} 55%,#02152e 100%);
    border-radius:22px;padding:60px 32px 50px 32px;text-align:center;
    animation:fadeUp 0.5s ease-out;
    box-shadow:0 16px 40px rgba(6,38,77,.35);
}}
.splash-wrap img{{
    width:120px;height:120px;border-radius:50%;background:white;padding:6px;
    object-fit:contain;box-shadow:0 8px 28px rgba(0,0,0,.35);margin-bottom:22px;
    animation:logoPulse 1.1s ease-out;
}}
.splash-fallback-logo{{
    width:120px;height:120px;border-radius:50%;background:rgba(255,255,255,.12);
    border:3px solid rgba(255,255,255,.3);display:flex;align-items:center;justify-content:center;
    font-weight:800;color:white;font-size:14px;margin:0 auto 22px auto;
    animation:logoPulse 1.1s ease-out;
}}
.splash-wrap h1{{color:white;font-size:23px;font-weight:800;margin:0;letter-spacing:-.01em;animation:fadeIn 1s ease-out .4s both;}}
.splash-wrap .splash-motto{{color:{GOLD};font-style:italic;font-weight:600;font-size:14px;margin:8px 0 0 0;animation:fadeIn 1s ease-out .6s both;}}
.splash-wrap .splash-location{{color:rgba(255,255,255,.6);font-size:11.5px;margin:5px 0 0 0;animation:fadeIn 1s ease-out .8s both;}}
.splash-wrap .splash-tag{{color:rgba(255,255,255,.65);font-size:11.5px;margin:24px 0 14px 0;text-transform:uppercase;letter-spacing:.14em;font-weight:700;animation:fadeIn 1s ease-out 1s both;}}
.loading-bar-track{{width:200px;height:4px;background:rgba(255,255,255,.15);border-radius:4px;margin:20px auto 8px auto;overflow:hidden;animation:fadeIn 1s ease-out 1s both;}}
.loading-bar-fill{{height:100%;width:0%;background:linear-gradient(90deg,{GOLD},{CRIMSON});border-radius:4px;animation:loadFill 4.6s cubic-bezier(.4,0,.2,1) forwards;}}
.loading-text{{color:rgba(255,255,255,.5);font-size:10.5px;letter-spacing:.06em;animation:fadeIn 1s ease-out 1s both;}}
.loading-text span{{animation:dotFade 1.4s infinite;opacity:0;}}
.loading-text span:nth-child(1){{animation-delay:0s;}}
.loading-text span:nth-child(2){{animation-delay:.25s;}}
.loading-text span:nth-child(3){{animation-delay:.5s;}}

/* Quick stats row */
.stat-row{{display:flex;gap:10px;margin-bottom:14px;}}
.stat-mini{{background:white;border-radius:14px;flex:1;padding:14px 12px;box-shadow:0 2px 10px rgba(15,30,51,.06);border:1px solid #ECEFF3;text-align:center;}}
.stat-mini .val{{font-family:'Poppins',sans-serif;font-size:18px;font-weight:800;color:{NAVY};}}
.stat-mini .lab{{font-size:10px;color:{SLATE};font-weight:600;text-transform:uppercase;letter-spacing:.04em;}}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------
# SCHOOL DATA
# ---------------------------------------------------------------
SCHOOL = {
    "name": "Wampeewo Ntakke SS",
    "full_name": "Wampeewo Ntakke Secondary School",
    "motto": "Ekula Y'ebuuka",
    "founded": 1966,
    "location": "Gayaza Road, Wakiso, Uganda",
}

STUDENTS = [
    {"name": "Mawanda Ronald", "klass": "S4 Science", "class_level": "S4", "stream": "Science",
     "admission_no": "WNSS/2023/0417", "payment_code": "WN-0417",
     "guardian": "Mr. Mawanda Joseph", "guardian_phone": "+256 700 501 001", "attendance_pct": 96,
     "fees_billed": 850000, "fees_paid": 600000, "rank": 6, "out_of": 42,
     "subjects": [("Mathematics", 61, 74), ("Biology", 70, 78), ("Chemistry", 55, 63),
                  ("Physics", 58, 60), ("English", 72, 80), ("Geography", 66, 71)]},
    {"name": "Ssekyondwa Simon", "klass": "S2 East", "class_level": "S2", "stream": "East",
     "admission_no": "WNSS/2024/0182", "payment_code": "WN-0182",
     "guardian": "Mrs. Ssekyondwa Grace", "guardian_phone": "+256 752 220 884", "attendance_pct": 89,
     "fees_billed": 620000, "fees_paid": 620000, "rank": 5, "out_of": 38,
     "subjects": [("Mathematics", 68, 75), ("Biology", 60, 64), ("English", 62, 70),
                  ("History", 70, 74), ("CRE", 80, 84)]},
    {"name": "Wampona Kenneth", "klass": "S6 Arts", "class_level": "S6", "stream": "Arts",
     "admission_no": "WNSS/2021/0099", "payment_code": "WN-0099",
     "guardian": "Mr. Wampona Charles", "guardian_phone": "+256 772 901 233", "attendance_pct": 98,
     "fees_billed": 950000, "fees_paid": 950000, "rank": 2, "out_of": 30,
     "subjects": [("Economics", 78, 85), ("Literature", 81, 88), ("Geography", 75, 79),
                  ("CRE", 80, 83)]},
    {"name": "Nakayima Brenda", "klass": "S1 West", "class_level": "S1", "stream": "West",
     "admission_no": "WNSS/2026/0301", "payment_code": "WN-0301",
     "guardian": "Mrs. Nakayima Rose", "guardian_phone": "+256 701 887 410", "attendance_pct": 92,
     "fees_billed": 540000, "fees_paid": 270000, "rank": 9, "out_of": 45,
     "subjects": [("Mathematics", 50, 54), ("Science", 58, 61), ("English", 60, 65),
                  ("Social Studies", 66, 70)]},
]
STUDENTS_DF = pd.DataFrame(STUDENTS)

NOTICES = [
    {"id": 1, "category": "emergency", "time": "Today, 7:05 AM",
     "title": "School closed Friday — heavy rain flooding",
     "body": "Due to flooding along Gayaza Road, the school will remain closed this Friday, 26 June. "
             "Day scholars should not report. Boarding students remain on campus as normal. "
             "Updates will follow by Sunday evening. Please keep your child home."},
    {"id": 2, "category": "meeting", "time": "Yesterday, 4:30 PM",
     "title": "S4 Parents' Meeting — Friday 2:00 PM",
     "body": "All parents and guardians of S4 students are invited to a meeting in the main hall "
             "this Friday at 2:00 PM to discuss UCE registration and mock exam performance."},
    {"id": 3, "category": "exam", "time": "Mon, 22 Jun",
     "title": "End of Term 2 exams begin 7 July",
     "body": "End of Term 2 examinations begin Monday 7 July and run for two weeks. Timetables "
             "are posted on the noticeboard and available from class teachers."},
    {"id": 4, "category": "fees", "time": "Fri, 19 Jun",
     "title": "Term 2 balance deadline — 30 June",
     "body": "All outstanding Term 2 fee balances should be cleared by 30 June to allow students "
             "to sit end of term examinations without disruption."},
    {"id": 5, "category": "event", "time": "Wed, 17 Jun",
     "title": "Inter-house sports day — 12 July",
     "body": "The annual inter-house sports day will be held on 12 July from 8:30 AM. "
             "Parents and guardians are warmly welcome to attend."},
]

EVENTS = [
    {"date": "26 Jun", "month": "JUN", "label": "School closed — flooding (day scholars)", "tag": "emergency"},
    {"date": "27 Jun", "month": "JUN", "label": "Visiting Sunday", "tag": "event"},
    {"date": "30 Jun", "month": "JUN", "label": "Fees deadline — Term 2 balance", "tag": "fees"},
    {"date": "7 Jul",  "month": "JUL", "label": "End of Term 2 examinations begin", "tag": "exam"},
    {"date": "12 Jul", "month": "JUL", "label": "Inter-house sports day", "tag": "event"},
    {"date": "26 Jul", "month": "JUL", "label": "Term 2 closing day", "tag": "meeting"},
]

HIGHLIGHTS = [
    {"id": 1, "title": "UCE Results",  "emoji": "📚", "c1": BLUE,    "c2": NAVY,         "image": "highlight_1.jpg",
     "detail": "96% UCE pass rate in 2025 — the school's strongest results in five years, with 12 students attaining first grade."},
    {"id": 2, "title": "Sports Day",   "emoji": "🥇", "c1": CRIMSON, "c2": CRIMSON_DARK, "image": "highlight_2.jpg",
     "detail": "Wakiso District inter-school athletics champions for the second year running."},
    {"id": 3, "title": "STEM Fair",    "emoji": "🔬", "c1": "#2E86C1","c2": "#1B4F72",   "image": "highlight_3.jpg",
     "detail": "Named Best STEM School, Wakiso District 2025, for the STEM club's mosquito-trap innovation."},
    {"id": 4, "title": "Cultural Day", "emoji": "🎭", "c1": GOLD,    "c2": "#8C6510",    "image": "highlight_4.jpg",
     "detail": "First place, Buganda regional cultural dance competition."},
    {"id": 5, "title": "Graduation",   "emoji": "🎓", "c1": NAVY,    "c2": "#02152e",    "image": "highlight_5.jpg",
     "detail": "Annual thanksgiving and graduation service for S6 leavers, June 2026."},
]

THREADS_SEED = [
    {"id": 1, "with": "Mrs. Nakimera — Class Teacher", "messages": [
        {"from": "teacher", "text": "Good morning. Mawanda did well in today's Chemistry quiz — 14/20.", "time": "10:40 AM"},
        {"from": "parent",  "text": "Thank you Madam, we will keep encouraging the revision at home.", "time": "10:42 AM"},
    ]},
    {"id": 2, "with": "Bursar's Office", "messages": [
        {"from": "teacher", "text": "Reminder: Term 2 balance is due by 30 June.", "time": "Yesterday"},
    ]},
    {"id": 3, "with": "S4 Science — Class Group", "group": True, "messages": [
        {"from": "teacher", "text": "All S4 parents: Friday's meeting starts promptly at 2:00 PM in the main hall.", "time": "Mon"},
    ]},
]

PAYMENT_HISTORY_SEED = [
    {"date": "14 May 2026", "method": "MTN Mobile Money", "amount": 300000, "ref": "MM240514.0091"},
    {"date": "02 Apr 2026", "method": "Bank deposit",     "amount": 300000, "ref": "CB-220409-77"},
]

# ---------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------
def ask_claude(system_prompt, user_text):
    api_key = st.secrets.get("ANTHROPIC_API_KEY")
    if not api_key:
        return "⚠️ Add ANTHROPIC_API_KEY to Streamlit secrets to enable AI features."
    try:
        r = requests.post("https://api.anthropic.com/v1/messages",
            headers={"x-api-key": api_key, "anthropic-version": "2023-06-01",
                     "content-type": "application/json"},
            json={"model": "claude-sonnet-4-6", "max_tokens": 600,
                  "system": system_prompt,
                  "messages": [{"role": "user", "content": user_text}]},
            timeout=30)
        r.raise_for_status()
        return "".join(b.get("text","") for b in r.json().get("content",[])).strip() or "No response."
    except Exception as e:
        return f"⚠️ AI error: {e}"

def money(n):
    return f"UGX {n:,.0f}"

# ---------------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------------
defaults = {
    "entered": False, "nav": "home",
    "student": None,  "chat": [],
    "read_ids": set(), "toasted": False,
    "threads": None,  "active_thread": None,
    "open_hl": None,  "paid_extra": {},
    "_last_receipt": None,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v
if st.session_state.threads is None:
    st.session_state.threads = [dict(t, messages=list(t["messages"])) for t in THREADS_SEED]

# ---------------------------------------------------------------
# SPLASH — 5 seconds, automatic, no button
# ---------------------------------------------------------------
if not st.session_state.entered:
    splash_logo = (f'<img src="data:image/png;base64,{logo_b64}" />' if logo_b64 else
                   '<div class="splash-fallback-logo">WNSS</div>')
    st.markdown(f"""
    <div class="splash-wrap">
        {splash_logo}
        <h1>{SCHOOL['full_name']}</h1>
        <p class="splash-motto">"{SCHOOL['motto']}"</p>
        <p class="splash-location">📍 {SCHOOL['location']} &nbsp;·&nbsp; Est. {SCHOOL['founded']}</p>
        <p class="splash-tag">Parent Portal</p>
        <div class="loading-bar-track"><div class="loading-bar-fill"></div></div>
        <p class="loading-text">LOADING<span>.</span><span>.</span><span>.</span></p>
    </div>
    """, unsafe_allow_html=True)
    time.sleep(5)
    st.session_state.entered = True
    st.rerun()

# ---------------------------------------------------------------
# TOP BAR
# ---------------------------------------------------------------
unread = len([n for n in NOTICES if n["id"] not in st.session_state.read_ids])
brand_logo_html = (f'<img src="data:image/png;base64,{logo_b64}" />' if logo_b64
                   else '<div class="fallback">WNSS</div>')
st.markdown(f"""
<div class="topbar">
    <div class="brand">
        {brand_logo_html}
        <div>
            <div class="name">{SCHOOL['name']}</div>
            <div class="tag">Parent Portal</div>
        </div>
    </div>
    <div class="bell-wrap">
        <span style="font-size:22px;cursor:pointer;">🔔</span>
        {f'<span class="bell-badge">{unread}</span>' if unread else ''}
    </div>
</div>
""", unsafe_allow_html=True)

# toast once per session
if not st.session_state.toasted:
    urgent = next((n for n in NOTICES if n["category"] == "emergency"), None)
    if urgent:
        st.toast(f"🚨 {urgent['title']}", icon="🔔")
    st.session_state.toasted = True

# ---------------------------------------------------------------
# STUDENT HELPERS
# ---------------------------------------------------------------
s = st.session_state.student
def fees_balance(rec):
    extra = st.session_state.paid_extra.get(rec["admission_no"], 0)
    return max(rec["fees_billed"] - rec["fees_paid"] - extra, 0)

# =================================================================
# PAGE: HOME — school dashboard, no student gate
# =================================================================
def page_home():
    # Hero banner
    badge_tag = (f'<img src="data:image/png;base64,{logo_b64}" />' if logo_b64
                 else '<div class="fallback-badge">WNSS</div>')
    st.markdown(f"""
    <div class="hero-banner">
        {badge_tag}
        <div class="hero-text">
            <h2>{SCHOOL['full_name']}</h2>
            <p class="motto">"{SCHOOL['motto']}"</p>
            <p class="sub">📍 {SCHOOL['location']} &nbsp;·&nbsp; Est. {SCHOOL['founded']}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # School quick stats
    st.markdown('<div class="stat-row">'
        f'<div class="stat-mini"><div class="val">1,200+</div><div class="lab">Students</div></div>'
        f'<div class="stat-mini"><div class="val">96%</div><div class="lab">UCE Pass Rate</div></div>'
        f'<div class="stat-mini"><div class="val">60+</div><div class="lab">Teachers</div></div>'
        f'<div class="stat-mini"><div class="val">1966</div><div class="lab">Founded</div></div>'
        '</div>', unsafe_allow_html=True)

    # ---- Sliding highlights carousel ----
    slides_html = ""
    for h in HIGHLIGHTS:
        img_b64_h = get_base64(h["image"])
        if img_b64_h:
            bg = f'background:url("data:image/jpeg;base64,{img_b64_h}") center/cover no-repeat;'
            overlay = "background:linear-gradient(to top,rgba(0,0,0,.75) 0%,rgba(0,0,0,.1) 60%);"
        else:
            bg = f"background:linear-gradient(135deg,{h['c1']},{h['c2']});"
            overlay = "background:rgba(0,0,0,.25);"
        slides_html += f"""
        <div class="slide" style="{bg}">
            <div class="overlay" style="{overlay}">
                <div class="slide-emoji">{h['emoji']}</div>
                <div class="slide-title">{h['title']}</div>
                <div class="slide-body">{h['detail']}</div>
            </div>
        </div>"""

    carousel_html = f"""
    <!DOCTYPE html><html><head>
    <style>
      *{{box-sizing:border-box;margin:0;padding:0;font-family:'Inter',sans-serif;}}
      body{{background:transparent;overflow:hidden;}}
      .carousel{{position:relative;width:100%;height:200px;border-radius:18px;overflow:hidden;}}
      .track{{display:flex;height:100%;transition:transform .5s cubic-bezier(.4,0,.2,1);}}
      .slide{{min-width:100%;height:200px;border-radius:18px;flex-shrink:0;position:relative;}}
      .overlay{{position:absolute;inset:0;border-radius:18px;display:flex;flex-direction:column;
               justify-content:flex-end;padding:18px 20px;}}
      .slide-emoji{{font-size:26px;margin-bottom:4px;}}
      .slide-title{{color:white;font-weight:800;font-size:17px;letter-spacing:-.01em;text-shadow:0 1px 6px rgba(0,0,0,.4);}}
      .slide-body{{color:rgba(255,255,255,.85);font-size:11.5px;margin-top:3px;line-height:1.45;
                  display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;}}
      .dots{{position:absolute;bottom:10px;right:14px;display:flex;gap:5px;}}
      .dot{{width:6px;height:6px;border-radius:50%;background:rgba(255,255,255,.4);transition:all .3s;cursor:pointer;}}
      .dot.active{{background:white;width:18px;border-radius:3px;}}
      .arrow{{position:absolute;top:50%;transform:translateY(-50%);
              background:rgba(0,0,0,.35);border:none;border-radius:50%;
              width:32px;height:32px;color:white;font-size:15px;cursor:pointer;
              display:flex;align-items:center;justify-content:center;backdrop-filter:blur(4px);}}
      .arrow-l{{left:10px;}} .arrow-r{{right:10px;}}
      .progress{{position:absolute;top:0;left:0;height:3px;background:rgba(255,255,255,.9);
                 border-radius:2px;transition:width .1s linear;}}
    </style></head><body>
    <div class="carousel" id="car">
      <div class="track" id="track">{slides_html}</div>
      <div class="progress" id="prog"></div>
      <button class="arrow arrow-l" onclick="prev()">&#8249;</button>
      <button class="arrow arrow-r" onclick="next()">&#8250;</button>
      <div class="dots" id="dots"></div>
    </div>
    <script>
      const n={len(HIGHLIGHTS)}, dur=3800;
      let cur=0, timer, elapsed=0, raf;
      const track=document.getElementById('track');
      const prog=document.getElementById('prog');
      const dotsEl=document.getElementById('dots');
      // build dots
      for(let i=0;i<n;i++){{
        const d=document.createElement('div');
        d.className='dot'+(i===0?' active':'');
        d.onclick=()=>go(i); dotsEl.appendChild(d);
      }}
      function updateDots(){{
        document.querySelectorAll('.dot').forEach((d,i)=>d.className='dot'+(i===cur?' active':''));
      }}
      function go(i){{cur=i;track.style.transform=`translateX(-${{cur*100}}%)`;updateDots();resetTimer();}}
      function next(){{go((cur+1)%n);}}
      function prev(){{go((cur-1+n)%n);}}
      function resetTimer(){{
        clearInterval(timer);cancelAnimationFrame(raf);elapsed=0;prog.style.width='0%';
        let last=performance.now();
        function tick(now){{
          elapsed+=now-last;last=now;
          prog.style.width=Math.min(elapsed/dur*100,100)+'%';
          if(elapsed>=dur){{next();return;}}
          raf=requestAnimationFrame(tick);
        }}
        raf=requestAnimationFrame(tick);
      }}
      resetTimer();
    </script></body></html>"""
    components.html(carousel_html, height=210)

    # AI daily briefing
    st.markdown('<div class="section-label" style="margin-top:6px;">✨ AI SCHOOL BRIEFING</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="card" style="background:linear-gradient(135deg,{NAVY},{BLUE});color:white;">', unsafe_allow_html=True)
    if st.button("Generate today's school briefing", key="briefing_btn"):
        st.session_state["_briefing"] = ask_claude(
            "You write a warm 2-sentence daily briefing for parents of a Ugandan secondary school, "
            "highlighting upcoming events and anything urgent. Be warm and professional.",
            f"School: {SCHOOL['full_name']}. Upcoming: End of term exams 7 July. "
            f"Latest notice: '{NOTICES[0]['title']}'. Sports day 12 July. Fees due 30 June.")
    st.write(st.session_state.get("_briefing",
             "Tap for a 2-sentence AI summary of what's happening at the school today."))
    st.markdown("</div>", unsafe_allow_html=True)

    # Latest 2 notices
    st.markdown('<div class="section-label" style="margin-top:6px;">📢 LATEST NOTICES</div>', unsafe_allow_html=True)
    for n in NOTICES[:2]:
        st.markdown(f"""<div class="notice-card {n['category']}">
            <span class="pill pill-{n['category']}">{n['category'].title()}</span>
            <span style="float:right;color:{SLATE};font-size:11.5px;">{n['time']}</span>
            <div class="notice-title">{n['title']}</div>
            <div style="color:{SLATE};font-size:13px;line-height:1.5;">{n['body'][:120]}…</div>
        </div>""", unsafe_allow_html=True)
    if st.button("View all notices →", use_container_width=False):
        st.session_state.nav = "notify"
        st.rerun()

    # Upcoming events (next 3)
    st.markdown('<div class="section-label" style="margin-top:6px;">📅 COMING UP</div>', unsafe_allow_html=True)
    chip_color = {"emergency": CRIMSON, "fees": GOLD, "exam": NAVY, "event": "#2E86C1", "meeting": BLUE}
    for e in EVENTS[:3]:
        col = chip_color.get(e["tag"], BLUE)
        st.markdown(f"""<div class="card" style="display:flex;align-items:center;gap:14px;padding:12px 16px;">
            <div style="min-width:50px;text-align:center;border-radius:10px;padding:5px 4px;background:{col};color:white;font-family:'Poppins',sans-serif;">
                <div style="font-size:14px;font-weight:800;line-height:1;">{e['date'].split()[0]}</div>
                <div style="font-size:9px;letter-spacing:.06em;opacity:.85;">{e['month']}</div>
            </div>
            <div style="font-weight:600;color:{INK};font-size:13.5px;">{e['label']}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown(f"""<div class="dark-banner">
        <span>🔍 Find your child's record</span><span>→</span>
    </div>""", unsafe_allow_html=True)
    if st.button("Go to My Child →", type="primary", use_container_width=True):
        st.session_state.nav = "child"
        st.rerun()

# =================================================================
# PAGE: MY CHILD — search, then dashboard
# =================================================================
def page_child():
    if s is None:
        st.markdown('<div class="section-label">🔍 FIND YOUR CHILD</div>', unsafe_allow_html=True)
        st.caption("Enter your child's name to access their record.")
        query = st.text_input("Search", placeholder="e.g. Mawanda, Simon, Kenneth…",
                               label_visibility="collapsed")
        if query:
            matches = STUDENTS_DF[STUDENTS_DF["name"].str.contains(query, case=False, na=False)]
            if matches.empty:
                st.error("No student found. Try a different name, or contact the school office.")
            else:
                for _, row in matches.iterrows():
                    st.markdown(f"""<div class="card" style="padding:14px 18px;">
                        <div style="font-weight:700;color:{INK};font-size:15px;">{row['name']}</div>
                        <div style="color:{SLATE};font-size:12.5px;">{row['klass']} · Adm. {row['admission_no']} · Guardian: {row['guardian']}</div>
                    </div>""", unsafe_allow_html=True)
                    if st.button(f"Open {row['name'].split()[0]}'s record →", key=f"sel_{row['admission_no']}"):
                        st.session_state.student = row.to_dict()
                        st.rerun()
        else:
            st.caption("⚠️ This demo has 4 sample students. In the real app this connects to your school's database.")
        return

    # ---- Student is selected ----
    bal = fees_balance(s)
    paid_live = s["fees_billed"] - bal

    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(f"""<div class="card" style="border-left:5px solid {BLUE};">
            <div style="font-family:'Poppins',sans-serif;font-weight:800;font-size:17px;color:{NAVY};">{s['name']}</div>
            <div style="color:{SLATE};font-size:12.5px;">{s['klass']} · Adm. {s['admission_no']} · Guardian: {s['guardian']}</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        if st.button("Switch"):
            st.session_state.student = None
            st.session_state.chat = []
            st.rerun()

    # Quick stats for child
    st.markdown('<div class="stat-row">'
        f'<div class="stat-mini"><div class="val" style="color:{"#1FAF54" if s["attendance_pct"]>=90 else CRIMSON};">{s["attendance_pct"]}%</div><div class="lab">Attendance</div></div>'
        f'<div class="stat-mini"><div class="val" style="color:{CRIMSON_DARK if bal>0 else "#1FAF54"};">{money(bal) if bal>0 else "Paid ✅"}</div><div class="lab">Fee Balance</div></div>'
        f'<div class="stat-mini"><div class="val">{s["rank"]}/{s["out_of"]}</div><div class="lab">Class Rank</div></div>'
        '</div>', unsafe_allow_html=True)

    child_tabs = st.tabs(["📊 Report Card", "✅ Attendance", "💳 Pay Fees", "🤖 AI Assistant"])

    # --- Report Card ---
    with child_tabs[0]:
        avg = round(sum(f for _, _, f in s["subjects"]) / len(s["subjects"]), 1)
        def grade(sc):
            return "A" if sc>=80 else "B" if sc>=70 else "C" if sc>=60 else "D" if sc>=50 else "F"
        st.markdown(f"""<div class="card">
            <div style="font-family:'Poppins',sans-serif;font-size:20px;font-weight:800;color:{NAVY};">
                Position {s['rank']} <span style="color:{SLATE};font-size:13px;font-weight:600;">of {s['out_of']}</span>
                &nbsp;·&nbsp; Avg <span style="color:{BLUE};">{avg}%</span>
            </div>
            <div style="color:{SLATE};font-size:12px;">Term 2, 2026 · {s['klass']}</div>
        </div>""", unsafe_allow_html=True)
        for name, mid, fin in s["subjects"]:
            up = fin >= mid
            col = BLUE if up else CRIMSON
            st.markdown(f"""<div class="card" style="display:flex;align-items:center;justify-content:space-between;padding:13px 18px;">
                <div style="display:flex;align-items:center;gap:12px;">
                    <div style="width:32px;height:32px;border-radius:8px;background:{SKY};color:{NAVY};display:flex;align-items:center;justify-content:center;font-weight:800;font-size:12px;">{grade(fin)}</div>
                    <span style="font-weight:600;color:{INK};">{name}</span>
                </div>
                <span style="font-family:'Poppins',sans-serif;font-weight:700;color:{col};">{mid} → {fin} {'↑' if up else '↓'}</span>
            </div>""", unsafe_allow_html=True)
        report_txt = (f"{SCHOOL['full_name']}\nOFFICIAL REPORT CARD — TERM 2, 2026\n"
                      f"Student: {s['name']}\nClass: {s['klass']}\nAdm No: {s['admission_no']}\n"
                      f"Position: {s['rank']} of {s['out_of']}\nAverage: {avg}%\n\n"
                      + "\n".join(f"{n}: {m}->{f} (Grade {grade(f)})" for n,m,f in s["subjects"])
                      + "\n\nClass teacher: Keep up the effort and revise past papers consistently.")
        st.download_button("⬇️ Download report card", data=report_txt,
                            file_name=f"{s['name'].replace(' ','_')}_T2_2026.txt")

    # --- Attendance ---
    with child_tabs[1]:
        ring_color = GREEN if s["attendance_pct"]>=90 else (GOLD if s["attendance_pct"]>=75 else CRIMSON)
        st.markdown(f"""<div class="card" style="text-align:center;padding:24px;">
            <div style="font-family:'Poppins',sans-serif;font-size:40px;font-weight:800;color:{ring_color};">{s['attendance_pct']}%</div>
            <div style="color:{SLATE};font-size:13px;">Present this term</div>
        </div>""", unsafe_allow_html=True)
        log = [("Mon 22 Jun","Present","🟢"),("Tue 23 Jun","Present","🟢"),
               ("Wed 24 Jun","Late — arrived 8:40am","🟡"),("Thu 18 Jun","Absent — no reason given","🔴"),
               ("Wed 17 Jun","Present","🟢"),("Tue 16 Jun","Present","🟢")]
        for date, status, icon in log:
            st.markdown(f"""<div class="card" style="display:flex;align-items:center;gap:12px;padding:11px 16px;">
                <span style="font-size:15px;">{icon}</span>
                <span><b>{date}</b> — <span style="color:{SLATE};">{status}</span></span>
            </div>""", unsafe_allow_html=True)

    # --- Pay Fees ---
    with child_tabs[2]:
        st.markdown('<div class="section-label">💳 PAY WITH CODE</div>', unsafe_allow_html=True)
        code_in = st.text_input("Payment code", value=s.get("payment_code",""),
                                 placeholder="e.g. WN-0417")
        if code_in.strip():
            match = STUDENTS_DF[STUDENTS_DF["payment_code"].str.upper() == code_in.strip().upper()]
            if match.empty:
                st.error("❌ Invalid code. Check the fee structure or report card for the correct code.")
            else:
                ps = match.iloc[0].to_dict()
                ps_bal = fees_balance(ps)
                ps_paid = ps["fees_billed"] - ps_bal
                st.markdown(f"""<div class="card" style="border-left:5px solid {GREEN};">
                    <span style="color:{GREEN};font-weight:700;font-size:12px;">✅ CODE VERIFIED</span>
                    <div style="font-family:'Poppins',sans-serif;font-weight:800;font-size:17px;color:{NAVY};margin-top:6px;">{ps['name']}</div>
                    <div style="color:{SLATE};font-size:12.5px;">Class: <b>{ps['class_level']}</b> &nbsp;·&nbsp; Stream: <b>{ps['stream']}</b> &nbsp;·&nbsp; Adm. {ps['admission_no']}</div>
                </div>""", unsafe_allow_html=True)
                st.markdown(f"""<div class="acct-card">
                    <div class="stat-line">Outstanding balance</div>
                    <div style="font-family:'Poppins',sans-serif;font-size:28px;font-weight:800;color:{CRIMSON_DARK if ps_bal>0 else GREEN};">{money(ps_bal) if ps_bal>0 else "Fully Paid ✅"}</div>
                    {"<div class='warn'>Due 30 June 2026</div>" if ps_bal>0 else ""}
                </div>""", unsafe_allow_html=True)
                if ps_bal > 0:
                    st.progress(ps_paid/ps["fees_billed"],
                                text=f"{ps_paid/ps['fees_billed']*100:.0f}% paid · {money(ps_paid)} of {money(ps['fees_billed'])}")
                    method = st.radio("Payment method", ["MTN Mobile Money","Airtel Money","Bank Deposit"],
                                      label_visibility="collapsed")
                    phone  = st.text_input("Phone number", value=ps["guardian_phone"])
                    choice = st.radio("Amount", ["Pay full balance","Pay a custom amount"])
                    amount = ps_bal if choice=="Pay full balance" else st.number_input(
                        "Amount (UGX)", min_value=1000, max_value=int(ps_bal), value=min(100000,int(ps_bal)), step=5000)
                    st.caption("🔧 Demo mode — real payments need the school to register with a licensed aggregator "
                               "(Flutterwave / Pegasus / Relworx).")
                    if st.button(f"Pay {money(amount)} via {method} →", type="primary", use_container_width=True):
                        with st.spinner("Processing…"):
                            time.sleep(1.6)
                        ref = f"{method.split()[0][:2].upper()}{datetime.now().strftime('%y%m%d')}.{random.randint(1000,9999)}"
                        st.session_state.paid_extra[ps["admission_no"]] = \
                            st.session_state.paid_extra.get(ps["admission_no"],0) + amount
                        st.session_state["_last_receipt"] = {
                            "name": ps["name"], "date": datetime.now().strftime("%d %b %Y"),
                            "method": method, "amount": amount, "ref": ref}
                        st.balloons()
                        st.rerun()
                if st.session_state["_last_receipt"]:
                    r = st.session_state["_last_receipt"]
                    st.markdown(f"""<div class="card" style="border-left:5px solid {GREEN};">
                        <b style="color:{GREEN};">✅ Payment received</b>
                        <p style="margin:6px 0 0 0;font-size:13.5px;color:{SLATE};">
                        {money(r['amount'])} via {r['method']} for {r['name']} on {r['date']}<br>Ref: {r['ref']}</p>
                    </div>""", unsafe_allow_html=True)
                    st.download_button("⬇️ Download receipt",
                        data=f"{SCHOOL['full_name']}\nStudent: {r['name']}\nAmount: {money(r['amount'])}\n"
                             f"Method: {r['method']}\nDate: {r['date']}\nRef: {r['ref']}\n",
                        file_name="receipt.txt")
        else:
            st.info("👆 Enter the payment code from your child's fee structure or report card.")
        st.markdown('<div class="section-label" style="margin-top:16px;">🧾 PAYMENT HISTORY</div>', unsafe_allow_html=True)
        st.dataframe(pd.DataFrame([{"Date":h["date"],"Method":h["method"],"Amount":money(h["amount"]),"Ref":h["ref"]}
                                    for h in PAYMENT_HISTORY_SEED]), use_container_width=True, hide_index=True)

    # --- AI Assistant ---
    with child_tabs[3]:
        bal = fees_balance(s)
        system_prompt = (
            "You are the Parent AI Assistant for a Ugandan secondary school. Speak warmly and briefly "
            "(2-5 sentences). Use UGX for money. Only use this record, never invent numbers:\n"
            f"Student: {s['name']}, Class: {s['klass']}\n"
            f"Attendance: {s['attendance_pct']}% this term\n"
            f"Fees: billed {s['fees_billed']} UGX, paid {s['fees_billed']-bal} UGX, balance {bal} UGX, due 30 June 2026\n"
            f"Class rank: {s['rank']} of {s['out_of']}\n"
            f"Subjects (midterm->final): {', '.join(f'{n} {m}->{f}' for n,m,f in s['subjects'])}\n"
            "If asked something outside this record, say you don't have that information and suggest messaging the school.")
        for msg in st.session_state.chat:
            with st.chat_message(msg["role"]):
                st.write(msg["text"])
        scols = st.columns(3)
        for col, sug in zip(scols, ["When are next exams?","What's my child's attendance?","How much fees remain?"]):
            if col.button(sug, key=f"sug_{sug}"):
                st.session_state.chat.append({"role":"user","text":sug})
                st.session_state.chat.append({"role":"assistant","text":ask_claude(system_prompt,sug)})
                st.rerun()
        inp = st.chat_input("Ask about fees, attendance, exams…")
        if inp:
            st.session_state.chat.append({"role":"user","text":inp})
            st.session_state.chat.append({"role":"assistant","text":ask_claude(system_prompt,inp)})
            st.rerun()
        st.divider()
        lang = st.selectbox("Translate last reply to:", ["—","Luganda","Swahili","English"])
        if lang != "—" and st.session_state.chat:
            last = next((m["text"] for m in reversed(st.session_state.chat) if m["role"]=="assistant"), None)
            if last and st.button("Translate"):
                st.info(ask_claude(f"Translate into {lang}, naturally and warmly. Output only the translation.", last))

# =================================================================
# PAGE: NOTIFICATIONS
# =================================================================
def page_notify():
    st.markdown('<div class="section-label">🔔 NOTIFICATIONS</div>', unsafe_allow_html=True)
    _, col_r = st.columns([3,1])
    with col_r:
        if st.button("Mark all read"):
            st.session_state.read_ids = {n["id"] for n in NOTICES}
            st.rerun()
    for n in NOTICES:
        is_unread = n["id"] not in st.session_state.read_ids
        st.markdown(f"""<div class="notice-card {n['category']}">
            <span class="pill pill-{n['category']}">{n['category'].title()}</span>
            <span style="float:right;color:{SLATE};font-size:11.5px;">{n['time']}</span>
            <div class="notice-title">{'🔵 ' if is_unread else ''}{n['title']}</div>
            <div style="color:{SLATE};font-size:13.5px;line-height:1.55;">{n['body']}</div>
        </div>""", unsafe_allow_html=True)
        b1, b2, _ = st.columns([1,1,3])
        with b1:
            if st.button("✨ AI summary", key=f"sum_{n['id']}"):
                st.success(ask_claude(
                    "Shorten this school announcement into one calm, plain sentence for a parent, under 25 words.",
                    n["body"]))
        with b2:
            if is_unread and st.button("Mark read", key=f"rd_{n['id']}"):
                st.session_state.read_ids.add(n["id"])
                st.rerun()

# =================================================================
# PAGE: CALENDAR
# =================================================================
def page_calendar():
    st.markdown('<div class="section-label">📅 TERM 2 — 2026</div>', unsafe_allow_html=True)
    chip_color = {"emergency":CRIMSON,"fees":GOLD,"exam":NAVY,"event":"#2E86C1","meeting":BLUE}
    for e in EVENTS:
        col = chip_color.get(e["tag"], BLUE)
        st.markdown(f"""<div class="card" style="display:flex;align-items:center;gap:14px;padding:12px 16px;">
            <div style="min-width:52px;text-align:center;border-radius:10px;padding:6px 4px;background:{col};color:white;font-family:'Poppins',sans-serif;">
                <div style="font-size:14px;font-weight:800;line-height:1;">{e['date'].split()[0]}</div>
                <div style="font-size:9px;letter-spacing:.06em;opacity:.85;">{e['month']}</div>
            </div>
            <div style="font-weight:600;color:{INK};font-size:14px;">{e['label']}</div>
        </div>""", unsafe_allow_html=True)

# =================================================================
# PAGE: MESSAGES
# =================================================================
def page_messages():
    if st.session_state.active_thread is None:
        st.markdown('<div class="section-label">💬 MESSAGES</div>', unsafe_allow_html=True)
        for t in st.session_state.threads:
            last = t["messages"][-1]["text"]
            st.markdown(f"""<div class="card" style="padding:14px 18px;">
                <b style="color:{NAVY};">{'👥 ' if t.get('group') else '👤 '}{t['with']}</b>
                <p style="color:{SLATE};font-size:12.5px;margin:4px 0 0 0;">{last[:80]}{'…' if len(last)>80 else ''}</p>
            </div>""", unsafe_allow_html=True)
            if st.button("Open", key=f"th_{t['id']}"):
                st.session_state.active_thread = t["id"]
                st.rerun()
    else:
        t = next(x for x in st.session_state.threads if x["id"] == st.session_state.active_thread)
        if st.button("← Back"):
            st.session_state.active_thread = None
            st.rerun()
        st.markdown(f"#### {t['with']}")
        for m in t["messages"]:
            with st.chat_message("user" if m["from"]=="parent" else "assistant"):
                st.write(m["text"])
                st.caption(m["time"])
        reply = st.chat_input("Write a message…")
        if reply:
            t["messages"].append({"from":"parent","text":reply,"time":"Now"})
            st.rerun()

# =================================================================
# PAGE: ACHIEVEMENTS
# =================================================================
def page_achieve():
    st.markdown('<div class="section-label">🏆 SCHOOL ACHIEVEMENTS</div>', unsafe_allow_html=True)
    for h in HIGHLIGHTS:
        st.markdown(f"""<div class="ach-card">
            <div class="ach-icon" style="background:linear-gradient(135deg,{h['c1']},{h['c2']});color:white;">{h['emoji']}</div>
            <div>
                <div style="font-weight:700;color:{NAVY};font-size:14.5px;">{h['title']}</div>
                <div style="color:{SLATE};font-size:13px;line-height:1.55;margin-top:3px;">{h['detail']}</div>
            </div>
        </div>""", unsafe_allow_html=True)

# =================================================================
# ROUTER
# =================================================================
PAGES = {
    "home": page_home, "child": page_child,
    "notify": page_notify, "calendar": page_calendar,
    "messages": page_messages, "achieve": page_achieve,
    "pay": lambda: page_child() or None,   # pay tab opens child page on Pay Fees sub-tab
}
PAGES.get(st.session_state.nav, page_home)()

# =================================================================
# BOTTOM NAV — TikTok style
# =================================================================
with st.container(border=True):
    st.markdown('<div class="navmarker"></div>', unsafe_allow_html=True)

    nav_items = [
        ("home",     "🏠",  "Home",      None),
        ("child",    "👤",  "My Child",  None),
        ("pay",      "+",   "",          None),   # center raise button
        ("notify",   "🔔",  "Alerts",    unread if unread else None),
        ("messages", "💬",  "Messages",  None),
    ]

    ncols = st.columns([1,1,1.1,1,1])
    for col, (key, icon, label, badge) in zip(ncols, nav_items):
        with col:
            active = st.session_state.nav == key
            if key == "pay":
                # Raised center button
                st.markdown(f"""
                <div style="display:flex;justify-content:center;align-items:center;padding:6px 0 8px 0;">
                    <div style="width:52px;height:44px;border-radius:14px;
                                background:linear-gradient(135deg,{BLUE},{CRIMSON});
                                display:flex;align-items:center;justify-content:center;
                                font-size:26px;font-weight:300;color:white;
                                box-shadow:0 4px 18px rgba(11,79,158,.55);
                                transform:translateY(-8px);cursor:pointer;">＋</div>
                </div>""", unsafe_allow_html=True)
                if col.button("Pay", key="nav_pay", use_container_width=True,
                              type="primary" if active else "secondary"):
                    st.session_state.nav = "pay"
                    st.rerun()
            else:
                badge_html = (f'<span style="background:#C8102E;color:white;border-radius:50%;'
                              f'font-size:9px;font-weight:800;padding:1px 5px;'
                              f'vertical-align:super;margin-left:1px;">{badge}</span>'
                              if badge else "")
                btn_label = f"{icon}{badge_html} {label}" if badge else f"{icon} {label}"
                if col.button(btn_label, key=f"nav_{key}", use_container_width=True,
                              type="primary" if active else "secondary"):
                    st.session_state.nav = key
                    st.rerun()
