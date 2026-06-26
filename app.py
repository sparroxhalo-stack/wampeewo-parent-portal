import streamlit as st
import pandas as pd
import requests
import base64
import os
import time

# ---------------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------------
st.set_page_config(page_title="Wampeewo Ntakke — Parent Portal", page_icon="🛡️", layout="wide")

# ---------------------------------------------------------------
# COLOR SYSTEM — pulled straight from the school badge
# ---------------------------------------------------------------
NAVY = "#06264D"        # shield blue, deep
BLUE = "#0B4F9E"        # shield blue, bright
SKY = "#EAF3FC"         # background tint
CRIMSON = "#C8102E"     # the red on the badge border / banner
CRIMSON_DARK = "#8C0B20"
GOLD = "#D7A33D"        # used only for the fees accent
INK = "#0F1E33"
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

.stApp {{ background-color: {SKY}; }}
#MainMenu {{visibility: hidden;}}
footer {{visibility: hidden;}}

/* ---------- Hero ---------- */
.hero {{
    background: linear-gradient(135deg, {NAVY} 0%, {BLUE} 100%);
    border-radius: 18px;
    padding: 28px 32px;
    margin-bottom: 18px;
    display: flex;
    align-items: center;
    gap: 22px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 10px 30px rgba(6,38,77,0.25);
}}
.hero::after {{
    content: "";
    position: absolute; right: -40px; top: -40px;
    width: 180px; height: 180px; border-radius: 50%;
    background: rgba(255,255,255,0.06);
}}
.hero img {{
    width: 78px; height: 78px; border-radius: 50%;
    background: white; padding: 4px; object-fit: contain;
    box-shadow: 0 4px 14px rgba(0,0,0,0.25);
    position: relative; z-index: 1;
}}
.hero-text {{ position: relative; z-index: 1; }}
.hero-text h1 {{
    color: white; font-size: 23px; font-weight: 800; margin: 0; letter-spacing: -0.01em;
}}
.hero-text .motto {{
    color: {GOLD}; font-style: italic; font-weight: 600; font-size: 13px; margin: 2px 0 0 0;
}}
.hero-text .sub {{
    color: rgba(255,255,255,0.75); font-size: 12.5px; margin: 4px 0 0 0;
}}
.accent-bar {{
    height: 4px; border-radius: 4px; margin-bottom: 22px;
    background: linear-gradient(90deg, {CRIMSON} 0%, {GOLD} 50%, {CRIMSON} 100%);
}}

/* ---------- Section labels ---------- */
.section-label {{
    font-family: 'Poppins', sans-serif; font-weight: 700; font-size: 12px;
    text-transform: uppercase; letter-spacing: .08em; color: {SLATE};
    margin: 4px 0 10px 0; display: flex; align-items: center; gap: 6px;
}}

/* ---------- Cards ---------- */
.card {{
    background: white; border-radius: 16px; padding: 18px 20px;
    box-shadow: 0 2px 10px rgba(15,30,51,0.06); border: 1px solid #E7EEF6;
    margin-bottom: 12px;
}}
.stat-card {{
    background: white; border-radius: 16px; padding: 18px;
    box-shadow: 0 2px 10px rgba(15,30,51,0.06); border: 1px solid #E7EEF6;
    text-align: left;
}}
.stat-card .icon {{
    font-size: 20px; width: 38px; height: 38px; border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    background: {SKY}; margin-bottom: 10px;
}}
.stat-card .value {{ font-family: 'Poppins', sans-serif; font-size: 25px; font-weight: 800; color: {NAVY}; }}
.stat-card .label {{ font-size: 11.5px; color: {SLATE}; text-transform: uppercase; letter-spacing: .04em; font-weight: 600; }}

.notice-card {{
    background: white; border-radius: 14px; padding: 16px 18px; margin-bottom: 10px;
    border-left: 5px solid {BLUE}; box-shadow: 0 2px 10px rgba(15,30,51,0.05);
}}
.notice-card.emergency {{ border-left-color: {CRIMSON}; background: #FDF2F3; }}
.notice-card.fees {{ border-left-color: {GOLD}; }}
.notice-card.exam {{ border-left-color: {NAVY}; }}
.notice-card.event {{ border-left-color: #2E86C1; }}

.pill {{
    display: inline-block; padding: 3px 11px; border-radius: 999px;
    font-size: 10.5px; font-weight: 700; text-transform: uppercase; letter-spacing: .05em;
}}
.pill-emergency {{ background: {CRIMSON}; color: white; }}
.pill-meeting {{ background: {BLUE}; color: white; }}
.pill-exam {{ background: {NAVY}; color: white; }}
.pill-fees {{ background: {GOLD}; color: #3a2a05; }}
.pill-event {{ background: #2E86C1; color: white; }}

.notice-title {{ font-weight: 700; color: {INK}; margin: 8px 0 4px 0; font-size: 15px; }}
.notice-time {{ color: {SLATE}; font-size: 11.5px; }}

/* ---------- Student banner ---------- */
.student-banner {{
    background: white; border-radius: 16px; padding: 16px 20px; margin-bottom: 16px;
    border: 1px solid #E7EEF6; display: flex; align-items: center; justify-content: space-between;
    box-shadow: 0 2px 10px rgba(15,30,51,0.05);
}}
.student-banner .name {{ font-family: 'Poppins', sans-serif; font-weight: 700; font-size: 17px; color: {NAVY}; }}
.student-banner .meta {{ color: {SLATE}; font-size: 12.5px; }}

/* ---------- Tabs ---------- */
button[data-baseweb="tab"] {{
    font-family: 'Poppins', sans-serif; font-weight: 600; font-size: 13.5px;
    color: {SLATE};
}}
button[data-baseweb="tab"][aria-selected="true"] {{ color: {BLUE} !important; }}
div[data-baseweb="tab-highlight"] {{ background-color: {BLUE} !important; height: 3px; }}

/* ---------- Buttons ---------- */
.stButton button {{
    border-radius: 10px; font-weight: 600; font-family: 'Inter', sans-serif;
}}
.stButton button[kind="primary"] {{
    background: {BLUE}; border: none;
}}

/* ---------- Inputs ---------- */
.stTextInput input {{ border-radius: 12px; padding: 10px 14px; }}

/* ---------- Chat ---------- */
[data-testid="stChatMessage"] {{
    background: white; border-radius: 14px; border: 1px solid #E7EEF6;
    box-shadow: 0 2px 8px rgba(15,30,51,0.05);
}}

/* ---------- Splash screen ---------- */
@keyframes fadeUp {{
    from {{ opacity: 0; transform: translateY(14px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}
.splash-wrap {{
    background: radial-gradient(circle at 30% 20%, {BLUE} 0%, {NAVY} 55%, #02152e 100%);
    border-radius: 22px; padding: 56px 32px 40px 32px; text-align: center;
    margin-bottom: 14px; animation: fadeUp 0.6s ease-out;
    box-shadow: 0 16px 40px rgba(6,38,77,0.35);
}}
.splash-wrap img {{
    width: 110px; height: 110px; border-radius: 50%; background: white; padding: 6px;
    object-fit: contain; box-shadow: 0 8px 22px rgba(0,0,0,0.3); margin-bottom: 18px;
}}
.splash-wrap h1 {{
    color: white; font-size: 24px; font-weight: 800; margin: 0; letter-spacing: -0.01em;
}}
.splash-wrap .splash-sub {{
    color: {GOLD}; font-style: italic; font-weight: 600; font-size: 14px; margin: 6px 0 0 0;
}}
.splash-wrap .splash-tag {{
    color: rgba(255,255,255,0.65); font-size: 12.5px; margin: 22px 0 14px 0;
    text-transform: uppercase; letter-spacing: .12em; font-weight: 600;
}}
@keyframes logoPulse {{
    0% {{ transform: scale(0.85); opacity: 0; }}
    50% {{ transform: scale(1.04); opacity: 1; }}
    100% {{ transform: scale(1); opacity: 1; }}
}}
.splash-wrap img, .splash-wrap .splash-fallback-logo {{
    animation: logoPulse 0.9s ease-out;
}}
.loading-bar-track {{
    width: 180px; height: 4px; background: rgba(255,255,255,0.15);
    border-radius: 4px; margin: 18px auto 6px auto; overflow: hidden;
}}
.loading-bar-fill {{
    height: 100%; width: 0%; background: linear-gradient(90deg, {GOLD}, {CRIMSON});
    border-radius: 4px; animation: loadFill 1.8s ease forwards;
}}
@keyframes loadFill {{ from {{ width: 0%; }} to {{ width: 100%; }} }}
.loading-text {{
    color: rgba(255,255,255,0.55); font-size: 11px; letter-spacing: .05em;
}}
.loading-text span {{
    animation: dotFade 1.4s infinite; opacity: 0;
}}
.loading-text span:nth-child(1) {{ animation-delay: 0s; }}
.loading-text span:nth-child(2) {{ animation-delay: 0.2s; }}
.loading-text span:nth-child(3) {{ animation-delay: 0.4s; }}
@keyframes dotFade {{ 0%, 100% {{ opacity: 0; }} 50% {{ opacity: 1; }} }}
.feature-chip {{
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15);
    border-radius: 999px; padding: 7px 14px; margin: 4px; font-size: 12.5px;
    color: white; font-weight: 500;
}}

/* ---------- Calendar ---------- */
.cal-row {{
    display: flex; align-items: center; gap: 14px; background: white;
    border-radius: 14px; padding: 12px 16px; margin-bottom: 9px;
    border: 1px solid #E7EEF6; box-shadow: 0 2px 10px rgba(15,30,51,0.05);
}}
.cal-chip {{
    min-width: 56px; text-align: center; border-radius: 10px; padding: 6px 4px;
    color: white; font-family: 'Poppins', sans-serif;
}}
.cal-chip .d {{ font-size: 16px; font-weight: 800; line-height: 1; }}
.cal-chip .m {{ font-size: 9.5px; letter-spacing: .06em; opacity: 0.85; }}

/* ---------- Achievements ---------- */
.ach-card {{
    background: white; border-radius: 16px; padding: 18px; margin-bottom: 12px;
    border: 1px solid #E7EEF6; box-shadow: 0 2px 10px rgba(15,30,51,0.06);
    display: flex; gap: 14px; align-items: flex-start;
}}
.ach-icon {{
    font-size: 22px; width: 46px; height: 46px; border-radius: 12px; flex-shrink: 0;
    background: linear-gradient(135deg, {GOLD} 0%, #b87f1f 100%);
    display: flex; align-items: center; justify-content: center;
}}

/* ---------- Notification badge ---------- */
.notif-dot {{
    background: {CRIMSON}; color: white; border-radius: 999px; font-size: 11px;
    font-weight: 700; padding: 1px 7px; margin-left: 6px;
}}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------
# SCHOOL FACTS
# ---------------------------------------------------------------
SCHOOL = {
    "name": "Wampeewo Ntakke Secondary School",
    "motto": "Ekula Y'ebuuka",
    "founded": 1966,
    "location": "Gayaza Road, Wakiso, Uganda",
}

# ---------------------------------------------------------------
# SAMPLE STUDENT DATABASE — replace with your real register (CSV/DB)
# ---------------------------------------------------------------
STUDENTS = [
    {"name": "Nantongo Patricia", "klass": "S4 Science", "admission_no": "WNSS/2023/0417",
     "guardian": "Mr. Ssebagala Robert", "attendance_pct": 96,
     "fees_billed": 850000, "fees_paid": 600000, "rank": 6, "out_of": 42,
     "subjects": [("Mathematics", 61, 74), ("Biology", 70, 78), ("Chemistry", 55, 63),
                  ("Physics", 58, 60), ("English", 72, 80), ("Geography", 66, 71)]},
    {"name": "Okello Brian", "klass": "S2 East", "admission_no": "WNSS/2024/0182",
     "guardian": "Mrs. Okello Joyce", "attendance_pct": 89,
     "fees_billed": 620000, "fees_paid": 620000, "rank": 14, "out_of": 38,
     "subjects": [("Mathematics", 48, 55), ("Biology", 60, 64), ("English", 52, 58),
                  ("History", 70, 72), ("CRE", 80, 84)]},
    {"name": "Namutebi Sarah", "klass": "S6 Arts", "admission_no": "WNSS/2021/0099",
     "guardian": "Mr. Namutebi Henry", "attendance_pct": 98,
     "fees_billed": 950000, "fees_paid": 950000, "rank": 2, "out_of": 30,
     "subjects": [("Economics", 78, 85), ("Literature", 81, 88), ("Geography", 75, 79),
                  ("CRE", 80, 83)]},
    {"name": "Mukasa David", "klass": "S1 West", "admission_no": "WNSS/2026/0301",
     "guardian": "Mr. Mukasa Fred", "attendance_pct": 92,
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

ACHIEVEMENTS = [
    {"icon": "🏆", "title": "Best STEM School — Wakiso District 2025",
     "body": "Recognised for the school's STEM club projects, including the mosquito-trap "
             "innovation showcased at the regional science fair."},
    {"icon": "📚", "title": "96% UCE pass rate — 2025",
     "body": "S4 candidates posted the school's strongest UCE results in five years, with "
             "12 students attaining first grade."},
    {"icon": "🥇", "title": "Wakiso Inter-school Athletics — Champions", "body":
     "The school's athletics team won the district inter-school championship for the second "
     "year running."},
    {"icon": "🎭", "title": "Best Cultural Dance — Buganda Region",
     "body": "The school's cultural troupe took first place at the regional Buganda cultural "
             "competition."},
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
            headers={
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": "claude-sonnet-4-6",
                "max_tokens": 600,
                "system": system_prompt,
                "messages": [{"role": "user", "content": user_text}],
            },
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        return "".join(block.get("text", "") for block in data.get("content", [])).strip() or "No response."
    except Exception as e:
        return f"⚠️ AI request failed: {e}"


def money(n):
    return f"UGX {n:,.0f}"


# ---------------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------------
if "student" not in st.session_state:
    st.session_state.student = None
if "chat" not in st.session_state:
    st.session_state.chat = []
if "entered" not in st.session_state:
    st.session_state.entered = False
if "read_ids" not in st.session_state:
    st.session_state.read_ids = set()
if "toasted_for" not in st.session_state:
    st.session_state.toasted_for = None

# ---------------------------------------------------------------
# SPLASH / LAUNCH SCREEN — first thing a parent sees, every visit
# ---------------------------------------------------------------
if not st.session_state.entered:
    splash_logo = (
        f'<img src="data:image/png;base64,{logo_b64}" />'
        if logo_b64 else
        '<div class="splash-fallback-logo" style="width:110px;height:110px;border-radius:50%;background:white;display:flex;'
        'align-items:center;justify-content:center;font-weight:800;color:#06264D;font-size:13px;margin:0 auto 18px auto;">WNSS</div>'
    )
    st.markdown(f"""
    <div class="splash-wrap">
        {splash_logo}
        <h1>{SCHOOL['name']}</h1>
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
# HERO HEADER (always visible once inside the app)
# ---------------------------------------------------------------
logo_img_tag = (
    f'<img src="data:image/png;base64,{logo_b64}" />'
    if logo_b64 else
    '<div style="width:78px;height:78px;border-radius:50%;background:white;display:flex;'
    'align-items:center;justify-content:center;font-weight:800;color:#06264D;font-size:11px;">WNSS</div>'
)

st.markdown(f"""
<div class="hero">
    {logo_img_tag}
    <div class="hero-text">
        <h1>{SCHOOL['name']}</h1>
        <p class="motto">"{SCHOOL['motto']}"</p>
        <p class="sub">📍 {SCHOOL['location']} &nbsp;·&nbsp; Est. {SCHOOL['founded']} &nbsp;·&nbsp; Parent Portal</p>
    </div>
</div>
<div class="accent-bar"></div>
""", unsafe_allow_html=True)

if not logo_b64:
    st.caption("💡 Drop your real school badge into the repo as `logo.png` to replace the placeholder above.")

# ---------------------------------------------------------------
# STUDENT SEARCH
# ---------------------------------------------------------------
if st.session_state.student is None:
    st.markdown('<div class="section-label">🔍 FIND YOUR CHILD</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([3, 2])
    with col1:
        query = st.text_input("Search", placeholder="Type your child's name — e.g. Nantongo, Okello, Sarah...",
                               label_visibility="collapsed")

        if query:
            matches = STUDENTS_DF[STUDENTS_DF["name"].str.contains(query, case=False, na=False)]
            if matches.empty:
                st.info("No student found with that name in this demo database. "
                        "Connect your real student register to search live records.")
            else:
                for _, row in matches.iterrows():
                    st.markdown(f"""
                    <div class="card" style="display:flex;align-items:center;justify-content:space-between;">
                        <div>
                            <div style="font-weight:700;color:{NAVY};font-size:15px;">{row['name']}</div>
                            <div style="color:{SLATE};font-size:12.5px;">{row['klass']} · Adm. {row['admission_no']} · Guardian: {row['guardian']}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"View {row['name'].split()[0]}'s record →", key=row["admission_no"]):
                        st.session_state.student = row.to_dict()
                        st.rerun()
        else:
            st.caption("⚠️ Sample database of 4 demo students. Swap `STUDENTS` for your real register to go live.")
    with col2:
        st.markdown(f"""
        <div class="card">
            <div class="section-label" style="margin-top:0;">ℹ️ ABOUT THIS PORTAL</div>
            <p style="color:{SLATE};font-size:13px;line-height:1.6;">
            One place for parents to check attendance, fees, grades, and school notices —
            with an AI assistant that can answer questions about your own child's record instantly,
            in English, Luganda, or Swahili.
            </p>
        </div>
        """, unsafe_allow_html=True)
    st.stop()

# ---------------------------------------------------------------
# STUDENT DASHBOARD
# ---------------------------------------------------------------
s = st.session_state.student
balance = s["fees_billed"] - s["fees_paid"]

# Simulate a real-time push notification the first time this student's dashboard loads
if st.session_state.toasted_for != s["admission_no"]:
    urgent = next((n for n in NOTICES if n["category"] == "emergency"), None)
    if urgent:
        st.toast(f"🔔 {urgent['title']}", icon="🚨")
    st.session_state.toasted_for = s["admission_no"]

unread_count = len([n for n in NOTICES if n["id"] not in st.session_state.read_ids])

bcol1, bcol2 = st.columns([5, 1])
with bcol1:
    st.markdown(f"""
    <div class="student-banner">
        <div>
            <div class="name">👤 {s['name']} <span style="color:{SLATE};font-weight:500;">· {s['klass']}</span></div>
            <div class="meta">Admission no. {s['admission_no']} · Guardian on record: {s['guardian']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
with bcol2:
    if st.button("🔄 Switch", use_container_width=True):
        st.session_state.student = None
        st.session_state.chat = []
        st.rerun()

tabs = st.tabs([
    "🏠 Overview",
    f"🔔 Notifications" + (f" ({unread_count})" if unread_count else ""),
    "📅 Calendar",
    "💰 Fees",
    "📊 Report Card",
    "✅ Attendance",
    "🏆 Achievements",
    "🤖 AI Assistant",
])

# --- Overview ---
with tabs[0]:
    c1, c2, c3 = st.columns(3)
    stats = [
        (c1, "📅", "Attendance", f"{s['attendance_pct']}%"),
        (c2, "💵", "Fee balance", money(balance)),
        (c3, "🏅", "Class rank", f"{s['rank']} of {s['out_of']}"),
    ]
    for col, icon, label, value in stats:
        col.markdown(f"""
        <div class="stat-card">
            <div class="icon">{icon}</div>
            <div class="value">{value}</div>
            <div class="label">{label}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-label" style="margin-top:20px;">✨ AI DAILY BRIEFING</div>', unsafe_allow_html=True)
    st.markdown(f"""<div class="card" style="background:linear-gradient(135deg,{NAVY} 0%,{BLUE} 100%);color:white;">""",
                unsafe_allow_html=True)
    if st.button("Generate today's briefing", key="briefing_btn"):
        briefing_prompt = (
            f"Attendance {s['attendance_pct']}%. Fee balance {money(balance)} due 30 June. "
            f"Class rank {s['rank']} of {s['out_of']}. Latest notice: '{NOTICES[0]['title']}'. "
            "Write a warm 2-sentence daily briefing for the parent covering anything that needs attention."
        )
        st.session_state["_briefing"] = ask_claude(
            "You write a short, warm daily briefing (max 2 sentences) for a parent, flagging only what matters.",
            briefing_prompt,
        )
    st.write(st.session_state.get("_briefing", "Tap the button for a 2-sentence AI summary of everything that needs your attention today."))
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="section-label" style="margin-top:20px;">📌 LATEST NOTICE</div>', unsafe_allow_html=True)
    n = NOTICES[1]
    st.markdown(f"""
    <div class="notice-card {n['category']}">
        <span class="pill pill-{n['category']}">{n['category'].title()}</span>
        <div class="notice-title">{n['title']}</div>
        <div style="color:{SLATE};font-size:13.5px;line-height:1.55;">{n['body']}</div>
        <div class="notice-time" style="margin-top:8px;">{n['time']}</div>
    </div>
    """, unsafe_allow_html=True)

# --- Notifications ---
with tabs[1]:
    top_l, top_r = st.columns([3, 1])
    with top_l:
        st.markdown(f'<div class="section-label" style="margin-top:0;">🔔 {unread_count} UNREAD</div>'
                    if unread_count else '<div class="section-label" style="margin-top:0;">✅ ALL CAUGHT UP</div>',
                    unsafe_allow_html=True)
    with top_r:
        if st.button("Mark all read", use_container_width=True):
            st.session_state.read_ids = {n["id"] for n in NOTICES}
            st.rerun()

    for n in NOTICES:
        is_unread = n["id"] not in st.session_state.read_ids
        dot = "🔵 " if is_unread else ""
        st.markdown(f"""
        <div class="notice-card {n['category']}">
            <span class="pill pill-{n['category']}">{n['category'].title()}</span>
            <span class="notice-time" style="float:right;">{n['time']}</span>
            <div class="notice-title">{dot}{n['title']}</div>
            <div style="color:{SLATE};font-size:13.5px;line-height:1.55;">{n['body']}</div>
        </div>
        """, unsafe_allow_html=True)
        bcols = st.columns([1, 1, 4])
        with bcols[0]:
            if st.button("✨ AI summary", key=f"sum_{n['id']}"):
                summary = ask_claude(
                    "Shorten this school announcement into one calm, plain sentence for a parent, under 25 words.",
                    n["body"],
                )
                st.success(summary)
        with bcols[1]:
            if is_unread and st.button("Mark read", key=f"read_{n['id']}"):
                st.session_state.read_ids.add(n["id"])
                st.rerun()

# --- Calendar ---
with tabs[2]:
    st.markdown('<div class="section-label" style="margin-top:0;">📅 TERM 2 — 2026</div>', unsafe_allow_html=True)
    chip_color = {"emergency": CRIMSON, "fees": GOLD, "exam": NAVY, "event": "#2E86C1", "meeting": BLUE}
    for e in EVENTS:
        col = chip_color.get(e["tag"], BLUE)
        st.markdown(f"""
        <div class="cal-row">
            <div class="cal-chip" style="background:{col};">
                <div class="d">{e['date'].split()[0]}</div>
                <div class="m">{e['month']}</div>
            </div>
            <div style="font-weight:600;color:{INK};font-size:14px;">{e['label']}</div>
        </div>
        """, unsafe_allow_html=True)

# --- Fees ---
with tabs[3]:
    pct_paid = s["fees_paid"] / s["fees_billed"]
    st.markdown(f"""
    <div class="card">
        <div class="section-label" style="margin-top:0;">💰 TERM 2 BALANCE</div>
        <div style="font-family:'Poppins',sans-serif;font-size:32px;font-weight:800;color:{CRIMSON_DARK};">{money(balance)}</div>
        <div style="color:{SLATE};font-size:12.5px;margin-bottom:10px;">Due 30 June 2026</div>
    </div>
    """, unsafe_allow_html=True)
    st.progress(pct_paid, text=f"{pct_paid*100:.0f}% paid · {money(s['fees_paid'])} of {money(s['fees_billed'])}")

    st.markdown('<div class="section-label" style="margin-top:18px;">🧾 PAYMENT HISTORY</div>', unsafe_allow_html=True)
    history = pd.DataFrame([
        {"Date": "14 May 2026", "Method": "MTN Mobile Money", "Amount": money(300000), "Ref": "MM240514.0091"},
        {"Date": "02 Apr 2026", "Method": "Bank deposit", "Amount": money(300000), "Ref": "CB-220409-77"},
    ])
    st.dataframe(history, use_container_width=True, hide_index=True)
    st.download_button(
        "⬇️ Download last receipt",
        data=f"WAMPEEWO NTAKKE SECONDARY SCHOOL\nStudent: {s['name']}\nAmount: {money(300000)}\n"
             f"Method: MTN Mobile Money\nDate: 14 May 2026\nRef: MM240514.0091\n",
        file_name="receipt.txt",
    )

# --- Report Card ---
with tabs[4]:
    avg = round(sum(f for _, _, f in s["subjects"]) / len(s["subjects"]), 1)

    def letter_grade(score):
        if score >= 80: return "A"
        if score >= 70: return "B"
        if score >= 60: return "C"
        if score >= 50: return "D"
        return "F"

    st.markdown(f"""
    <div class="card">
        <div class="section-label" style="margin-top:0;">📊 OFFICIAL REPORT CARD — TERM 2, 2026</div>
        <div style="display:flex;gap:28px;flex-wrap:wrap;">
            <div>
                <div style="font-family:'Poppins',sans-serif;font-size:24px;font-weight:800;color:{NAVY};">
                    Position {s['rank']} <span style="color:{SLATE};font-size:14px;font-weight:600;">of {s['out_of']}</span>
                </div>
                <div style="color:{SLATE};font-size:12px;">Class rank</div>
            </div>
            <div>
                <div style="font-family:'Poppins',sans-serif;font-size:24px;font-weight:800;color:{NAVY};">{avg}%</div>
                <div style="color:{SLATE};font-size:12px;">Average final score</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    for name, mid, fin in s["subjects"]:
        up = fin >= mid
        arrow_color = BLUE if up else CRIMSON
        arrow = "↑" if up else "↓"
        grade = letter_grade(fin)
        st.markdown(f"""
        <div class="card" style="display:flex;align-items:center;justify-content:space-between;padding:14px 20px;">
            <div style="display:flex;align-items:center;gap:12px;">
                <div style="width:34px;height:34px;border-radius:9px;background:{SKY};color:{NAVY};
                            display:flex;align-items:center;justify-content:center;font-weight:800;font-size:13px;">{grade}</div>
                <div style="font-weight:600;color:{INK};">{name}</div>
            </div>
            <div style="font-family:'Poppins',sans-serif;font-weight:700;color:{arrow_color};">
                {mid} → {fin} <span style="font-size:13px;">{arrow}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    report_text = (
        f"{SCHOOL['name']}\nOFFICIAL REPORT CARD — TERM 2, 2026\n"
        f"Student: {s['name']}\nClass: {s['klass']}\nAdmission No: {s['admission_no']}\n"
        f"Class Position: {s['rank']} of {s['out_of']}\nAverage Score: {avg}%\n\n"
        + "\n".join(f"{name}: midterm {mid} -> final {fin} (Grade {letter_grade(fin)})" for name, mid, fin in s["subjects"])
        + "\n\nClass teacher's comment: Keep up the consistent effort and continue revising past papers ahead of finals."
    )
    st.download_button("⬇️ Download report card", data=report_text,
                        file_name=f"{s['name'].replace(' ', '_')}_report_card.txt")

# --- Attendance ---
with tabs[5]:
    st.markdown(f"""
    <div class="card">
        <div class="section-label" style="margin-top:0;">📅 THIS TERM</div>
        <div style="font-family:'Poppins',sans-serif;font-size:32px;font-weight:800;color:{NAVY};">{s['attendance_pct']}% present</div>
    </div>
    """, unsafe_allow_html=True)
    log = [
        ("Mon 22 Jun", "Present", "🟢"), ("Tue 23 Jun", "Present", "🟢"),
        ("Wed 24 Jun", "Late — arrived 8:40am", "🟡"), ("Thu 18 Jun", "Absent — no reason given", "🔴"),
        ("Wed 17 Jun", "Present", "🟢"), ("Tue 16 Jun", "Present", "🟢"),
    ]
    for date, status, icon in log:
        st.markdown(f"""
        <div class="card" style="display:flex;align-items:center;gap:12px;padding:12px 18px;">
            <span style="font-size:16px;">{icon}</span>
            <div><b>{date}</b> — <span style="color:{SLATE};">{status}</span></div>
        </div>
        """, unsafe_allow_html=True)

# --- Achievements ---
with tabs[6]:
    st.markdown('<div class="section-label" style="margin-top:0;">🏆 SCHOOL ACHIEVEMENTS</div>', unsafe_allow_html=True)
    st.caption("Sample achievements — replace with your school's real wins, trophies and results.")
    for a in ACHIEVEMENTS:
        st.markdown(f"""
        <div class="ach-card">
            <div class="ach-icon">{a['icon']}</div>
            <div>
                <div style="font-weight:700;color:{NAVY};font-size:14.5px;">{a['title']}</div>
                <div style="color:{SLATE};font-size:13px;line-height:1.55;margin-top:3px;">{a['body']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# --- AI Assistant ---
with tabs[7]:
    st.markdown(f"""
    <div class="card" style="display:flex;align-items:center;gap:10px;">
        <div style="width:38px;height:38px;border-radius:50%;background:{NAVY};display:flex;align-items:center;justify-content:center;font-size:16px;">✨</div>
        <div>
            <div style="font-weight:700;color:{NAVY};">Parent AI Assistant</div>
            <div style="color:{SLATE};font-size:12px;">Answers using {s['name']}'s live record</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    system_prompt = (
        "You are the Parent AI Assistant for a Ugandan secondary school. Speak warmly and briefly "
        "(2-5 sentences). Use UGX for money. Only use this student record, never invent numbers:\n"
        f"Name: {s['name']}, Class: {s['klass']}\n"
        f"Attendance: {s['attendance_pct']}% this term\n"
        f"Fees: billed {s['fees_billed']} UGX, paid {s['fees_paid']} UGX, "
        f"balance {balance} UGX, due 30 June 2026\n"
        f"Class rank: {s['rank']} of {s['out_of']}\n"
        f"Subjects (midterm->final): {', '.join(f'{n} {m}->{f}' for n, m, f in s['subjects'])}\n"
        "If asked something outside this record, say you don't have that information and suggest "
        "messaging the class teacher or office."
    )

    for msg in st.session_state.chat:
        with st.chat_message(msg["role"]):
            st.write(msg["text"])

    cols = st.columns(3)
    suggestions = ["When are the next exams?", "What is my child's attendance?", "How much fees remain?"]
    for col, sug in zip(cols, suggestions):
        if col.button(sug, key=f"sug_{sug}"):
            st.session_state.chat.append({"role": "user", "text": sug})
            reply = ask_claude(system_prompt, sug)
            st.session_state.chat.append({"role": "assistant", "text": reply})
            st.rerun()

    user_input = st.chat_input("Ask about fees, attendance, exams…")
    if user_input:
        st.session_state.chat.append({"role": "user", "text": user_input})
        reply = ask_claude(system_prompt, user_input)
        st.session_state.chat.append({"role": "assistant", "text": reply})
        st.rerun()

    st.divider()
    lang = st.selectbox("Translate the assistant's last reply to:", ["—", "Luganda", "Swahili", "English"])
    if lang != "—" and st.session_state.chat:
        last_reply = next((m["text"] for m in reversed(st.session_state.chat) if m["role"] == "assistant"), None)
        if last_reply and st.button("Translate"):
            translated = ask_claude(
                f"Translate this into {lang}, naturally and warmly. Output only the translation.",
                last_reply,
            )
            st.info(translated)
