"""
SmartCampusAI — Premium Dashboard Page
=========================================
Main authenticated dashboard showing attendance metrics, today's schedule,
campus announcements, events calendar, and AI assistant interface.
"""

import streamlit as st
from utils.styles import apply_custom_css
from auth.auth_utils import is_logged_in, logout_user, get_current_user
from utils.api_client import ask_ai
from database.db_utils import load_announcements, load_events

# ── Page Configuration ────────────────────────────────────────
st.set_page_config(
    page_title="SmartCampusAI — Dashboard",
    page_icon="📊",
    layout="wide"
)

apply_custom_css()

# ── Session Guard ─────────────────────────────────────────────
if not is_logged_in():
    st.warning("⚠️ Access denied. Please log in to continue.")
    st.page_link("pages/1_Login.py", label="→ Go to Login", icon="🔒")
    st.stop()

user = get_current_user()

# ── Sidebar ───────────────────────────────────────────────────
initial = user["username"][0].upper()

st.sidebar.markdown(
    f"""
    <div style="text-align:center; padding: 16px 0 8px;">
        <div class="avatar-circle">{initial}</div>
        <h4 style="margin: 6px 0 2px; color: #818cf8;">{user['username']}</h4>
        <span style="font-size:0.8rem; color:#64748b;">{user['email']}</span><br>
        <span class="metric-badge badge-blue" style="margin-top:6px; display:inline-block;">
            {user.get('role', 'Student').title()}
        </span>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("---")
st.sidebar.markdown("**📍 Navigation**")
st.sidebar.page_link("app.py",               label="🏠 Home",        icon="🏠")
st.sidebar.page_link("pages/3_Dashboard.py", label="📊 Dashboard",   icon="📊")
st.sidebar.markdown("---")

st.sidebar.markdown(
    f"<small style='color:#475569;'>Member since: {user['created_at'][:10]}</small>",
    unsafe_allow_html=True
)

st.sidebar.markdown("<br>", unsafe_allow_html=True)
if st.sidebar.button("🚪 Logout", use_container_width=True, key="sidebar_logout"):
    logout_user()
    st.toast("Logged out successfully.")
    st.switch_page("app.py")

# ── Dashboard Header ──────────────────────────────────────────
st.markdown(
    f"""
    <div style="margin-bottom: 8px;">
        <h1 class="gradient-text" style="font-size: 2.2rem; margin-bottom: 4px;">
            Welcome back, {user['username']}! 👋
        </h1>
        <p style="color:#64748b;">Here's your academic status summary for today.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# ── Top Metric Strip ──────────────────────────────────────────
m1, m2, m3, m4 = st.columns(4, gap="small")

with m1:
    st.markdown(
        """
        <div class="glass-card" style="text-align:center; padding:20px;">
            <div style="font-size:2rem;">📈</div>
            <h2 style="margin:8px 0 4px; color:#4ade80;">88.5%</h2>
            <span style="color:#64748b; font-size:0.85rem;">Overall Attendance</span>
        </div>
        """,
        unsafe_allow_html=True
    )

with m2:
    st.markdown(
        """
        <div class="glass-card" style="text-align:center; padding:20px;">
            <div style="font-size:2rem;">📚</div>
            <h2 style="margin:8px 0 4px; color:#818cf8;">3.55</h2>
            <span style="color:#64748b; font-size:0.85rem;">Current CGPA</span>
        </div>
        """,
        unsafe_allow_html=True
    )

with m3:
    st.markdown(
        """
        <div class="glass-card" style="text-align:center; padding:20px;">
            <div style="font-size:2rem;">🗓️</div>
            <h2 style="margin:8px 0 4px; color:#f472b6;">3</h2>
            <span style="color:#64748b; font-size:0.85rem;">Classes Today</span>
        </div>
        """,
        unsafe_allow_html=True
    )

with m4:
    st.markdown(
        """
        <div class="glass-card" style="text-align:center; padding:20px;">
            <div style="font-size:2rem;">🔔</div>
            <h2 style="margin:8px 0 4px; color:#fbbf24;">4</h2>
            <span style="color:#64748b; font-size:0.85rem;">New Announcements</span>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")

# ── Row 1: Attendance + Schedule + Announcements ──────────────
row1_c1, row1_c2, row1_c3 = st.columns([1.1, 1.1, 1.2], gap="medium")

# ── Attendance ────────────────────────────────────────────────
with row1_c1:
    st.markdown("### 📈 Attendance Health")
    st.markdown(
        """
        <div class="glass-card">
        """,
        unsafe_allow_html=True
    )

    subjects = [
        ("CS101 — Programming",    38, 40, "#4ade80"),
        ("MATH202 — Linear Algebra", 32, 40, "#fbbf24"),
        ("ENG105 — Tech Writing",   36, 40, "#818cf8"),
        ("PHY301 — Physics",        30, 40, "#f87171"),
    ]

    for subj, attended, total, color in subjects:
        pct = int((attended / total) * 100)
        status = "🟢" if pct >= 85 else ("🟡" if pct >= 75 else "🔴")
        st.markdown(
            f"""
            <div class="stat-card" style="border-left-color:{color};">
                <strong style="font-size:0.88rem;">{subj}</strong>
                <div style="display:flex; justify-content:space-between; margin-top:4px;">
                    <span style="color:#94a3b8; font-size:0.82rem;">{attended}/{total} classes</span>
                    <span style="color:{color}; font-weight:700;">{status} {pct}%</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("</div>", unsafe_allow_html=True)

# ── Today's Schedule ──────────────────────────────────────────
with row1_c2:
    st.markdown("### 📅 Today's Schedule")
    st.markdown(
        """
        <div class="glass-card">
            <div class="stat-card" style="border-left-color:#f472b6;">
                <strong>09:00 – 10:30 AM</strong><br>
                <span>CS101: Intro to Programming</span><br>
                <span style="font-size:0.82rem; color:#94a3b8;">📍 Room 402, Engineering Block</span>
            </div>
            <div class="stat-card" style="border-left-color:#818cf8;">
                <strong>11:00 – 12:30 PM</strong><br>
                <span>MATH202: Linear Algebra</span><br>
                <span style="font-size:0.82rem; color:#94a3b8;">📍 Seminar Hall B</span>
            </div>
            <div class="stat-card" style="border-left-color:#a855f7;">
                <strong>02:00 – 04:00 PM</strong><br>
                <span>CS101: Programming Lab</span><br>
                <span style="font-size:0.82rem; color:#94a3b8;">📍 Lab Building A</span>
            </div>
            <div class="stat-card" style="border-left-color:#fbbf24;">
                <strong>04:30 – 05:30 PM</strong><br>
                <span>Library Study Session (Self)</span><br>
                <span style="font-size:0.82rem; color:#94a3b8;">📍 Central Library</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ── Announcements ─────────────────────────────────────────────
with row1_c3:
    st.markdown("### 🔔 Campus Announcements")

    try:
        announcements = load_announcements()
    except Exception:
        announcements = []

    if announcements:
        for ann in announcements[:4]:
            priority = ann.get("priority", "low")
            badge_cls = "badge-red" if priority == "high" else (
                "badge-amber" if priority == "medium" else "badge-green"
            )
            priority_label = priority.upper()
            st.markdown(
                f"""
                <div class="ann-card {priority}">
                    <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:6px;">
                        <strong style="font-size:0.92rem;">{ann['title']}</strong>
                        <span class="metric-badge {badge_cls}">{priority_label}</span>
                    </div>
                    <p style="font-size:0.83rem; color:#94a3b8; margin:0 0 6px;">{ann['body']}</p>
                    <small style="color:#475569;">— {ann.get('author','Admin')} · {ann.get('date','')}</small>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.markdown(
            """
            <div class="glass-card">
                <div class="ann-card high">
                    <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:6px;">
                        <strong>Exam Timetable Published</strong>
                        <span class="metric-badge badge-red">HIGH</span>
                    </div>
                    <p style="font-size:0.83rem; color:#94a3b8; margin:0 0 6px;">
                        Final examinations start July 22nd. Confirm seating by July 18th.
                    </p>
                    <small style="color:#475569;">— Academic Registrar · 2026-07-14</small>
                </div>
                <div class="ann-card medium">
                    <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:6px;">
                        <strong>Hostel WiFi Maintenance</strong>
                        <span class="metric-badge badge-amber">MEDIUM</span>
                    </div>
                    <p style="font-size:0.83rem; color:#94a3b8; margin:0 0 6px;">
                        Network disruption Thursday 10:00 PM – Friday 2:00 AM.
                    </p>
                    <small style="color:#475569;">— IT Services · 2026-07-13</small>
                </div>
                <div class="ann-card low">
                    <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:6px;">
                        <strong>Library Digital Access</strong>
                        <span class="metric-badge badge-green">LOW</span>
                    </div>
                    <p style="font-size:0.83rem; color:#94a3b8; margin:0 0 6px;">
                        Free access to IEEE Xplore and SpringerLink now available.
                    </p>
                    <small style="color:#475569;">— Central Library · 2026-07-12</small>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# ── Row 2: Events Calendar ────────────────────────────────────
st.markdown("---")
st.markdown("### 🗓️ Upcoming Campus Events")

try:
    events = load_events()
except Exception:
    events = []

if events:
    ev_cols = st.columns(len(events) if len(events) <= 3 else 3, gap="medium")
    for i, ev in enumerate(events[:3]):
        cat = ev.get("category", "other")
        cat_colors = {
            "competition": "#f472b6",
            "academic":    "#818cf8",
            "workshop":    "#4ade80",
            "other":       "#94a3b8"
        }
        color = cat_colors.get(cat, "#94a3b8")
        with ev_cols[i]:
            st.markdown(
                f"""
                <div class="glass-card" style="border-top: 3px solid {color};">
                    <span class="metric-badge" style="background:rgba(255,255,255,0.06); color:{color}; border:1px solid {color}50; margin-bottom:12px; display:inline-block;">
                        {cat.upper()}
                    </span>
                    <h4 style="margin: 8px 0 6px;">{ev['title']}</h4>
                    <p style="font-size:0.85rem; color:#94a3b8; margin-bottom:12px;">{ev['description'][:120]}...</p>
                    <div class="stat-card" style="border-left-color:{color}; padding:10px 14px; margin:0;">
                        <span style="font-size:0.82rem; color:#64748b;">📅 {ev['date']} · ⏰ {ev['time']}</span><br>
                        <span style="font-size:0.82rem; color:#64748b;">📍 {ev['venue']}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
else:
    st.markdown(
        """
        <div class="glass-card">
            <div style="display:flex; gap:24px; flex-wrap:wrap;">
                <div style="flex:1; min-width:240px;">
                    <div class="stat-card" style="border-left-color:#f472b6;">
                        <strong>🏆 Annual Tech Hackathon</strong><br>
                        <span style="font-size:0.82rem; color:#94a3b8;">July 20 · 09:00 AM · Engineering Auditorium</span>
                    </div>
                </div>
                <div style="flex:1; min-width:240px;">
                    <div class="stat-card" style="border-left-color:#818cf8;">
                        <strong>📝 Final Examination Period</strong><br>
                        <span style="font-size:0.82rem; color:#94a3b8;">July 22 · 08:00 AM · Multiple Exam Halls</span>
                    </div>
                </div>
                <div style="flex:1; min-width:240px;">
                    <div class="stat-card" style="border-left-color:#4ade80;">
                        <strong>🤖 ML/AI Workshop</strong><br>
                        <span style="font-size:0.82rem; color:#94a3b8;">July 28 · 10:00 AM · CS Lab 201</span>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ── Row 3: AI Chat Assistant ──────────────────────────────────
st.markdown("---")
st.markdown("### 💬 SmartCampusAI Assistant")
st.caption("Ask anything about schedules, attendance, exams, or campus life.")

# ── Init chat history ─────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# ── Quick Prompt Suggestions ──────────────────────────────────
st.write("💡 **Quick queries:**")
qc1, qc2, qc3, qc4 = st.columns(4)
quick_prompts = {
    "📅 Today's schedule": "What classes do I have today?",
    "📈 Attendance status": "Give me my subject-wise attendance breakdown",
    "📢 Latest notices": "What are the latest campus announcements?",
    "📊 My GPA": "What is my current GPA and academic standing?"
}
for col, (label, prompt) in zip([qc1, qc2, qc3, qc4], quick_prompts.items()):
    with col:
        if st.button(label, use_container_width=True, key=f"qp_{label}"):
            st.session_state["pending_prompt"] = prompt

# ── Retrieve pending prompt ───────────────────────────────────
default_prompt = st.session_state.pop("pending_prompt", "")

# ── Chat Input ────────────────────────────────────────────────
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)

user_query = st.text_input(
    "Ask the AI assistant:",
    value=default_prompt,
    placeholder="e.g., What are my exam dates? or Help me make a study plan for Linear Algebra."
)

send_col, clear_col = st.columns([3, 1])
with send_col:
    send_btn = st.button("🤖 Send Query", key="ai_send_btn", use_container_width=True)
with clear_col:
    clear_btn = st.button("🗑️ Clear Chat", key="clear_chat_btn", use_container_width=True)

if clear_btn:
    st.session_state["chat_history"] = []
    st.rerun()

if send_btn and user_query.strip():
    st.session_state["chat_history"].append({"role": "user", "text": user_query})
    with st.spinner("🤖 SmartCampusAI is thinking..."):
        try:
            reply = ask_ai(user_query)
            st.session_state["chat_history"].append({"role": "assistant", "text": reply})
        except Exception as e:
            st.session_state["chat_history"].append({
                "role": "assistant",
                "text": f"❌ AI Assistant encountered an error: {e}"
            })

# ── Render Chat History ───────────────────────────────────────
if st.session_state["chat_history"]:
    st.markdown("#### 💬 Conversation:")
    for chat in reversed(st.session_state["chat_history"][-8:]):
        if chat["role"] == "user":
            st.markdown(
                f"<div class='chat-user'>👤 <strong>You:</strong> {chat['text']}</div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"<div class='chat-assistant'>🤖 <strong>Assistant:</strong><br>{chat['text']}</div>",
                unsafe_allow_html=True
            )

st.markdown("</div>", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────
st.markdown(
    """
    <div class="custom-footer">
        SmartCampusAI v2.0.0 &nbsp;|&nbsp; Academic Intelligence Console &nbsp;|&nbsp; © 2026
    </div>
    """,
    unsafe_allow_html=True
)
