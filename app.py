import streamlit as st
import pandas as pd
import requests
import base64, os, time, random
from datetime import datetime

st.set_page_config(page_title="Wampeewo Ntakke — Parent Portal", page_icon="🛡️", layout="wide")

NAVY   = "#06264D"; BLUE  = "#0B4F9E"; SKY   = "#EAF3FC"; BG    = "#F4F6F9"
CRIM   = "#C8102E"; CRIMD = "#8C0B20"; GOLD  = "#D7A33D"; INK   = "#10182B"
SLATE  = "#5B6B82"; WHITE = "#FFFFFF"; GREEN = "#1FAF54"

LOGO_PATH = "logo.png"
def get_b64(p):
    if os.path.exists(p):
        with open(p,"rb") as f: return base64.b64encode(f.read()).decode()
    return None
logo_b64 = get_b64(LOGO_PATH)

# ── STYLES ──────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap');
html,body,[class*="css"]{{font-family:'Inter',sans-serif;}}
h1,h2,h3,h4{{font-family:'Poppins',sans-serif;}}
.stApp{{background:{BG};}}
#MainMenu{{visibility:hidden;}} footer{{visibility:hidden;}}
header[data-testid="stHeader"]{{display:none!important;}}
[data-testid="stToolbar"]{{display:none!important;}}
[data-testid="stDecoration"]{{display:none!important;}}
.stDeployButton{{display:none!important;}}
#stDecoration{{display:none!important;}}
.block-container{{padding-bottom:90px!important;padding-top:0.6rem!important;max-width:720px;}}

/* Top bar */
.topbar{{display:flex;align-items:center;justify-content:space-between;margin-bottom:12px;}}
.topbar img{{width:38px;height:38px;border-radius:50%;object-fit:contain;background:white;padding:2px;box-shadow:0 2px 8px rgba(0,0,0,.12);}}
.topbar .fb{{width:38px;height:38px;border-radius:50%;background:{NAVY};color:white;font-size:9px;font-weight:800;display:flex;align-items:center;justify-content:center;}}
.topbar .tname{{font-family:'Poppins',sans-serif;font-weight:800;font-size:15px;color:{NAVY};line-height:1.1;}}
.topbar .ttag{{font-size:10.5px;color:{SLATE};}}
.bell{{position:relative;font-size:22px;}}
.bell-badge{{position:absolute;top:-5px;right:-5px;background:{GREEN};color:white;border-radius:50%;font-size:9px;font-weight:800;width:17px;height:17px;display:flex;align-items:center;justify-content:center;}}

/* Hero */
.hero{{background:linear-gradient(135deg,{NAVY},{BLUE});border-radius:16px;padding:16px 20px;
       margin-bottom:12px;display:flex;align-items:center;gap:14px;
       box-shadow:0 8px 24px rgba(6,38,77,.22);}}
.hero img{{width:58px;height:58px;border-radius:50%;background:white;padding:3px;object-fit:contain;flex-shrink:0;}}
.hero .hfb{{width:58px;height:58px;border-radius:50%;background:rgba(255,255,255,.15);color:white;font-weight:800;font-size:10px;display:flex;align-items:center;justify-content:center;flex-shrink:0;}}
.hero h2{{color:white;font-size:16px;font-weight:800;margin:0;}}
.hero .hsub{{color:rgba(255,255,255,.75);font-size:10.5px;margin-top:2px;}}
.hero .hmotto{{color:{GOLD};font-style:italic;font-size:11px;margin-top:1px;}}

/* Action strip */
.act-strip{{background:white;border-radius:16px;padding:14px 10px 10px 10px;
            margin-bottom:12px;box-shadow:0 2px 10px rgba(15,30,51,.06);border:1px solid #ECEFF3;}}
/* hide the Streamlit button default styling inside action strip */
.act-strip .stButton>button{{
    background:transparent!important;border:none!important;box-shadow:none!important;
    padding:0!important;height:auto!important;color:{INK}!important;
    font-size:10.5px!important;font-weight:600!important;
    display:flex!important;flex-direction:column!important;align-items:center!important;
    gap:5px!important;width:100%!important;border-radius:0!important;
}}
.act-strip .stButton>button:hover{{background:transparent!important;color:{BLUE}!important;}}
.act-ic{{width:50px;height:50px;border-radius:14px;display:flex;align-items:center;
          justify-content:center;font-size:22px;margin:0 auto 4px auto;}}

/* Generic cards */
.card{{background:white;border-radius:14px;padding:16px 18px;
       box-shadow:0 2px 10px rgba(15,30,51,.05);border:1px solid #ECEFF3;margin-bottom:10px;}}
.acct-card{{background:white;border-radius:16px;padding:16px 18px;margin-bottom:12px;
            box-shadow:0 2px 10px rgba(15,30,51,.06);border:1px solid #ECEFF3;}}

/* Stats row */
.stat-row{{display:flex;gap:8px;margin-bottom:12px;}}
.stat-mini{{background:white;border-radius:12px;flex:1;padding:12px 8px;
            box-shadow:0 2px 8px rgba(15,30,51,.05);border:1px solid #ECEFF3;text-align:center;}}
.stat-mini .sv{{font-family:'Poppins',sans-serif;font-size:17px;font-weight:800;color:{NAVY};}}
.stat-mini .sl{{font-size:9.5px;color:{SLATE};font-weight:600;text-transform:uppercase;letter-spacing:.04em;}}

/* Highlights carousel */
.hl-wrap{{display:flex;gap:10px;overflow-x:auto;padding:2px 2px 10px 2px;scrollbar-width:none;margin-bottom:12px;}}
.hl-wrap::-webkit-scrollbar{{display:none;}}
.hl-card{{min-width:160px;height:110px;border-radius:14px;flex-shrink:0;position:relative;
          display:flex;flex-direction:column;justify-content:flex-end;padding:10px 12px;
          cursor:pointer;overflow:hidden;}}
.hl-card .hlov{{position:absolute;inset:0;border-radius:14px;
                background:linear-gradient(to top,rgba(0,0,0,.7) 0%,rgba(0,0,0,.05) 60%);}}
.hl-card .hltx{{position:relative;z-index:1;}}
.hl-card .hltit{{color:white;font-weight:700;font-size:13px;line-height:1.2;}}
.hl-card .hlsub{{color:rgba(255,255,255,.8);font-size:10px;margin-top:2px;}}

/* Notices */
.nc{{background:white;border-radius:12px;padding:14px 16px;margin-bottom:9px;
     border-left:5px solid {BLUE};box-shadow:0 2px 8px rgba(15,30,51,.05);}}
.nc.emergency{{border-left-color:{CRIM};background:#FDF2F3;}}
.nc.fees{{border-left-color:{GOLD};}}
.nc.exam{{border-left-color:{NAVY};}}
.nc.event{{border-left-color:#2E86C1;}}
.pill{{display:inline-block;padding:2px 9px;border-radius:999px;font-size:10px;font-weight:700;text-transform:uppercase;}}
.pill-emergency{{background:{CRIM};color:white;}}
.pill-meeting{{background:{BLUE};color:white;}}
.pill-exam{{background:{NAVY};color:white;}}
.pill-fees{{background:{GOLD};color:#3a2a05;}}
.pill-event{{background:#2E86C1;color:white;}}
.ntit{{font-weight:700;color:{INK};margin:7px 0 3px 0;font-size:14px;}}

/* Section label */
.slabel{{font-family:'Poppins',sans-serif;font-weight:700;font-size:11.5px;
          text-transform:uppercase;letter-spacing:.08em;color:{SLATE};margin:4px 0 9px 0;}}

/* iOS-style action strip */
.ios-sw{{background:white;border-radius:16px;padding:14px 6px 0 6px;margin-bottom:0;
          box-shadow:0 2px 10px rgba(15,30,51,.06);border:1px solid #ECEFF3;}}
/* The st.columns block rendered right after .ios-sw */
.ios-sw + div [data-testid="stHorizontalBlock"],
.ios-sw ~ div [data-testid="stHorizontalBlock"]{{
    overflow-x:auto!important;flex-wrap:nowrap!important;
    scrollbar-width:none!important;
    padding:0 4px 14px 4px!important;
    gap:2px!important;
}}
.ios-sw + div [data-testid="stHorizontalBlock"]::-webkit-scrollbar{{display:none;}}
.ios-sw + div [data-testid="stColumn"],
.ios-sw ~ div [data-testid="stColumn"]{{
    min-width:72px!important;max-width:72px!important;
    flex:0 0 72px!important;padding:0 2px!important;
}}
/* Buttons inside the strip */
.ios-sw + div button, .ios-sw ~ div button,
.ios-sw + div [data-testid="stColumn"] button,
.ios-sw ~ div [data-testid="stColumn"] button {{
    background:transparent!important;border:none!important;
    box-shadow:none!important;outline:none!important;
    color:{INK}!important;font-size:10.5px!important;font-weight:700!important;
    padding:0 2px 5px!important;min-height:0!important;height:auto!important;
    width:100%!important;text-align:center!important;border-radius:10px!important;
}}

/* Bottom nav */
div[data-testid="stVerticalBlockBorderWrapper"]:has(div.navmarker){{
    position:fixed;bottom:0;left:0;right:0;z-index:999;
    background:white;box-shadow:0 -2px 12px rgba(0,0,0,.09);
    border-top:1px solid #E8EDF3;
    padding:4px 6px calc(env(safe-area-inset-bottom)+4px) 6px;
    max-width:720px;margin:0 auto;border:none!important;
}}
div[data-testid="stVerticalBlockBorderWrapper"]:has(div.navmarker)>div{{border:none!important;}}
.navmarker{{display:none;}}
div[data-testid="stVerticalBlockBorderWrapper"]:has(div.navmarker) button{{
    background:transparent!important;border:none!important;box-shadow:none!important;
    color:{SLATE}!important;font-size:10px!important;font-weight:600!important;
    padding:6px 2px!important;border-radius:8px!important;
}}
div[data-testid="stVerticalBlockBorderWrapper"]:has(div.navmarker) button[kind="primary"]{{
    color:{BLUE}!important;background:{SKY}!important;
}}
/* Chat */
[data-testid="stChatMessage"]{{background:white;border-radius:12px;border:1px solid #ECEFF3;}}

/* Splash */
@keyframes fadeUp{{from{{opacity:0;transform:translateY(16px);}}to{{opacity:1;transform:translateY(0);}}}}
@keyframes logoPulse{{0%{{transform:scale(.8);opacity:0;}}60%{{transform:scale(1.05);opacity:1;}}100%{{transform:scale(1);opacity:1;}}}}
@keyframes loadFill{{from{{width:0;}}to{{width:100%;}}}}
@keyframes dotFade{{0%,100%{{opacity:0;}}50%{{opacity:1;}}}}
@keyframes fadeIn{{from{{opacity:0;}}to{{opacity:1;}}}}
.splash{{background:radial-gradient(circle at 30% 20%,{BLUE},{NAVY} 55%,#02152e);
          border-radius:20px;padding:60px 32px 48px;text-align:center;
          animation:fadeUp .5s ease-out;box-shadow:0 16px 40px rgba(6,38,77,.35);}}
.splash img{{width:120px;height:120px;border-radius:50%;background:white;padding:6px;
             object-fit:contain;box-shadow:0 8px 28px rgba(0,0,0,.35);margin-bottom:20px;
             animation:logoPulse 1.1s ease-out;}}
.splash .sfb{{width:120px;height:120px;border-radius:50%;background:rgba(255,255,255,.12);
              border:3px solid rgba(255,255,255,.25);display:flex;align-items:center;
              justify-content:center;font-weight:800;color:white;font-size:14px;
              margin:0 auto 20px;animation:logoPulse 1.1s ease-out;}}
.splash h1{{color:white;font-size:22px;font-weight:800;margin:0;animation:fadeIn 1s .4s both;}}
.splash .sm{{color:{GOLD};font-style:italic;font-weight:600;font-size:13px;margin:6px 0 0;animation:fadeIn 1s .6s both;}}
.splash .sl{{color:rgba(255,255,255,.6);font-size:11px;margin:4px 0 0;animation:fadeIn 1s .8s both;}}
.splash .stag{{color:rgba(255,255,255,.6);font-size:11px;margin:22px 0 12px;text-transform:uppercase;letter-spacing:.14em;font-weight:700;animation:fadeIn 1s 1s both;}}
.lbt{{width:200px;height:4px;background:rgba(255,255,255,.15);border-radius:4px;margin:18px auto 7px;overflow:hidden;animation:fadeIn 1s 1s both;}}
.lbf{{height:100%;width:0;background:linear-gradient(90deg,{GOLD},{CRIM});border-radius:4px;animation:loadFill 4.6s cubic-bezier(.4,0,.2,1) forwards;}}
.ltx{{color:rgba(255,255,255,.5);font-size:10px;letter-spacing:.06em;animation:fadeIn 1s 1s both;}}
.ltx span{{animation:dotFade 1.4s infinite;opacity:0;}}
.ltx span:nth-child(1){{animation-delay:0s;}}
.ltx span:nth-child(2){{animation-delay:.25s;}}
.ltx span:nth-child(3){{animation-delay:.5s;}}

/* Report card */
.rc-row{{background:white;border-radius:12px;display:flex;align-items:center;
          justify-content:space-between;padding:12px 16px;margin-bottom:8px;
          border:1px solid #ECEFF3;box-shadow:0 1px 6px rgba(15,30,51,.04);}}
.grade-box{{width:32px;height:32px;border-radius:8px;background:{SKY};color:{NAVY};
            display:flex;align-items:center;justify-content:center;font-weight:800;font-size:12px;}}
</style>
""", unsafe_allow_html=True)

# ── DATA ─────────────────────────────────────────────────────────
SCHOOL = {"name":"Wampeewo Ntakke SS","full":"Wampeewo Ntakke Secondary School",
          "motto":"Ekula Y'ebuuka","founded":1966,"loc":"Gayaza Road, Wakiso, Uganda"}

STUDENTS = [
  {"name":"Mawanda Ronald","klass":"S4 Science","level":"S4","stream":"Science",
   "adm":"WNSS/2023/0417","code":"WN-0417","guardian":"Mr. Mawanda Joseph",
   "phone":"+256 700 501 001","att":96,"billed":850000,"paid":600000,"rank":6,"of":42,
   "subs":[("Mathematics",61,74),("Biology",70,78),("Chemistry",55,63),
           ("Physics",58,60),("English",72,80),("Geography",66,71)]},
  {"name":"Ssekyondwa Simon","klass":"S2 East","level":"S2","stream":"East",
   "adm":"WNSS/2024/0182","code":"WN-0182","guardian":"Mrs. Ssekyondwa Grace",
   "phone":"+256 752 220 884","att":89,"billed":620000,"paid":620000,"rank":5,"of":38,
   "subs":[("Mathematics",68,75),("Biology",60,64),("English",62,70),
           ("History",70,74),("CRE",80,84)]},
  {"name":"Wampona Kenneth","klass":"S6 Arts","level":"S6","stream":"Arts",
   "adm":"WNSS/2021/0099","code":"WN-0099","guardian":"Mr. Wampona Charles",
   "phone":"+256 772 901 233","att":98,"billed":950000,"paid":950000,"rank":2,"of":30,
   "subs":[("Economics",78,85),("Literature",81,88),("Geography",75,79),("CRE",80,83)]},
  {"name":"Nakayima Brenda","klass":"S1 West","level":"S1","stream":"West",
   "adm":"WNSS/2026/0301","code":"WN-0301","guardian":"Mrs. Nakayima Rose",
   "phone":"+256 701 887 410","att":92,"billed":540000,"paid":270000,"rank":9,"of":45,
   "subs":[("Mathematics",50,54),("Science",58,61),("English",60,65),("Social Studies",66,70)]},
]
SDF = pd.DataFrame(STUDENTS)

NOTICES = [
  {"id":1,"cat":"emergency","time":"Today, 7:05 AM",
   "title":"School closed Friday — heavy rain flooding",
   "body":"Due to flooding along Gayaza Road the school will remain closed this Friday 26 June. Day scholars should not report. Boarding students remain on campus. Updates follow Sunday evening."},
  {"id":2,"cat":"meeting","time":"Yesterday, 4:30 PM",
   "title":"S4 Parents' Meeting — Friday 2:00 PM",
   "body":"All parents and guardians of S4 students are invited to a meeting in the main hall this Friday at 2:00 PM to discuss UCE registration and mock exam performance."},
  {"id":3,"cat":"exam","time":"Mon, 22 Jun",
   "title":"End of Term 2 exams begin 7 July",
   "body":"End of Term 2 examinations begin Monday 7 July and run for two weeks. Timetables are posted on the noticeboard and available from class teachers."},
  {"id":4,"cat":"fees","time":"Fri, 19 Jun",
   "title":"Term 2 balance deadline — 30 June",
   "body":"All outstanding Term 2 fee balances should be cleared by 30 June to allow students to sit end of term examinations without disruption."},
  {"id":5,"cat":"event","time":"Wed, 17 Jun",
   "title":"Inter-house sports day — 12 July",
   "body":"The annual inter-house sports day will be held on 12 July from 8:30 AM. Parents and guardians are warmly welcome to attend."},
]

EVENTS = [
  {"d":"26 Jun","m":"JUN","label":"School closed — flooding (day scholars)","tag":"emergency"},
  {"d":"27 Jun","m":"JUN","label":"Visiting Sunday","tag":"event"},
  {"d":"30 Jun","m":"JUN","label":"Fees deadline — Term 2 balance","tag":"fees"},
  {"d":"7 Jul", "m":"JUL","label":"End of Term 2 examinations begin","tag":"exam"},
  {"d":"12 Jul","m":"JUL","label":"Inter-house sports day","tag":"event"},
  {"d":"26 Jul","m":"JUL","label":"Term 2 closing day","tag":"meeting"},
]

HIGHLIGHTS = [
  {"id":1,"title":"UCE Results","emoji":"📚","c1":BLUE,  "c2":NAVY,
   "img":"highlight_1.jpg","detail":"96% UCE pass rate in 2025 — 12 students attained first grade."},
  {"id":2,"title":"Sports Day", "emoji":"🥇","c1":CRIM,  "c2":CRIMD,
   "img":"highlight_2.jpg","detail":"Wakiso District athletics champions two years running."},
  {"id":3,"title":"STEM Fair",  "emoji":"🔬","c1":"#2E86C1","c2":"#1B4F72",
   "img":"highlight_3.jpg","detail":"Best STEM School, Wakiso District 2025."},
  {"id":4,"title":"Cultural Day","emoji":"🎭","c1":GOLD, "c2":"#8C6510",
   "img":"highlight_4.jpg","detail":"First place, Buganda regional cultural dance."},
  {"id":5,"title":"Graduation", "emoji":"🎓","c1":NAVY, "c2":"#02152e",
   "img":"highlight_5.jpg","detail":"Annual S6 thanksgiving and graduation service 2026."},
]

THREADS_SEED = [
  {"id":1,"with":"Mrs. Nakimera — Class Teacher","messages":[
    {"from":"teacher","text":"Good morning. Mawanda did well in Chemistry today — 14/20.","time":"10:40 AM"},
    {"from":"parent","text":"Thank you Madam, we will keep encouraging him.","time":"10:42 AM"},
  ]},
  {"id":2,"with":"Bursar's Office","messages":[
    {"from":"teacher","text":"Reminder: Term 2 balance is due by 30 June.","time":"Yesterday"},
  ]},
  {"id":3,"with":"S4 Science — Class Group","group":True,"messages":[
    {"from":"teacher","text":"All S4 parents: Friday's meeting starts at 2:00 PM in the main hall.","time":"Mon"},
  ]},
]
PAY_HIST = [
  {"date":"14 May 2026","method":"MTN Mobile Money","amount":300000,"ref":"MM240514.0091"},
  {"date":"02 Apr 2026","method":"Bank deposit","amount":300000,"ref":"CB-220409-77"},
]

# ── HELPERS ──────────────────────────────────────────────────────
def ask_claude(sys_p, user_p):
    key = st.secrets.get("ANTHROPIC_API_KEY")
    if not key: return "⚠️ Add ANTHROPIC_API_KEY to Streamlit secrets."
    try:
        r = requests.post("https://api.anthropic.com/v1/messages",
            headers={"x-api-key":key,"anthropic-version":"2023-06-01","content-type":"application/json"},
            json={"model":"claude-sonnet-4-6","max_tokens":600,"system":sys_p,
                  "messages":[{"role":"user","content":user_p}]},timeout=30)
        r.raise_for_status()
        return "".join(b.get("text","") for b in r.json().get("content",[])).strip() or "No response."
    except Exception as e: return f"⚠️ {e}"

def money(n): return f"UGX {n:,.0f}"
def grade(s): return "A" if s>=80 else "B" if s>=70 else "C" if s>=60 else "D" if s>=50 else "F"
def bal(rec):
    extra = st.session_state.paid_extra.get(rec["adm"],0)
    return max(rec["billed"]-rec["paid"]-extra, 0)

# ── SESSION STATE ────────────────────────────────────────────────
for k,v in {"entered":False,"nav":"home","student":None,"chat":[],
            "read_ids":set(),"toasted":False,"threads":None,
            "active_thread":None,"paid_extra":{},"_receipt":None}.items():
    if k not in st.session_state: st.session_state[k]=v
if st.session_state.threads is None:
    st.session_state.threads=[dict(t,messages=list(t["messages"])) for t in THREADS_SEED]

# ── SPLASH ───────────────────────────────────────────────────────
if not st.session_state.entered:
    logo_tag = (f'<img src="data:image/png;base64,{logo_b64}"/>' if logo_b64
                else '<div class="sfb">WNSS</div>')
    st.markdown(f"""<div class="splash">
        {logo_tag}
        <h1>{SCHOOL['full']}</h1>
        <p class="sm">"{SCHOOL['motto']}"</p>
        <p class="sl">📍 {SCHOOL['loc']} &nbsp;·&nbsp; Est. {SCHOOL['founded']}</p>
        <p class="stag">Parent Portal</p>
        <div class="lbt"><div class="lbf"></div></div>
        <p class="ltx">LOADING<span>.</span><span>.</span><span>.</span></p>
    </div>""", unsafe_allow_html=True)
    time.sleep(5)
    st.session_state.entered = True
    st.rerun()

# ── TOP BAR ──────────────────────────────────────────────────────
unread = len([n for n in NOTICES if n["id"] not in st.session_state.read_ids])
logo_tag = (f'<img src="data:image/png;base64,{logo_b64}"/>' if logo_b64
            else '<div class="fb">WNSS</div>')
st.markdown(f"""<div class="topbar">
  <div style="display:flex;align-items:center;gap:10px;">
    {logo_tag}
    <div><div class="tname">{SCHOOL['name']}</div><div class="ttag">Parent Portal</div></div>
  </div>
  <div class="bell">🔔{f'<span class="bell-badge">{unread}</span>' if unread else ''}</div>
</div>""", unsafe_allow_html=True)

if not st.session_state.toasted:
    u = next((n for n in NOTICES if n["cat"]=="emergency"),None)
    if u: st.toast(f"🚨 {u['title']}", icon="🔔")
    st.session_state.toasted = True

# ── STUDENT GATE ─────────────────────────────────────────────────
s = st.session_state.student

# ================================================================
# PAGES
# ================================================================

# ── ACTION STRIP helper (used in both home & child pages) ────────
import streamlit.components.v1 as components

ACTIONS = [
    ("👤", "#4A90D9", "My Child",     "child"),
    ("💳", BLUE,      "Pay Fees",     "pay"),
    ("💬", "#2E86C1", "Messages",     "messages"),
    ("📊", NAVY,      "Report Card",  "child"),
    ("📅", CRIM,      "Calendar",     "calendar"),
    ("✅", GREEN,     "Attendance",   "child"),
    ("🏆", GOLD,      "Achievements", "achieve"),
    ("🔔", CRIMD,     "Notifications","notify"),
]

def render_action_strip():
    st.markdown('<div class="ios-sw">', unsafe_allow_html=True)
    cols = st.columns(len(ACTIONS))
    for col, (icon, color, label, target) in zip(cols, ACTIONS):
        with col:
            st.markdown(f"""
            <div style="width:52px;height:52px;border-radius:14px;
                        background:{color}18;
                        display:flex;align-items:center;justify-content:center;
                        font-size:24px;margin:0 auto 4px auto;pointer-events:none;">
                {icon}
            </div>""", unsafe_allow_html=True)
            if st.button(label, key=f"act_{label}", use_container_width=True):
                st.session_state.nav = target
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ── HOME ─────────────────────────────────────────────────────────
def page_home():
    badge = (f'<img src="data:image/png;base64,{logo_b64}"/>' if logo_b64
             else '<div class="hfb">WNSS</div>')
    st.markdown(f"""<div class="hero">{badge}
      <div><h2>{SCHOOL['full']}</h2>
      <div class="hmotto">"{SCHOOL['motto']}"</div>
      <div class="hsub">📍 {SCHOOL['loc']}</div></div>
    </div>""", unsafe_allow_html=True)

    render_action_strip()

    # Stats row
    st.markdown('<div class="stat-row">'
        '<div class="stat-mini"><div class="sv">1,200+</div><div class="sl">Students</div></div>'
        '<div class="stat-mini"><div class="sv">96%</div><div class="sl">UCE Pass</div></div>'
        '<div class="stat-mini"><div class="sv">60+</div><div class="sl">Teachers</div></div>'
        '<div class="stat-mini"><div class="sv">1966</div><div class="sl">Founded</div></div>'
        '</div>', unsafe_allow_html=True)

    # Highlights — auto-sliding carousel
    st.markdown('<div class="slabel">✨ SCHOOL HIGHLIGHTS</div>', unsafe_allow_html=True)
    slides = ""
    for h in HIGHLIGHTS:
        ib = get_b64(h["img"])
        bg = (f'background:url("data:image/jpeg;base64,{ib}") center/cover no-repeat;'
              if ib else f"background:linear-gradient(135deg,{h['c1']},{h['c2']});")
        slides += f"""<div class="slide" style="{bg}">
            <div class="ov"></div>
            <div class="tx">
                <div style="font-size:22px;margin-bottom:3px;">{h['emoji']}</div>
                <div class="tit">{h['title']}</div>
                <div class="sub">{h['detail'][:65]}…</div>
            </div>
        </div>"""

    components.html(f"""<!DOCTYPE html><html><head>
    <style>
      *{{box-sizing:border-box;margin:0;padding:0;}}
      body{{background:transparent;overflow:hidden;font-family:'Inter',sans-serif;}}
      .car{{position:relative;width:100%;height:172px;border-radius:16px;overflow:hidden;}}
      .track{{display:flex;height:100%;transition:transform .55s cubic-bezier(.4,0,.2,1);will-change:transform;}}
      .slide{{min-width:100%;height:172px;flex-shrink:0;position:relative;}}
      .ov{{position:absolute;inset:0;background:linear-gradient(to top,rgba(0,0,0,.78) 0%,rgba(0,0,0,.04) 65%);}}
      .tx{{position:absolute;bottom:0;left:0;right:0;padding:14px 16px;}}
      .tit{{color:white;font-weight:800;font-size:16px;}}
      .sub{{color:rgba(255,255,255,.82);font-size:11px;margin-top:3px;line-height:1.4;}}
      .dots{{position:absolute;bottom:11px;right:13px;display:flex;gap:5px;}}
      .dot{{width:6px;height:6px;border-radius:50%;background:rgba(255,255,255,.4);cursor:pointer;transition:all .3s;}}
      .dot.on{{background:white;width:18px;border-radius:3px;}}
      .bar{{position:absolute;top:0;left:0;height:3px;background:rgba(255,255,255,.9);border-radius:2px;transition:width .1s linear;}}
      .arr{{position:absolute;top:50%;transform:translateY(-50%);background:rgba(0,0,0,.28);border:none;border-radius:50%;width:30px;height:30px;color:white;font-size:16px;cursor:pointer;display:flex;align-items:center;justify-content:center;}}
      .al{{left:8px;}}.ar{{right:8px;}}
    </style></head><body>
    <div class="car">
      <div class="track" id="tr">{slides}</div>
      <div class="bar" id="bar"></div>
      <button class="arr al" onclick="prev()">&#8249;</button>
      <button class="arr ar" onclick="next()">&#8250;</button>
      <div class="dots" id="dots"></div>
    </div>
    <script>
      const N={len(HIGHLIGHTS)},DUR=3800;
      let cur=0,raf,last;
      const tr=document.getElementById('tr'),bar=document.getElementById('bar'),dt=document.getElementById('dots');
      for(let i=0;i<N;i++){{const d=document.createElement('div');d.className='dot'+(i===0?' on':'');d.onclick=()=>go(i);dt.appendChild(d);}}
      function upd(){{document.querySelectorAll('.dot').forEach((d,i)=>d.className='dot'+(i===cur?' on':''));}}
      function go(i){{cur=i;tr.style.transform=`translateX(-${{cur*100}}%)`;upd();reset();}}
      function next(){{go((cur+1)%N);}}
      function prev(){{go((cur-1+N)%N);}}
      function reset(){{cancelAnimationFrame(raf);bar.style.width='0%';last=null;
        function tick(now){{if(!last)last=now;const e=now-last;bar.style.width=Math.min(e/DUR*100,100)+'%';if(e>=DUR){{next();return;}}raf=requestAnimationFrame(tick);}}
        raf=requestAnimationFrame(tick);}}
      reset();
    </script></body></html>""", height=182)

    # AI briefing
    st.markdown('<div class="slabel">✨ AI SCHOOL BRIEFING</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="background:linear-gradient(135deg,{NAVY},{BLUE});border-radius:14px;padding:16px 18px;color:white;margin-bottom:12px;">', unsafe_allow_html=True)
    if st.button("Generate today's briefing", key="briefing_btn"):
        st.session_state["_briefing"] = ask_claude(
            "Write a warm 2-sentence briefing for parents of a Ugandan secondary school. Be professional.",
            f"School: {SCHOOL['full']}. Notice: '{NOTICES[0]['title']}'. Exams: 7 July. Fees due: 30 June.")
    st.write(st.session_state.get("_briefing","Tap for a quick AI summary of what's happening at school today."))
    st.markdown("</div>", unsafe_allow_html=True)

    # Latest notices
    st.markdown('<div class="slabel">📢 LATEST NOTICES</div>', unsafe_allow_html=True)
    for n in NOTICES[:2]:
        st.markdown(f"""<div class="nc {n['cat']}">
            <span class="pill pill-{n['cat']}">{n['cat'].title()}</span>
            <span style="float:right;color:{SLATE};font-size:11px;">{n['time']}</span>
            <div class="ntit">{n['title']}</div>
            <div style="color:{SLATE};font-size:13px;line-height:1.5;">{n['body'][:110]}…</div>
        </div>""", unsafe_allow_html=True)
    if st.button("View all notices →"):
        st.session_state.nav = "notify"; st.rerun()

    # Upcoming events
    st.markdown('<div class="slabel" style="margin-top:6px;">📅 COMING UP</div>', unsafe_allow_html=True)
    cc = {"emergency":CRIM,"fees":GOLD,"exam":NAVY,"event":"#2E86C1","meeting":BLUE}
    for e in EVENTS[:3]:
        c = cc.get(e["tag"],BLUE)
        st.markdown(f"""<div class="card" style="display:flex;align-items:center;gap:12px;padding:11px 14px;">
            <div style="min-width:46px;text-align:center;border-radius:9px;padding:5px 3px;
                        background:{c};color:white;font-family:'Poppins',sans-serif;">
                <div style="font-size:13px;font-weight:800;line-height:1;">{e['d'].split()[0]}</div>
                <div style="font-size:8.5px;opacity:.85;">{e['m']}</div>
            </div>
            <div style="font-weight:600;color:{INK};font-size:13px;">{e['label']}</div>
        </div>""", unsafe_allow_html=True)

    if st.button("🔍 Find My Child →", type="primary", use_container_width=True):
        st.session_state.nav = "child"; st.rerun()

# ── MY CHILD ─────────────────────────────────────────────────────
def page_child():
    if s is None:
        st.markdown('<div class="slabel">🔍 FIND YOUR CHILD</div>', unsafe_allow_html=True)
        q = st.text_input("Search","",placeholder="e.g. Mawanda, Simon, Kenneth…",
                           label_visibility="collapsed")
        if q:
            m = SDF[SDF["name"].str.contains(q,case=False,na=False)]
            if m.empty:
                st.error("No student found. Try a different name or contact the school office.")
            else:
                for _,row in m.iterrows():
                    st.markdown(f"""<div class="card" style="padding:13px 16px;">
                        <div style="font-weight:700;color:{INK};font-size:15px;">{row['name']}</div>
                        <div style="color:{SLATE};font-size:12px;">{row['klass']} · Adm. {row['adm']}</div>
                    </div>""", unsafe_allow_html=True)
                    if st.button(f"Open {row['name'].split()[0]}'s record →", key=f"sel_{row['adm']}"):
                        st.session_state.student = row.to_dict(); st.rerun()
        else:
            st.caption("⚠️ Demo: 4 sample students. Connect your real school register to go live.")
        return

    b = bal(s)
    paid_live = s["billed"] - b
    a1,a2 = st.columns([4,1])
    with a1:
        st.markdown(f"""<div class="card" style="border-left:5px solid {BLUE};padding:13px 16px;">
            <div style="font-family:'Poppins',sans-serif;font-weight:800;font-size:16px;color:{NAVY};">{s['name']}</div>
            <div style="color:{SLATE};font-size:12px;">{s['klass']} · {s['adm']} · {s['guardian']}</div>
        </div>""", unsafe_allow_html=True)
    with a2:
        if st.button("Switch"):
            st.session_state.student=None; st.session_state.chat=[]; st.rerun()

    st.markdown('<div class="stat-row">'
        f'<div class="stat-mini"><div class="sv" style="color:{"#1FAF54" if s["att"]>=90 else CRIM};">{s["att"]}%</div><div class="sl">Attendance</div></div>'
        f'<div class="stat-mini"><div class="sv" style="color:{CRIMD if b>0 else GREEN};">{money(b) if b>0 else "Paid ✅"}</div><div class="sl">Fee Balance</div></div>'
        f'<div class="stat-mini"><div class="sv">{s["rank"]}/{s["of"]}</div><div class="sl">Class Rank</div></div>'
        '</div>', unsafe_allow_html=True)

    t1,t2,t3,t4 = st.tabs(["📊 Report Card","✅ Attendance","💳 Pay Fees","🤖 AI Assistant"])

    with t1:
        avg = round(sum(f for _,_,f in s["subs"])/len(s["subs"]),1)
        st.markdown(f"""<div class="card">
            <div style="font-family:'Poppins',sans-serif;font-size:20px;font-weight:800;color:{NAVY};">
                Position {s['rank']} <span style="color:{SLATE};font-size:13px;font-weight:600;">of {s['of']}</span>
                &nbsp;·&nbsp; Avg <span style="color:{BLUE};">{avg}%</span>
            </div><div style="color:{SLATE};font-size:11.5px;">Term 2, 2026 · {s['klass']}</div>
        </div>""", unsafe_allow_html=True)
        for nm,mi,fi in s["subs"]:
            up = fi>=mi; col = BLUE if up else CRIM
            st.markdown(f"""<div class="rc-row">
                <div style="display:flex;align-items:center;gap:10px;">
                    <div class="grade-box">{grade(fi)}</div>
                    <span style="font-weight:600;color:{INK};">{nm}</span>
                </div>
                <span style="font-family:'Poppins',sans-serif;font-weight:700;color:{col};">{mi} → {fi} {'↑' if up else '↓'}</span>
            </div>""", unsafe_allow_html=True)
        txt = (f"{SCHOOL['full']}\nOFFICIAL REPORT CARD — TERM 2, 2026\n"
               f"Student: {s['name']}\nClass: {s['klass']}\nAdm: {s['adm']}\n"
               f"Position: {s['rank']} of {s['of']}\nAverage: {avg}%\n\n"
               +"\n".join(f"{n}: {m}→{f} (Grade {grade(f)})" for n,m,f in s["subs"])
               +"\n\nClass teacher: Keep up the effort and revise past papers consistently.")
        st.download_button("⬇️ Download report card", data=txt,
                            file_name=f"{s['name'].replace(' ','_')}_T2_2026.txt")

    with t2:
        ring_c = GREEN if s["att"]>=90 else (GOLD if s["att"]>=75 else CRIM)
        st.markdown(f"""<div class="card" style="text-align:center;padding:22px;">
            <div style="font-family:'Poppins',sans-serif;font-size:38px;font-weight:800;color:{ring_c};">{s['att']}%</div>
            <div style="color:{SLATE};font-size:13px;">Present this term</div>
        </div>""", unsafe_allow_html=True)
        for dt,st_,ic in [("Mon 22 Jun","Present","🟢"),("Tue 23 Jun","Present","🟢"),
                            ("Wed 24 Jun","Late — arrived 8:40am","🟡"),
                            ("Thu 18 Jun","Absent — no reason given","🔴"),
                            ("Wed 17 Jun","Present","🟢"),("Tue 16 Jun","Present","🟢")]:
            st.markdown(f"""<div class="card" style="display:flex;align-items:center;gap:11px;padding:11px 14px;">
                <span style="font-size:15px;">{ic}</span>
                <span><b>{dt}</b> — <span style="color:{SLATE};">{st_}</span></span>
            </div>""", unsafe_allow_html=True)

    with t3:
        st.markdown('<div class="slabel">💳 ENTER PAYMENT CODE</div>', unsafe_allow_html=True)
        code_in = st.text_input("Payment code", value=s.get("code",""),
                                 placeholder="e.g. WN-0417")
        if code_in.strip():
            mx = SDF[SDF["code"].str.upper()==code_in.strip().upper()]
            if mx.empty:
                st.error("❌ Invalid code. Check the fee structure or report card.")
            else:
                ps = mx.iloc[0].to_dict()
                ps_bal = bal(ps); ps_paid = ps["billed"]-ps_bal
                st.markdown(f"""<div class="card" style="border-left:5px solid {GREEN};">
                    <span style="color:{GREEN};font-weight:700;font-size:11.5px;">✅ CODE VERIFIED</span>
                    <div style="font-family:'Poppins',sans-serif;font-weight:800;font-size:16px;color:{NAVY};margin-top:5px;">{ps['name']}</div>
                    <div style="color:{SLATE};font-size:12px;">Class: <b>{ps['level']}</b> &nbsp;·&nbsp; Stream: <b>{ps['stream']}</b> &nbsp;·&nbsp; Adm. {ps['adm']}</div>
                </div>""", unsafe_allow_html=True)
                st.markdown(f"""<div class="acct-card">
                    <div style="font-size:12px;color:{SLATE};">Outstanding balance</div>
                    <div style="font-family:'Poppins',sans-serif;font-size:28px;font-weight:800;color:{CRIMD if ps_bal>0 else GREEN};">
                        {money(ps_bal) if ps_bal>0 else "Fully Paid ✅"}
                    </div>
                    {"<div style='color:"+CRIM+";font-weight:700;font-size:11.5px;'>Due 30 June 2026</div>" if ps_bal>0 else ""}
                </div>""", unsafe_allow_html=True)
                if ps_bal > 0:
                    st.progress(ps_paid/ps["billed"],
                                text=f"{ps_paid/ps['billed']*100:.0f}% paid · {money(ps_paid)} of {money(ps['billed'])}")
                    method = st.radio("Payment method",
                                      ["MTN Mobile Money","Airtel Money","Bank Deposit"],
                                      label_visibility="collapsed")
                    phone = st.text_input("Phone number", value=ps["phone"])
                    choice = st.radio("Amount",["Pay full balance","Pay a custom amount"])
                    amount = ps_bal if choice=="Pay full balance" else st.number_input(
                        "Amount (UGX)",min_value=1000,max_value=int(ps_bal),
                        value=min(100000,int(ps_bal)),step=5000)
                    st.caption("🔧 Demo mode — live payments need a licensed aggregator (Flutterwave / Pegasus / Relworx).")
                    if st.button(f"Pay {money(amount)} via {method} →",type="primary",use_container_width=True):
                        with st.spinner("Processing…"): time.sleep(1.6)
                        ref = f"{method.split()[0][:2].upper()}{datetime.now().strftime('%y%m%d')}.{random.randint(1000,9999)}"
                        st.session_state.paid_extra[ps["adm"]] = \
                            st.session_state.paid_extra.get(ps["adm"],0)+amount
                        st.session_state["_receipt"] = {
                            "name":ps["name"],"date":datetime.now().strftime("%d %b %Y"),
                            "method":method,"amount":amount,"ref":ref}
                        st.balloons(); st.rerun()
                if st.session_state["_receipt"]:
                    r = st.session_state["_receipt"]
                    st.markdown(f"""<div class="card" style="border-left:5px solid {GREEN};">
                        <b style="color:{GREEN};">✅ Payment received</b>
                        <p style="margin:5px 0 0;font-size:13px;color:{SLATE};">
                        {money(r['amount'])} via {r['method']} for {r['name']} on {r['date']}<br>Ref: {r['ref']}</p>
                    </div>""", unsafe_allow_html=True)
                    st.download_button("⬇️ Download receipt",
                        data=f"{SCHOOL['full']}\nStudent: {r['name']}\nAmount: {money(r['amount'])}\n"
                             f"Method: {r['method']}\nDate: {r['date']}\nRef: {r['ref']}\n",
                        file_name="receipt.txt")
        else:
            st.info("👆 Enter the payment code printed on the fee structure or report card.")
        st.markdown('<div class="slabel" style="margin-top:14px;">🧾 PAYMENT HISTORY</div>', unsafe_allow_html=True)
        st.dataframe(pd.DataFrame([{"Date":h["date"],"Method":h["method"],
                                     "Amount":money(h["amount"]),"Ref":h["ref"]}
                                    for h in PAY_HIST]),use_container_width=True,hide_index=True)

    with t4:
        sys_p = (f"You are a parent AI assistant for {SCHOOL['full']} in Uganda. "
                 "Speak warmly, briefly (2-5 sentences). Use UGX. Only use this record:\n"
                 f"Student: {s['name']}, Class: {s['klass']}\n"
                 f"Attendance: {s['att']}%\n"
                 f"Fees: billed {s['billed']}, paid {paid_live}, balance {b}, due 30 June 2026\n"
                 f"Rank: {s['rank']} of {s['of']}\n"
                 f"Subjects: {', '.join(f'{n} {m}->{f}' for n,m,f in s['subs'])}\n"
                 "If unsure, say so and suggest messaging the school.")
        for msg in st.session_state.chat:
            with st.chat_message(msg["role"]): st.write(msg["text"])
        c1,c2,c3 = st.columns(3)
        for col,sg in zip([c1,c2,c3],["When are next exams?","What's my child's attendance?","How much fees remain?"]):
            if col.button(sg,key=f"sg_{sg}"):
                st.session_state.chat.append({"role":"user","text":sg})
                st.session_state.chat.append({"role":"assistant","text":ask_claude(sys_p,sg)})
                st.rerun()
        inp = st.chat_input("Ask about fees, attendance, exams…")
        if inp:
            st.session_state.chat.append({"role":"user","text":inp})
            st.session_state.chat.append({"role":"assistant","text":ask_claude(sys_p,inp)})
            st.rerun()
        st.divider()
        lang = st.selectbox("Translate last reply to:",["—","Luganda","Swahili","English"])
        if lang!="—" and st.session_state.chat:
            last = next((m["text"] for m in reversed(st.session_state.chat) if m["role"]=="assistant"),None)
            if last and st.button("Translate"):
                st.info(ask_claude(f"Translate into {lang}, naturally and warmly. Output only the translation.",last))

# ── NOTIFICATIONS ────────────────────────────────────────────────
def page_notify():
    st.markdown('<div class="slabel">🔔 NOTIFICATIONS</div>', unsafe_allow_html=True)
    _,cr = st.columns([3,1])
    with cr:
        if st.button("Mark all read"):
            st.session_state.read_ids={n["id"] for n in NOTICES}; st.rerun()
    for n in NOTICES:
        unrd = n["id"] not in st.session_state.read_ids
        st.markdown(f"""<div class="nc {n['cat']}">
            <span class="pill pill-{n['cat']}">{n['cat'].title()}</span>
            <span style="float:right;color:{SLATE};font-size:11px;">{n['time']}</span>
            <div class="ntit">{'🔵 ' if unrd else ''}{n['title']}</div>
            <div style="color:{SLATE};font-size:13px;line-height:1.5;">{n['body']}</div>
        </div>""", unsafe_allow_html=True)
        b1,b2,_ = st.columns([1,1,3])
        with b1:
            if st.button("✨ Summary",key=f"sm_{n['id']}"):
                st.success(ask_claude(
                    "Shorten this school announcement into one plain sentence for a parent, under 25 words.",
                    n["body"]))
        with b2:
            if unrd and st.button("Mark read",key=f"rd_{n['id']}"):
                st.session_state.read_ids.add(n["id"]); st.rerun()

# ── CALENDAR ─────────────────────────────────────────────────────
def page_calendar():
    st.markdown('<div class="slabel">📅 TERM 2 — 2026</div>', unsafe_allow_html=True)
    cc = {"emergency":CRIM,"fees":GOLD,"exam":NAVY,"event":"#2E86C1","meeting":BLUE}
    for e in EVENTS:
        c = cc.get(e["tag"],BLUE)
        st.markdown(f"""<div class="card" style="display:flex;align-items:center;gap:12px;padding:11px 14px;">
            <div style="min-width:48px;text-align:center;border-radius:9px;padding:5px 3px;
                        background:{c};color:white;font-family:'Poppins',sans-serif;">
                <div style="font-size:14px;font-weight:800;line-height:1;">{e['d'].split()[0]}</div>
                <div style="font-size:8.5px;opacity:.85;">{e['m']}</div>
            </div>
            <div style="font-weight:600;color:{INK};font-size:13.5px;">{e['label']}</div>
        </div>""", unsafe_allow_html=True)

# ── MESSAGES ─────────────────────────────────────────────────────
def page_messages():
    if st.session_state.active_thread is None:
        st.markdown('<div class="slabel">💬 MESSAGES</div>', unsafe_allow_html=True)
        for t in st.session_state.threads:
            last = t["messages"][-1]["text"]
            st.markdown(f"""<div class="card" style="padding:13px 16px;">
                <b style="color:{NAVY};">{'👥 ' if t.get('group') else '👤 '}{t['with']}</b>
                <p style="color:{SLATE};font-size:12px;margin:4px 0 0;">{last[:80]}{'…' if len(last)>80 else ''}</p>
            </div>""", unsafe_allow_html=True)
            if st.button("Open",key=f"th_{t['id']}"):
                st.session_state.active_thread=t["id"]; st.rerun()
    else:
        t = next(x for x in st.session_state.threads if x["id"]==st.session_state.active_thread)
        if st.button("← Back"):
            st.session_state.active_thread=None; st.rerun()
        st.markdown(f"#### {t['with']}")
        for m in t["messages"]:
            with st.chat_message("user" if m["from"]=="parent" else "assistant"):
                st.write(m["text"]); st.caption(m["time"])
        rep = st.chat_input("Write a message…")
        if rep:
            t["messages"].append({"from":"parent","text":rep,"time":"Now"}); st.rerun()

# ── ACHIEVEMENTS ─────────────────────────────────────────────────
def page_achieve():
    st.markdown('<div class="slabel">🏆 SCHOOL ACHIEVEMENTS</div>', unsafe_allow_html=True)
    for h in HIGHLIGHTS:
        ib = get_b64(h["img"])
        img_html = (f'<img src="data:image/jpeg;base64,{ib}" style="width:52px;height:52px;border-radius:12px;object-fit:cover;flex-shrink:0;"/>'
                    if ib else f'<div style="width:52px;height:52px;border-radius:12px;flex-shrink:0;background:linear-gradient(135deg,{h["c1"]},{h["c2"]});display:flex;align-items:center;justify-content:center;font-size:22px;">{h["emoji"]}</div>')
        st.markdown(f"""<div class="card" style="display:flex;gap:14px;align-items:flex-start;">
            {img_html}
            <div>
                <div style="font-weight:700;color:{NAVY};font-size:14px;">{h['title']}</div>
                <div style="color:{SLATE};font-size:13px;line-height:1.5;margin-top:3px;">{h['detail']}</div>
            </div>
        </div>""", unsafe_allow_html=True)

# ── ROUTER ───────────────────────────────────────────────────────
PAGES = {"home":page_home,"child":page_child,"notify":page_notify,
         "calendar":page_calendar,"messages":page_messages,"achieve":page_achieve,
         "pay":page_child}
PAGES.get(st.session_state.nav, page_home)()

# ── BOTTOM NAV ───────────────────────────────────────────────────
NAV = [("home","🏠","Home"),("child","👤","My Child"),
       ("notify","🔔","Alerts"),("calendar","📅","Calendar"),("messages","💬","Messages")]

with st.container(border=True):
    st.markdown('<div class="navmarker"></div>', unsafe_allow_html=True)
    ncols = st.columns(5)
    for col,(key,icon,label) in zip(ncols,NAV):
        active = st.session_state.nav == key
        badge = f" {unread}" if key=="notify" and unread else ""
        with col:
            if col.button(f"{icon}{badge}\n{label}", key=f"nav_{key}",
                          use_container_width=True,
                          type="primary" if active else "secondary"):
                st.session_state.nav=key; st.rerun()
