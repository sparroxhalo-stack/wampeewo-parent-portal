import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# ---------------------------------------------------------------
# PAGE CONFIG + THEME
# ---------------------------------------------------------------
st.set_page_config(page_title="Wampeewo Ntakke — Parent Portal", page_icon="🎓", layout="wide")

PRIMARY = "#14342B"   # deep forest green
GOLD = "#D7A33D"      # gayaza gold
TERRACOTTA = "#B8512F"
CREAM = "#F7F2E7"

st.markdown(f"""
<style>
.stApp {{ background-color: {CREAM}; }}
.header-bar {{
    background-color: {PRIMARY}; color: white; padding: 18px 24px;
    border-radius: 12px; margin-bottom: 14px; display:flex; align-items:center; gap:14px;
}}
.header-bar h1 {{ font-size: 20px; margin: 0; }}
.header-bar p {{ margin: 0; color: #9fcdb4; font-size: 12px; }}
.badge {{
    display:inline-block; padding: 2px 10px; border-radius: 999px;
    font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: .04em;
}}
.badge-emergency {{ background:{TERRACOTTA}; color:white; }}
.badge-meeting {{ background:{PRIMARY}; color:white; }}
.badge-exam {{ background:#555; color:white; }}
.badge-fees {{ background:{GOLD}; color:#3a2a05; }}
.badge-event {{ background:#3f7a5d; color:white; }}
.card {{
    background:white; border:1px solid #e3ddca; border-radius:12px;
    padding:16px; margin-bottom:10px;
}}
.metric-card {{
    background:white; border:1px solid #e3ddca; border-radius:12px; padding:14px;
    text-align:center;
}}
.metric-card .value {{ font-size: 26px; font-weight: 800; color:{PRIMARY}; }}
.metric-card .label {{ font-size: 11px; text-transform:uppercase; letter-spacing:.05em; color:#777; }}
.seal {{
    border: 3px dashed {TERRACOTTA}; border-radius: 50%; width: 70px; height: 70px;
    display:flex; align-items:center; justify-content:center; font-size: 10px;
    text-align:center; color:{TERRACOTTA}; font-weight:700; line-height:1.1; padding:4px;
}}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------
# SCHOOL FACTS (real, public) — swap in your own about-page copy
# ---------------------------------------------------------------
SCHOOL = {
    "name": "Wampeewo Ntakke Secondary School",
    "motto": "Ekkula ye bukka",
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

# ---------------------------------------------------------------
# CLAUDE API HELPER (uses the same secrets pattern as your other app)
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

# ---------------------------------------------------------------
# HEADER
# ---------------------------------------------------------------
st.markdown(f"""
<div class="header-bar">
    <div class="seal">WNSS<br>EST {SCHOOL['founded']}</div>
    <div>
        <h1>{SCHOOL['name']}</h1>
        <p>Parent Portal · {SCHOOL['location']} · Motto: "{SCHOOL['motto']}"</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------
# STUDENT SEARCH (this is the bit you asked for)
# ---------------------------------------------------------------
if st.session_state.student is None:
    st.subheader("🔍 Find your child")
    query = st.text_input("Type your child's name", placeholder="e.g. Nantongo, Okello, Sarah...")

    if query:
        matches = STUDENTS_DF[STUDENTS_DF["name"].str.contains(query, case=False, na=False)]
        if matches.empty:
            st.info("No student found with that name in this demo database. "
                    "Connect your real student register to search live records.")
        else:
            st.write(f"Found {len(matches)} match(es):")
            for _, row in matches.iterrows():
                with st.container(border=True):
                    c1, c2 = st.columns([4, 1])
                    with c1:
                        st.markdown(f"**{row['name']}** — {row['klass']}")
                        st.caption(f"Admission no. {row['admission_no']} · Guardian: {row['guardian']}")
                    with c2:
                        if st.button("Select", key=row["admission_no"]):
                            st.session_state.student = row.to_dict()
                            st.rerun()
    else:
        st.caption("⚠️ This is a sample database of 4 demo students for testing. "
                   "Swap `STUDENTS` for your real register (CSV/Google Sheet/database) to make this live.")
    st.stop()

# ---------------------------------------------------------------
# STUDENT DASHBOARD
# ---------------------------------------------------------------
s = st.session_state.student
top_l, top_r = st.columns([5, 1])
with top_l:
    st.markdown(f"### {s['name']} · {s['klass']}")
    st.caption(f"Admission no. {s['admission_no']} · Guardian on record: {s['guardian']}")
with top_r:
    if st.button("🔄 Switch student"):
        st.session_state.student = None
        st.session_state.chat = []
        st.rerun()

tabs = st.tabs(["🏠 Overview", "📢 Notices", "💰 Fees", "📊 Academic", "✅ Attendance", "🤖 AI Assistant"])

# --- Overview ---
with tabs[0]:
    balance = s["fees_billed"] - s["fees_paid"]
    c1, c2, c3 = st.columns(3)
    for col, label, value in zip(
        [c1, c2, c3],
        ["Attendance", "Fee balance", "Class rank"],
        [f"{s['attendance_pct']}%", money(balance), f"{s['rank']} / {s['out_of']}"],
    ):
        col.markdown(f"<div class='metric-card'><div class='value'>{value}</div>"
                      f"<div class='label'>{label}</div></div>", unsafe_allow_html=True)

    st.markdown("#### Latest notice")
    n = NOTICES[1]
    st.markdown(f"""<div class="card">
        <span class="badge badge-{n['category']}">{n['category'].title()}</span><br><br>
        <b>{n['title']}</b><p>{n['body']}</p><small>{n['time']}</small>
    </div>""", unsafe_allow_html=True)

# --- Notices ---
with tabs[1]:
    for n in NOTICES:
        with st.container(border=True):
            st.markdown(f"<span class='badge badge-{n['category']}'>{n['category'].title()}</span> "
                        f"<small>{n['time']}</small>", unsafe_allow_html=True)
            st.markdown(f"**{n['title']}**")
            st.write(n["body"])
            if st.button("✨ AI summary", key=f"sum_{n['id']}"):
                summary = ask_claude(
                    "Shorten this school announcement into one calm, plain sentence for a parent, under 25 words.",
                    n["body"],
                )
                st.success(summary)

# --- Fees ---
with tabs[2]:
    balance = s["fees_billed"] - s["fees_paid"]
    pct_paid = s["fees_paid"] / s["fees_billed"]
    st.markdown(f"#### Outstanding balance: {money(balance)}")
    st.progress(pct_paid, text=f"{pct_paid*100:.0f}% paid · {money(s['fees_paid'])} of {money(s['fees_billed'])}")
    st.caption("Due 30 June 2026")

    st.markdown("#### Payment history")
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

# --- Academic ---
with tabs[3]:
    st.markdown(f"#### Report card — Position {s['rank']} of {s['out_of']}")
    sub_df = pd.DataFrame(s["subjects"], columns=["Subject", "Midterm", "Final"])
    sub_df["Change"] = sub_df["Final"] - sub_df["Midterm"]
    st.dataframe(sub_df, use_container_width=True, hide_index=True)

# --- Attendance ---
with tabs[4]:
    st.metric("This term", f"{s['attendance_pct']}% present")
    log = [
        ("Mon 22 Jun", "Present"), ("Tue 23 Jun", "Present"),
        ("Wed 24 Jun", "Late — arrived 8:40am"), ("Thu 18 Jun", "Absent — no reason given"),
        ("Wed 17 Jun", "Present"), ("Tue 16 Jun", "Present"),
    ]
    for date, status in log:
        icon = "🟢" if "Present" in status else "🟡" if "Late" in status else "🟠"
        st.write(f"{icon} **{date}** — {status}")

# --- AI Assistant ---
with tabs[5]:
    st.caption(f"Answers using {s['name']}'s live record")

    system_prompt = (
        "You are the Parent AI Assistant for a Ugandan secondary school. Speak warmly and briefly "
        "(2-5 sentences). Use UGX for money. Only use this student record, never invent numbers:\n"
        f"Name: {s['name']}, Class: {s['klass']}\n"
        f"Attendance: {s['attendance_pct']}% this term\n"
        f"Fees: billed {s['fees_billed']} UGX, paid {s['fees_paid']} UGX, "
        f"balance {s['fees_billed'] - s['fees_paid']} UGX, due 30 June 2026\n"
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
