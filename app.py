import streamlit as st
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

# ---------------------------------------------------------------
# COLOR SYSTEM — navy/blue from the badge, red for accents & alerts
# ---------------------------------------------------------------
NAVY = "#06264D"
BLUE = "#0B4F9E"
SKY = "#EAF3FC"
BG = "#F4F6F9"
CRIMSON = "#C8102E"
CRIMSON_DARK = "#8C0B20"
GOLD = "#D7A33D"
INK = "#10182B"
SLATE = "#5B6B82"
WHITE = "#FFFFFF"

LOGO_PATH = "logo.png"


def get_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None


logo_b64 = get_base64(LOGO_PATH)

# ---------------------------------------------------------------
# GLOBAL STYLE
# ---------------------------------------------------------------
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap');
html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}
h1, h2, h3, h4 {{ font-family: 'Poppins', sans-serif; }}
.stApp {{ background-color: {BG}; }}
#MainMenu {{visibility: hidden;}}
footer {{visibility: hidden;}}
.block-container {{ padding-bottom: 100px !important; padding-top: 1.4rem !important; max-width: 720px; }}

/* ---------- Top app bar ---------- */
.topbar {{
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 14px;
}}
.topbar .brand {{ display: flex; align-items: center; gap: 10px; }}
.topbar .brand img {{ width: 38px; height: 38px; border-radius: 50%; object-fit: contain; background: white; padding: 2px; box-shadow: 0 2px 8px rgba(0,0,0,0.12); }}
.topbar .brand .fallback {{ width:38px;height:38px;border-radius:50%;background:{NAVY};color:white;font-size:9px;font-weight:800;display:flex;align-items:center;justify-content:center; }}
.topbar .brand .name {{ font-family:'Poppins',sans-serif; font-weight:800; font-size:15px; color:{NAVY}; line-height:1.1; }}
.topbar .brand .tag {{ font-size:10.5px; color:{SLATE}; }}
.bell-wrap {{ position: relative; }}
.bell-badge {{
    position: absolute; top: -6px; right: -6px; background: #1FAF54; color: white;
    border-radius: 50%; font-size: 10px; font-weight: 800; width: 18px; height: 18px;
    display: flex; align-items: center; justify-content: center;
}}

/* ---------- Quick action grid (Airtel-style) ---------- */
.grid-card {{
    background: white; border-radius: 18px; padding: 18px 14px 8px 14px; margin-bottom: 14px;
    box-shadow: 0 2px 12px rgba(15,30,51,0.06); border: 1px solid #ECEFF3;
}}
.grid-item {{ text-align: center; padding: 8px 2px 14px 2px; }}
.grid-item .ic {{
    width: 50px; height: 50px; border-radius: 14px; margin: 0 auto 8px auto;
    display: flex; align-items: center; justify-content: center; font-size: 22px;
}}
.grid-item .lbl {{ font-size: 11.5px; font-weight: 600; color: {INK}; line-height: 1.25; }}

/* ---------- Account / student card ---------- */
.acct-card {{
    background: white; border-radius: 18px; padding: 18px 20px; margin-bottom: 14px;
    box-shadow: 0 2px 12px rgba(15,30,51,0.06); border: 1px solid #ECEFF3;
}}
.acct-top {{ display:flex; justify-content:space-between; align-items:flex-start; border-bottom:1px solid #EEF1F5; padding-bottom:14px; margin-bottom:14px; }}
.acct-name {{ font-family:'Poppins',sans-serif; font-weight:800; font-size:16px; color:{INK}; letter-spacing:.01em; }}
.acct-sub {{ font-size:12px; color:{SLATE}; margin-top:2px; }}

.ring-wrap {{ display:flex; align-items:center; gap:22px; }}
.ring {{
    width: 88px; height: 88px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center; flex-shrink: 0;
    position: relative;
}}
.ring .ring-inner {{ font-family:'Poppins',sans-serif; font-weight:800; font-size:16px; text-align:center; line-height:1.1; }}
.stat-line {{ font-size: 12px; color:{SLATE}; }}
.stat-big {{ font-family:'Poppins',sans-serif; font-weight:800; font-size:18px; }}
.warn {{ color:{CRIMSON}; font-weight:700; font-size:11.5px; }}

/* ---------- Highlights / stories ---------- */
.story-scroll {{ display:flex; gap:14px; overflow-x:auto; padding: 4px 2px 10px 2px; }}
.story-circle {{
    width: 64px; height: 64px; border-radius: 50%; flex-shrink:0;
    display:flex; align-items:center; justify-content:center; font-size:24px; color:white;
    border: 3px solid {GOLD};
}}
.story-label {{ font-size: 10.5px; text-align:center; color:{INK}; font-weight:600; margin-top:5px; width:70px; }}

/* ---------- Notice / message cards ---------- */
.notice-card {{
    background: white; border-radius: 14px; padding: 16px 18px; margin-bottom: 10px;
    border-left: 5px solid {BLUE}; box-shadow: 0 2px 10px rgba(15,30,51,0.05);
}}
.notice-card.emergency {{ border-left-color: {CRIMSON}; background: #FDF2F3; }}
.notice-card.fees {{ border-left-color: {GOLD}; }}
.notice-card.exam {{ border-left-color: {NAVY}; }}
.notice-card.event {{ border-left-color: #2E86C1; }}
.pill {{ display:inline-block; padding:3px 11px; border-radius:999px; font-size:10.5px; font-weight:700; text-transform:uppercase; letter-spacing:.05em; }}
.pill-emergency {{ background:{CRIMSON}; color:white; }}
.pill-meeting {{ background:{BLUE}; color:white; }}
.pill-exam {{ background:{NAVY}; color:white; }}
.pill-fees {{ background:{GOLD}; color:#3a2a05; }}
.pill-event {{ background:#2E86C1; color:white; }}
.notice-title {{ font-weight:700; color:{INK}; margin:8px 0 4px 0; font-size:15px; }}

/* ---------- Dark banner ---------- */
.dark-banner {{
    background: {NAVY}; color: white; border-radius: 14px; padding: 14px 18px;
    display:flex; align-items:center; justify-content:space-between; margin-bottom:14px; font-weight:600; font-size:13.5px;
}}

/* ---------- Section label ---------- */
.section-label {{ font-family:'Poppins',sans-serif; font-weight:700; font-size:12px; text-transform:uppercase; letter-spacing:.08em; color:{SLATE}; margin: 4px 0 10px 0; }}

/* ---------- Generic card ---------- */
.card {{ background:white; border-radius:16px; padding:18px 20px; box-shadow:0 2px 10px rgba(15,30,51,0.06); border:1px solid #ECEFF3; margin-bottom:12px; }}

/* ---------- Bottom nav ---------- */
div[data-testid="stVerticalBlockBorderWrapper"]:has(div.navmarker) {{
    position: fixed; bottom: 0; left: 0; right: 0; z-index: 999;
    background: white; box-shadow: 0 -4px 16px rgba(0,0,0,0.08);
    padding: 6px 8px calc(env(safe-area-inset-bottom) + 6px) 8px;
    max-width: 720px; margin: 0 auto; border: none !important;
}}
div[data-testid="stVerticalBlockBorderWrapper"]:has(div.navmarker) > div {{ border: none !important; }}
.navmarker {{ display:none; }}
.stButton button {{ border-radius: 10px; font-weight: 600; }}

/* chat */
[data-testid="stChatMessage"] {{ background:white; border-radius:14px; border:1px solid #ECEFF3; box-shadow:0 2px 8px rgba(15,30,51,0.05); }}

/* ---------- Splash ---------- */
@keyframes fadeUp {{ from {{opacity:0; transform:translateY(14px);}} to {{opacity:1; transform:translateY(0);}} }}
@keyframes logoPulse {{ 0% {{transform:scale(0.85); opacity:0;}} 50% {{transform:scale(1.04); opacity:1;}} 100% {{transform:scale(1); opacity:1;}} }}
@keyframes loadFill {{ from {{width:0%;}} to {{width:100%;}} }}
@keyframes dotFade {{ 0%,100% {{opacity:0;}} 50% {{opacity:1;}} }}
.splash-wrap {{
    background: radial-gradient(circle at 30% 20%, {BLUE} 0%, {NAVY} 55%, #02152e 100%);
    border-radius: 22px; padding: 56px 32px 40px 32px; text-align: center;
    margin-bottom: 14px; animation: fadeUp 0.6s ease-out;
    box-shadow: 0 16px 40px rgba(6,38,77,0.35);
}}
.splash-wrap img, .splash-fallback-logo {{ animation: logoPulse 0.9s ease-out; }}
.splash-wrap img {{ width:110px; height:110px; border-radius:50%; background:white; padding:6px; object-fit:contain; box-shadow:0 8px 22px rgba(0,0,0,0.3); margin-bottom:18px; }}
.splash-wrap h1 {{ color:white; font-size:24px; font-weight:800; margin:0; letter-spacing:-0.01em; }}
.splash-wrap .splash-sub {{ color:{GOLD}; font-style:italic; font-weight:600; font-size:14px; margin:6px 0 0 0; }}
.splash-wrap .splash-tag {{ color:rgba(255,255,255,0.65); font-size:12.5px; margin:22px 0 14px 0; text-transform:uppercase; letter-spacing:.12em; font-weight:600; }}
.loading-bar-track {{ width:180px; height:4px; background:rgba(255,255,255,0.15); border-radius:4px; margin:18px auto 6px auto; overflow:hidden; }}
.loading-bar-fill {{ height:100%; width:0%; background:linear-gradient(90deg,{GOLD},{CRIMSON}); border-radius:4px; animation:loadFill 1.8s ease forwards; }}
.loading-text {{ color:rgba(255,255,255,0.55); font-size:11px; letter-spacing:.05em; }}
.loading-text span {{ animation: dotFade 1.4s infinite; opacity:0; }}
.loading-text span:nth-child(1) {{ animation-delay:0s; }}
.loading-text span:nth-child(2) {{ animation-delay:0.2s; }}
.loading-text span:nth-child(3) {{ animation-delay:0.4s; }}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------
# SCHOOL FACTS
# ---------------------------------------------------------------
SCHOOL = {
    "name": "Wampeewo Ntakke SS",
    "full_name": "Wampeewo Ntakke Secondary School",
    "motto": "Ekula Y'ebuuka",
    "founded": 1966,
    "location": "Gayaza Road, Wakiso, Uganda",
}

# ---------------------------------------------------------------
# SAMPLE STUDENT DATABASE
# ---------------------------------------------------------------
STUDENTS = [
    {"name": "Nantongo Patricia", "klass": "S4 Science", "admission_no": "WNSS/2023/0417",
     "guardian": "Mr. Ssebagala Robert", "guardian_phone": "+256 700 501 001", "attendance_pct": 96,
     "fees_billed": 850000, "fees_paid": 600000, "rank": 6, "out_of": 42,
     "subjects": [("Mathematics", 61, 74), ("Biology", 70, 78), ("Chemistry", 55, 63),
                  ("Physics", 58, 60), ("English", 72, 80), ("Geography", 66, 71)]},
    {"name": "Okello Brian", "klass": "S2 East", "admission_no": "WNSS/2024/0182",
     "guardian": "Mrs. Okello Joyce", "guardian_phone": "+256 752 220 884", "attendance_pct": 89,
     "fees_billed": 620000, "fees_paid": 620000, "rank": 14, "out_of": 38,
     "subjects": [("Mathematics", 48, 55), ("Biology", 60, 64), ("English", 52, 58),
                  ("History", 70, 72), ("CRE", 80, 84)]},
    {"name": "Namutebi Sarah", "klass": "S6 Arts", "admission_no": "WNSS/2021/0099",
     "guardian": "Mr. Namutebi Henry", "guardian_phone": "+256 772 901 233", "attendance_pct": 98,
     "fees_billed": 950000, "fees_paid": 950000, "rank": 2, "out_of": 30,
     "subjects": [("Economics", 78, 85), ("Literature", 81, 88), ("Geography", 75, 79),
                  ("CRE", 80, 83)]},
    {"name": "Mukasa David", "klass": "S1 West", "admission_no": "WNSS/2026/0301",
     "guardian": "Mr. Mukasa Fred", "guardian_phone": "+256 701 887 410", "attendance_pct": 92,
     "fees_billed": 540000, "fees_paid": 270000, "rank": 9, "out_of": 45,
     "subjects": [("Mathematics", 50, 54), ("Science", 58, 61), ("English", 60, 65),
                  ("Social Studies", 66, 70)]},
]
STUDENTS_DF = pd.DataFrame(STUDENTS)

NOTICES = [
    {"id": 1, "category": "emergency", "time": "Today, 7:05 AM",
     "title": "School closed Friday — heavy rain flooding",
     "body": "Due to flooding along Gayaza Road, the school will remain closed this Friday, "
             "26 June. Day scholars should not report. Boarding students remain on campus. "
             "Updates will follow by Sunday evening."},
    {"id": 2, "category": "meeting", "time": "Yesterday, 4:30 PM",
     "title": "S4 Parents' Meeting — Friday 2:00 PM",
     "body": "All parents and guardians of S4 students are invited to a meeting in the main "
             "hall this Friday at 2:00 PM to discuss UCE registration and mock exam performance."},
    {"id": 3, "category": "exam", "time": "Mon, 22 Jun",
     "title": "End of Term 2 exams begin 7 July",
     "body": "End of Term 2 examinations begin Monday 7 July and run for two weeks. The full "
             "timetable is posted on the noticeboard and available from class teachers."},
    {"id": 4, "category": "fees", "time": "Fri, 19 Jun",
     "title": "Term 2 balance deadline — 30 June",
     "body": "All outstanding Term 2 fee balances should be cleared by 30 June so students can "
             "sit end of term examinations without disruption."},
    {"id": 5, "category": "event", "time": "Wed, 17 Jun",
     "title": "Inter-house sports day — 12 July",
     "body": "The annual inter-house sports day will be held on 12 July from 8:30 AM. Parents "
             "and guardians are warmly welcome to attend."},
]

EVENTS = [
    {"date": "26 Jun", "month": "JUN", "label": "School closed — flooding (day scholars)", "tag": "emergency"},
    {"date": "27 Jun", "month": "JUN", "label": "Visiting Sunday", "tag": "event"},
    {"date": "30 Jun", "month": "JUN", "label": "Fees deadline — Term 2 balance", "tag": "fees"},
    {"date": "7 Jul", "month": "JUL", "label": "End of Term 2 examinations begin (2 weeks)", "tag": "exam"},
    {"date": "12 Jul", "month": "JUL", "label": "Inter-house sports day", "tag": "event"},
    {"date": "26 Jul", "month": "JUL", "label": "Term 2 closing day", "tag": "meeting"},
]

# Highlights — circular "story" style achievements. Drop a real photo in the repo
# (e.g. highlight_1.jpg) and it'll be used automatically; otherwise a colour + emoji shows.
HIGHLIGHTS = [
    {"id": 1, "title": "UCE Results", "emoji": "📚", "c1": BLUE, "c2": NAVY, "image": "highlight_1.jpg",
     "detail": "96% UCE pass rate in 2025 — the school's strongest results in five years, "
               "with 12 students attaining first grade."},
    {"id": 2, "title": "Sports Day", "emoji": "🥇", "c1": CRIMSON, "c2": CRIMSON_DARK, "image": "highlight_2.jpg",
     "detail": "Wakiso District inter-school athletics champions for the second year running."},
    {"id": 3, "title": "STEM Fair", "emoji": "🔬", "c1": "#2E86C1", "c2": "#1B4F72", "image": "highlight_3.jpg",
     "detail": "Named Best STEM School, Wakiso District 2025, for the STEM club's mosquito-trap "
               "innovation project."},
    {"id": 4, "title": "Cultural Day", "emoji": "🎭", "c1": GOLD, "c2": "#8C6510", "image": "highlight_4.jpg",
     "detail": "First place, Buganda regional cultural dance competition."},
    {"id": 5, "title": "Thanksgiving", "emoji": "🎓", "c1": NAVY, "c2": "#02152e", "image": "highlight_5.jpg",
     "detail": "Annual thanksgiving and graduation service for S6 leavers, June 2026."},
]

THREADS_SEED = [
    {"id": 1, "with": "Mrs. Nakimera — Class Teacher", "messages": [
        {"from": "teacher", "text": "Good morning. Your child did well in today's Chemistry quiz — 14/20.", "time": "10:40 AM"},
        {"from": "parent", "text": "Thank you Madam, we will keep encouraging the revision at home.", "time": "10:42 AM"},
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
    {"date": "02 Apr 2026", "method": "Bank deposit", "amount": 300000, "ref": "CB-220409-77"},
]


# ---------------------------------------------------------------
# CLAUDE API HELPER
# ---------------------------------------------------------------
def ask_claude(system_prompt: str, user_text: str) -> str:
    api_key = st.secrets.get("ANTHROPIC_API_KEY")
    if not api_key:
        return "⚠️ No ANTHROPIC_API_KEY found in secrets. Add it under Settings → Secrets to enable AI features."
    try:
        resp = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={"x-api-key": api_key, "anthropic-version": "2023-06-01", "content-type": "application/json"},
            json={"model": "claude-sonnet-4-6", "max_tokens": 600, "system": system_prompt,
                  "messages": [{"role": "user", "content": user_text}]},
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        return "".join(b.get("text", "") for b in data.get("content", [])).strip() or "No response."
    except Exception as e:
        return f"⚠️ AI request failed: {e}"


def money(n):
    return f"UGX {n:,.0f}"


# ---------------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------------
defaults = {
    "student": None, "chat": [], "entered": False, "read_ids": set(),
    "toasted_for": None, "nav": "home", "threads": None, "active_thread": None,
    "open_highlight": None, "paid_extra": {},
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v
if st.session_state.threads is None:
    st.session_state.threads = [dict(t, messages=list(t["messages"])) for t in THREADS_SEED]

# ---------------------------------------------------------------
# SPLASH SCREEN — automatic, no tap needed
# ---------------------------------------------------------------
if not st.session_state.entered:
    splash_logo = (f'<img src="data:image/png;base64,{logo_b64}" />' if logo_b64 else
                   f'<div class="splash-fallback-logo" style="width:110px;height:110px;border-radius:50%;'
                   f'background:white;display:flex;align-items:center;justify-content:center;font-weight:800;'
                   f'color:{NAVY};font-size:13px;margin:0 auto 18px auto;">WNSS</div>')
    st.markdown(f"""
    <div class="splash-wrap">
        {splash_logo}
        <h1>{SCHOOL['full_name']}</h1>
        <p class="splash-sub">"{SCHOOL['motto']}"</p>
        <p class="splash-tag">Parent Portal</p>
        <div class="loading-bar-track"><div class="loading-bar-fill"></div></div>
        <p class="loading-text">LOADING<span>.</span><span>.</span><span>.</span></p>
    </div>
    """, unsafe_allow_html=True)
    time.sleep(1.9)
    st.session_state.entered = True
    st.rerun()

# ---------------------------------------------------------------
# TOP BAR (always visible once inside)
# ---------------------------------------------------------------
brand_logo = (f'<img src="{"data:image/png;base64,"+logo_b64}" />' if logo_b64 else
              f'<div class="fallback">WNSS</div>')
unread_count = len([n for n in NOTICES if n["id"] not in st.session_state.read_ids])

st.markdown(f"""
<div class="topbar">
    <div class="brand">
        {brand_logo}
        <div>
            <div class="name">{SCHOOL['name']}</div>
            <div class="tag">Parent Portal</div>
        </div>
    </div>
    <div class="bell-wrap">
        <span style="font-size:22px;">🔔</span>
        {f'<span class="bell-badge">{unread_count}</span>' if unread_count else ''}
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------
# STUDENT SEARCH GATE
# ---------------------------------------------------------------
if st.session_state.student is None:
    st.markdown('<div class="section-label">🔍 FIND YOUR CHILD</div>', unsafe_allow_html=True)
    query = st.text_input("Search", placeholder="Type your child's name — e.g. Nantongo, Okello, Sarah...",
                           label_visibility="collapsed")
    if query:
        matches = STUDENTS_DF[STUDENTS_DF["name"].str.contains(query, case=False, na=False)]
        if matches.empty:
            st.info("No student found in this demo database. Connect your real student register to search live records.")
        else:
            for _, row in matches.iterrows():
                st.markdown(f"""
                <div class="card" style="padding:14px 18px;">
                    <div style="font-weight:700;color:{INK};font-size:15px;">{row['name']}</div>
                    <div style="color:{SLATE};font-size:12.5px;">{row['klass']} · Adm. {row['admission_no']} · Guardian: {row['guardian']}</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"View {row['name'].split()[0]}'s record →", key=row["admission_no"]):
                    st.session_state.student = row.to_dict()
                    st.rerun()
    else:
        st.caption("⚠️ Sample database of 4 demo students. Swap `STUDENTS` for your real register to go live.")
    st.stop()

s = st.session_state.student
extra_paid = st.session_state.paid_extra.get(s["admission_no"], 0)
fees_paid_live = s["fees_paid"] + extra_paid
balance = s["fees_billed"] - fees_paid_live

if st.session_state.toasted_for != s["admission_no"]:
    urgent = next((n for n in NOTICES if n["category"] == "emergency"), None)
    if urgent:
        st.toast(f"🔔 {urgent['title']}", icon="🚨")
    st.session_state.toasted_for = s["admission_no"]


# =================================================================
# PAGE: HOME
# =================================================================
def page_home():
    st.markdown(f"""
    <div class="acct-card">
        <div class="acct-top" style="border-bottom:none; margin-bottom:6px; padding-bottom:0;">
            <div>
                <div class="acct-name">{s['name']}</div>
                <div class="acct-sub">{s['klass']} · Adm. {s['admission_no']}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🔄 Not your child? Switch student", use_container_width=False):
        st.session_state.student = None
        st.session_state.chat = []
        st.rerun()

    # Quick action grid — Airtel-style
    st.markdown('<div class="grid-card">', unsafe_allow_html=True)
    grid_items = [
        ("💳", BLUE, "Pay Fees", "pay"), ("💬", "#2E86C1", "Message School", "messages"),
        ("📊", NAVY, "Report Card", "report"), ("📅", CRIMSON, "Calendar", "calendar"),
        ("✅", "#1FAF54", "Attendance", "attendance"), ("🏆", GOLD, "Achievements", "achieve"),
        ("🤖", "#7B4FCB", "AI Assistant", "ai"), ("🔔", CRIMSON_DARK, "Notifications", "notify"),
    ]
    cols = st.columns(4)
    for i, (icon, color, label, target) in enumerate(grid_items):
        with cols[i % 4]:
            st.markdown(f"""
            <div class="grid-item">
                <div class="ic" style="background:{color}1A; color:{color};">{icon}</div>
                <div class="lbl">{label}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Open", key=f"grid_{target}", use_container_width=True):
                st.session_state.nav = target
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Highlights / achievements story strip
    st.markdown('<div class="section-label">✨ SCHOOL HIGHLIGHTS</div>', unsafe_allow_html=True)
    hcols = st.columns(len(HIGHLIGHTS))
    for i, h in enumerate(HIGHLIGHTS):
        img_b64 = get_base64(h["image"])
        with hcols[i]:
            if img_b64:
                st.markdown(f"""
                <div class="story-circle" style="padding:0;border-color:{GOLD};">
                    <img src="data:image/jpeg;base64,{img_b64}" style="width:100%;height:100%;border-radius:50%;object-fit:cover;" />
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="story-circle" style="background:linear-gradient(135deg,{h['c1']},{h['c2']});">{h['emoji']}</div>
                """, unsafe_allow_html=True)
            st.markdown(f"<div class='story-label'>{h['title']}</div>", unsafe_allow_html=True)
            if st.button("View", key=f"hl_{h['id']}", use_container_width=True):
                st.session_state.open_highlight = h["id"]
                st.rerun()
    if st.session_state.open_highlight:
        hh = next(h for h in HIGHLIGHTS if h["id"] == st.session_state.open_highlight)
        st.markdown(f"""
        <div class="card" style="border-left:5px solid {hh['c1']};">
            <b style="color:{NAVY};">{hh['emoji']} {hh['title']}</b>
            <p style="color:{SLATE};font-size:13.5px;margin-top:6px;">{hh['detail']}</p>
        </div>
        """, unsafe_allow_html=True)
        st.caption("📷 Sample content — drop real photos into the repo (e.g. `highlight_1.jpg`) to replace these.")

    # Attendance ring + fee status
    rcol1, rcol2 = st.columns(2)
    with rcol1:
        ring_color = "#1FAF54" if s["attendance_pct"] >= 90 else (GOLD if s["attendance_pct"] >= 75 else CRIMSON)
        st.markdown(f"""
        <div class="acct-card">
            <div class="ring-wrap">
                <div class="ring" style="border:7px solid {ring_color}22; background: conic-gradient({ring_color} {s['attendance_pct']*3.6}deg, #EEF1F5 0deg);">
                    <div class="ring" style="width:70px;height:70px;background:white;">
                        <div class="ring-inner" style="color:{ring_color};">{s['attendance_pct']}%</div>
                    </div>
                </div>
                <div>
                    <div class="stat-line">Attendance</div>
                    <div class="stat-big" style="color:{ring_color};">This term</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with rcol2:
        warn = balance > 0
        st.markdown(f"""
        <div class="acct-card">
            <div class="stat-line">Fee balance</div>
            <div class="stat-big" style="color:{CRIMSON_DARK if warn else '#1FAF54'};">{money(balance)}</div>
            {f'<div class="warn">⚠️ Due 30 June 2026</div>' if warn else '<div style="color:#1FAF54;font-weight:700;font-size:11.5px;">✅ Fully paid</div>'}
        </div>
        """, unsafe_allow_html=True)

    if st.button("💳 Pay Fees Now", type="primary", use_container_width=True):
        st.session_state.nav = "pay"
        st.rerun()

    st.markdown('<div class="section-label" style="margin-top:18px;">✨ AI DAILY BRIEFING</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="card" style="background:linear-gradient(135deg,{NAVY} 0%,{BLUE} 100%);color:white;">', unsafe_allow_html=True)
    if st.button("Generate today's briefing", key="briefing_btn"):
        prompt = (f"Attendance {s['attendance_pct']}%. Fee balance {money(balance)} due 30 June. "
                  f"Class rank {s['rank']} of {s['out_of']}. Latest notice: '{NOTICES[0]['title']}'. "
                  "Write a warm 2-sentence daily briefing for the parent flagging anything urgent.")
        st.session_state["_briefing"] = ask_claude(
            "You write a short, warm daily briefing (max 2 sentences) for a parent, flagging only what matters.", prompt)
    st.write(st.session_state.get("_briefing", "Tap for a 2-sentence AI summary of anything that needs your attention today."))
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-label" style="margin-top:6px;">📌 LATEST NOTICE</div>', unsafe_allow_html=True)
    n = NOTICES[1]
    st.markdown(f"""
    <div class="notice-card {n['category']}">
        <span class="pill pill-{n['category']}">{n['category'].title()}</span>
        <div class="notice-title">{n['title']}</div>
        <div style="color:{SLATE};font-size:13.5px;line-height:1.55;">{n['body']}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="dark-banner">
        <span>📊 View {s['name'].split()[0]}'s full report card</span><span>→</span>
    </div>
    """, unsafe_allow_html=True)


# =================================================================
# PAGE: NOTIFICATIONS
# =================================================================
def page_notify():
    st.markdown('<div class="section-label">🔔 NOTIFICATIONS</div>', unsafe_allow_html=True)
    top_l, top_r = st.columns([3, 1])
    with top_r:
        if st.button("Mark all read", use_container_width=True):
            st.session_state.read_ids = {n["id"] for n in NOTICES}
            st.rerun()
    for n in NOTICES:
        unread = n["id"] not in st.session_state.read_ids
        dot = "🔵 " if unread else ""
        st.markdown(f"""
        <div class="notice-card {n['category']}">
            <span class="pill pill-{n['category']}">{n['category'].title()}</span>
            <span style="float:right;color:{SLATE};font-size:11.5px;">{n['time']}</span>
            <div class="notice-title">{dot}{n['title']}</div>
            <div style="color:{SLATE};font-size:13.5px;line-height:1.55;">{n['body']}</div>
        </div>
        """, unsafe_allow_html=True)
        b1, b2, _ = st.columns([1, 1, 3])
        with b1:
            if st.button("✨ AI summary", key=f"sum_{n['id']}"):
                st.success(ask_claude(
                    "Shorten this school announcement into one calm, plain sentence for a parent, under 25 words.",
                    n["body"]))
        with b2:
            if unread and st.button("Mark read", key=f"read_{n['id']}"):
                st.session_state.read_ids.add(n["id"])
                st.rerun()


# =================================================================
# PAGE: PAY FEES
# =================================================================
def page_pay():
    st.markdown('<div class="section-label">💳 PAY SCHOOL FEES</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="acct-card">
        <div class="stat-line">Outstanding balance</div>
        <div style="font-family:'Poppins',sans-serif;font-size:30px;font-weight:800;color:{CRIMSON_DARK if balance>0 else '#1FAF54'};">{money(max(balance,0))}</div>
        <div class="warn">Due 30 June 2026</div>
    </div>
    """, unsafe_allow_html=True)
    pct_paid = min(fees_paid_live / s["fees_billed"], 1.0)
    st.progress(pct_paid, text=f"{pct_paid*100:.0f}% paid · {money(fees_paid_live)} of {money(s['fees_billed'])}")

    if balance <= 0:
        st.success("✅ This term's fees are fully paid. Thank you!")
    else:
        st.markdown("##### Choose a payment method")
        method = st.radio("Method", ["MTN Mobile Money", "Airtel Money", "Bank Deposit"], label_visibility="collapsed")
        phone = st.text_input("Phone number for payment", value=s["guardian_phone"])
        amount_choice = st.radio("Amount", ["Pay full balance", "Pay a custom amount"], label_visibility="visible")
        if amount_choice == "Pay full balance":
            amount = balance
        else:
            amount = st.number_input("Amount (UGX)", min_value=1000, max_value=int(balance), value=min(100000, int(balance)), step=5000)

        st.caption("🔧 Demo flow — not yet connected to a live payment gateway. Going live needs the school to "
                   "register with a licensed aggregator (e.g. Flutterwave, Pegasus, Relworx) for real MTN/Airtel "
                   "Money processing.")

        if st.button(f"Pay {money(amount)} via {method} →", type="primary", use_container_width=True):
            with st.spinner(f"Requesting payment of {money(amount)} from {phone}…"):
                time.sleep(1.6)
            ref = f"{method.split()[0].upper()[:2]}{datetime.now().strftime('%y%m%d')}.{random.randint(1000,9999)}"
            st.session_state.paid_extra[s["admission_no"]] = st.session_state.paid_extra.get(s["admission_no"], 0) + amount
            st.session_state["_last_receipt"] = {"date": datetime.now().strftime("%d %b %Y"), "method": method,
                                                  "amount": amount, "ref": ref}
            st.balloons()
            st.rerun()

    if "_last_receipt" in st.session_state:
        r = st.session_state["_last_receipt"]
        st.markdown(f"""
        <div class="card" style="border-left:5px solid #1FAF54;">
            <b style="color:#1FAF54;">✅ Payment received</b>
            <p style="margin:6px 0 0 0;font-size:13.5px;color:{SLATE};">{money(r['amount'])} via {r['method']} on {r['date']}<br>Ref: {r['ref']}</p>
        </div>
        """, unsafe_allow_html=True)
        st.download_button("⬇️ Download receipt",
                            data=f"{SCHOOL['full_name']}\nStudent: {s['name']}\nAmount: {money(r['amount'])}\n"
                                 f"Method: {r['method']}\nDate: {r['date']}\nRef: {r['ref']}\n",
                            file_name="receipt.txt")

    st.markdown('<div class="section-label" style="margin-top:18px;">🧾 PAYMENT HISTORY</div>', unsafe_allow_html=True)
    st.dataframe(pd.DataFrame([{"Date": h["date"], "Method": h["method"], "Amount": money(h["amount"]), "Ref": h["ref"]}
                                for h in PAYMENT_HISTORY_SEED]), use_container_width=True, hide_index=True)


# =================================================================
# PAGE: MESSAGES
# =================================================================
def page_messages():
    if st.session_state.active_thread is None:
        st.markdown('<div class="section-label">💬 MESSAGE THE SCHOOL</div>', unsafe_allow_html=True)
        for t in st.session_state.threads:
            last = t["messages"][-1]["text"]
            st.markdown(f"""
            <div class="card" style="padding:14px 18px;">
                <b style="color:{NAVY};">{'👥 ' if t.get('group') else '👤 '}{t['with']}</b>
                <p style="color:{SLATE};font-size:12.5px;margin:4px 0 0 0;">{last[:70]}{'…' if len(last)>70 else ''}</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Open", key=f"thread_{t['id']}"):
                st.session_state.active_thread = t["id"]
                st.rerun()
    else:
        t = next(x for x in st.session_state.threads if x["id"] == st.session_state.active_thread)
        if st.button("← Back to messages"):
            st.session_state.active_thread = None
            st.rerun()
        st.markdown(f"#### {t['with']}")
        for m in t["messages"]:
            with st.chat_message("user" if m["from"] == "parent" else "assistant"):
                st.write(m["text"])
                st.caption(m["time"])
        reply = st.chat_input("Write a message to the school…")
        if reply:
            t["messages"].append({"from": "parent", "text": reply, "time": "Now"})
            st.rerun()


# =================================================================
# PAGE: REPORT CARD
# =================================================================
def page_report():
    st.markdown('<div class="section-label">📊 OFFICIAL REPORT CARD — TERM 2, 2026</div>', unsafe_allow_html=True)
    avg = round(sum(f for _, _, f in s["subjects"]) / len(s["subjects"]), 1)

    def grade(score):
        return "A" if score >= 80 else "B" if score >= 70 else "C" if score >= 60 else "D" if score >= 50 else "F"

    st.markdown(f"""
    <div class="card">
        <div style="display:flex;gap:28px;flex-wrap:wrap;">
            <div><div style="font-family:'Poppins',sans-serif;font-size:22px;font-weight:800;color:{NAVY};">Position {s['rank']} <span style="color:{SLATE};font-size:13px;font-weight:600;">of {s['out_of']}</span></div><div style="color:{SLATE};font-size:11.5px;">Class rank</div></div>
            <div><div style="font-family:'Poppins',sans-serif;font-size:22px;font-weight:800;color:{NAVY};">{avg}%</div><div style="color:{SLATE};font-size:11.5px;">Average final score</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    for name, mid, fin in s["subjects"]:
        up = fin >= mid
        col = BLUE if up else CRIMSON
        st.markdown(f"""
        <div class="card" style="display:flex;align-items:center;justify-content:space-between;padding:14px 20px;">
            <div style="display:flex;align-items:center;gap:12px;">
                <div style="width:34px;height:34px;border-radius:9px;background:{SKY};color:{NAVY};display:flex;align-items:center;justify-content:center;font-weight:800;font-size:13px;">{grade(fin)}</div>
                <div style="font-weight:600;color:{INK};">{name}</div>
            </div>
            <div style="font-family:'Poppins',sans-serif;font-weight:700;color:{col};">{mid} → {fin} <span style="font-size:13px;">{'↑' if up else '↓'}</span></div>
        </div>
        """, unsafe_allow_html=True)
    report_text = (f"{SCHOOL['full_name']}\nOFFICIAL REPORT CARD — TERM 2, 2026\nStudent: {s['name']}\n"
                   f"Class: {s['klass']}\nAdmission No: {s['admission_no']}\nClass Position: {s['rank']} of {s['out_of']}\n"
                   f"Average Score: {avg}%\n\n" + "\n".join(f"{n}: {m} -> {f} (Grade {grade(f)})" for n, m, f in s["subjects"])
                   + "\n\nClass teacher's comment: Keep up the consistent effort and continue revising past papers.")
    st.download_button("⬇️ Download report card", data=report_text, file_name=f"{s['name'].replace(' ','_')}_report_card.txt")


# =================================================================
# PAGE: CALENDAR
# =================================================================
def page_calendar():
    st.markdown('<div class="section-label">📅 TERM 2 — 2026</div>', unsafe_allow_html=True)
    chip_color = {"emergency": CRIMSON, "fees": GOLD, "exam": NAVY, "event": "#2E86C1", "meeting": BLUE}
    for e in EVENTS:
        col = chip_color.get(e["tag"], BLUE)
        st.markdown(f"""
        <div class="card" style="display:flex;align-items:center;gap:14px;padding:12px 16px;">
            <div style="min-width:54px;text-align:center;border-radius:10px;padding:6px 4px;background:{col};color:white;font-family:'Poppins',sans-serif;">
                <div style="font-size:15px;font-weight:800;line-height:1;">{e['date'].split()[0]}</div>
                <div style="font-size:9px;letter-spacing:.06em;opacity:.85;">{e['month']}</div>
            </div>
            <div style="font-weight:600;color:{INK};font-size:14px;">{e['label']}</div>
        </div>
        """, unsafe_allow_html=True)


# =================================================================
# PAGE: ATTENDANCE
# =================================================================
def page_attendance():
    st.markdown(f"""
    <div class="card"><div class="section-label" style="margin-top:0;">📅 THIS TERM</div>
    <div style="font-family:'Poppins',sans-serif;font-size:28px;font-weight:800;color:{NAVY};">{s['attendance_pct']}% present</div></div>
    """, unsafe_allow_html=True)
    log = [("Mon 22 Jun", "Present", "🟢"), ("Tue 23 Jun", "Present", "🟢"),
           ("Wed 24 Jun", "Late — arrived 8:40am", "🟡"), ("Thu 18 Jun", "Absent — no reason given", "🔴"),
           ("Wed 17 Jun", "Present", "🟢"), ("Tue 16 Jun", "Present", "🟢")]
    for date, status, icon in log:
        st.markdown(f"""<div class="card" style="display:flex;align-items:center;gap:12px;padding:12px 18px;">
        <span style="font-size:16px;">{icon}</span><div><b>{date}</b> — <span style="color:{SLATE};">{status}</span></div></div>""",
                    unsafe_allow_html=True)


# =================================================================
# PAGE: ACHIEVEMENTS
# =================================================================
def page_achieve():
    st.markdown('<div class="section-label">🏆 SCHOOL ACHIEVEMENTS</div>', unsafe_allow_html=True)
    st.caption("Sample achievements — replace with your school's real wins, trophies and results.")
    for h in HIGHLIGHTS:
        st.markdown(f"""
        <div class="card" style="display:flex;gap:14px;align-items:flex-start;">
            <div style="font-size:22px;width:46px;height:46px;border-radius:12px;flex-shrink:0;
                        background:linear-gradient(135deg,{h['c1']},{h['c2']});display:flex;align-items:center;justify-content:center;color:white;">{h['emoji']}</div>
            <div><div style="font-weight:700;color:{NAVY};font-size:14.5px;">{h['title']}</div>
            <div style="color:{SLATE};font-size:13px;line-height:1.55;margin-top:3px;">{h['detail']}</div></div>
        </div>
        """, unsafe_allow_html=True)


# =================================================================
# PAGE: AI ASSISTANT
# =================================================================
def page_ai():
    st.markdown(f"""
    <div class="card" style="display:flex;align-items:center;gap:10px;">
        <div style="width:38px;height:38px;border-radius:50%;background:{NAVY};display:flex;align-items:center;justify-content:center;font-size:16px;">✨</div>
        <div><div style="font-weight:700;color:{NAVY};">Parent AI Assistant</div>
        <div style="color:{SLATE};font-size:12px;">Answers using {s['name']}'s live record</div></div>
    </div>
    """, unsafe_allow_html=True)

    system_prompt = (
        "You are the Parent AI Assistant for a Ugandan secondary school. Speak warmly and briefly "
        "(2-5 sentences). Use UGX for money. Only use this student record, never invent numbers:\n"
        f"Name: {s['name']}, Class: {s['klass']}\nAttendance: {s['attendance_pct']}% this term\n"
        f"Fees: billed {s['fees_billed']} UGX, paid {fees_paid_live} UGX, balance {balance} UGX, due 30 June 2026\n"
        f"Class rank: {s['rank']} of {s['out_of']}\n"
        f"Subjects (midterm->final): {', '.join(f'{n} {m}->{f}' for n, m, f in s['subjects'])}\n"
        "If asked something outside this record, say you don't have that information and suggest "
        "messaging the class teacher or office.")

    for msg in st.session_state.chat:
        with st.chat_message(msg["role"]):
            st.write(msg["text"])

    cols = st.columns(3)
    for col, sug in zip(cols, ["When are the next exams?", "What is my child's attendance?", "How much fees remain?"]):
        if col.button(sug, key=f"sug_{sug}"):
            st.session_state.chat.append({"role": "user", "text": sug})
            st.session_state.chat.append({"role": "assistant", "text": ask_claude(system_prompt, sug)})
            st.rerun()

    user_input = st.chat_input("Ask about fees, attendance, exams…")
    if user_input:
        st.session_state.chat.append({"role": "user", "text": user_input})
        st.session_state.chat.append({"role": "assistant", "text": ask_claude(system_prompt, user_input)})
        st.rerun()

    st.divider()
    lang = st.selectbox("Translate the assistant's last reply to:", ["—", "Luganda", "Swahili", "English"])
    if lang != "—" and st.session_state.chat:
        last_reply = next((m["text"] for m in reversed(st.session_state.chat) if m["role"] == "assistant"), None)
        if last_reply and st.button("Translate"):
            st.info(ask_claude(f"Translate this into {lang}, naturally and warmly. Output only the translation.", last_reply))


# =================================================================
# RENDER ACTIVE PAGE
# =================================================================
PAGES = {
    "home": page_home, "notify": page_notify, "pay": page_pay, "messages": page_messages,
    "report": page_report, "calendar": page_calendar, "attendance": page_attendance,
    "achieve": page_achieve, "ai": page_ai,
}
PAGES.get(st.session_state.nav, page_home)()

# =================================================================
# BOTTOM NAV
# =================================================================
with st.container(border=True):
    st.markdown('<div class="navmarker"></div>', unsafe_allow_html=True)
    nav_items = [("home", "🏠", "Home"), ("notify", "🔔", "Alerts"), ("pay", "💳", "Pay"),
                 ("ai", "🤖", "Assistant"), ("messages", "💬", "Messages")]
    ncols = st.columns(5)
    for col, (key, icon, label) in zip(ncols, nav_items):
        with col:
            active = st.session_state.nav == key
            if col.button(f"{icon} {label}", key=f"nav_{key}", use_container_width=True,
                          type="primary" if active else "secondary"):
                st.session_state.nav = key
                st.rerun()
