"""
SmartCampusAI — Home Page (v2 Professional)
=============================================
Official landing page with hero banner image, feature cards
with images, statistics section, and institutional branding.
"""

import os
import streamlit as st
from utils.styles import apply_custom_css, render_official_header, render_official_footer, section_heading, asset
from auth.auth_utils import is_logged_in, logout_user

# ── Page Config ───────────────────────────────────────────────
st.set_page_config(
    page_title="SmartCampusAI — Intelligent Academic Portal",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="collapsed",
)

apply_custom_css()

# ── Session State ─────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "user" not in st.session_state:
    st.session_state["user"] = None

user = st.session_state.get("user")

# ── Official Top Header ───────────────────────────────────────
render_official_header(active_page="home", user=user)

# ════════════════════════════════════════════════════════════
# HERO SECTION WITH BANNER IMAGE
# ════════════════════════════════════════════════════════════
hero_img_path = asset("hero_banner.png")

if os.path.exists(hero_img_path):
    st.markdown('<div class="hero-section">', unsafe_allow_html=True)
    st.image(hero_img_path, use_container_width=True)
    st.markdown(
        """
        <div style="
            position: relative;
            background: linear-gradient(135deg, rgba(4,5,12,0.88) 0%, rgba(15,12,40,0.65) 60%, rgba(99,38,130,0.25) 100%);
            border-radius: 0 0 24px 24px;
            padding: 36px 48px 40px;
            margin-top: -8px;
        ">
            <div class="hero-badge">✦ &nbsp; AI-POWERED CAMPUS INTELLIGENCE</div>
            <h1 class="hero-title">
                The Future of<br><span>Academic Management</span>
            </h1>
            <p class="hero-subtitle">
                SmartCampusAI unifies your schedule, attendance records, performance metrics,
                and an intelligent AI assistant into one seamless, secure portal.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)
else:
    # Fallback text hero
    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg, rgba(79,70,229,0.15) 0%, rgba(109,40,217,0.12) 50%, rgba(196,40,130,0.08) 100%);
            border-radius: 24px;
            padding: 56px 48px;
            border: 1px solid rgba(129,140,248,0.18);
            margin-bottom: 36px;
            text-align: center;
        ">
            <div class="hero-badge" style="margin: 0 auto 16px;">✦ &nbsp; AI-POWERED CAMPUS INTELLIGENCE</div>
            <h1 class="hero-title" style="text-align:center;">
                The Future of <span>Academic Management</span>
            </h1>
            <p class="hero-subtitle" style="margin: 0 auto; text-align:center;">
                SmartCampusAI unifies your schedule, attendance, performance metrics,
                and an intelligent AI assistant into one secure portal.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

# ── Auth CTA buttons ──────────────────────────────────────────
if is_logged_in():
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.page_link("pages/3_Dashboard.py", label="📊 Open My Dashboard →", icon="📊")
else:
    c1, c2, c3, c4, c5 = st.columns([1, 1.2, 0.4, 1.2, 1])
    with c2:
        st.page_link("pages/1_Login.py", label="🔒 Sign In to Portal", icon="🔒")
    with c4:
        st.page_link("pages/2_Register.py", label="📝 Create Free Account", icon="📝")

st.markdown("---")

# ════════════════════════════════════════════════════════════
# STATISTICS STRIP
# ════════════════════════════════════════════════════════════
section_heading("📊", "Platform at a Glance")

s1, s2, s3, s4 = st.columns(4, gap="medium")
stats = [
    ("s1", "indigo",  "2,400+", "Registered Students"),
    ("s2", "purple",  "180+",   "Faculty Members"),
    ("s3", "pink",    "98.7%",  "System Uptime"),
    ("s4", "emerald", "50ms",   "Avg. AI Response Time"),
]
for col, (key, color, value, label) in zip([s1, s2, s3, s4], stats):
    with col:
        st.markdown(
            f"""
            <div class="kpi-card {color}">
                <div class="kpi-value gradient-text">{value}</div>
                <div class="kpi-label">{label}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown("---")

# ════════════════════════════════════════════════════════════
# FEATURE CARDS WITH IMAGES
# ════════════════════════════════════════════════════════════
section_heading("⚡", "Core Platform Features")

fc1, fc2, fc3 = st.columns(3, gap="medium")

ai_img    = asset("ai_icon.png")
dash_img  = asset("dashboard_preview.png")
camp_img  = asset("campus_building.png")

with fc1:
    if os.path.exists(ai_img):
        st.image(ai_img, use_container_width=True)
    st.markdown(
        """
        <div class="glass-card" style="margin-top:0; border-top-left-radius:0; border-top-right-radius:0;">
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;">
                <span style="font-size:1.5rem;">🤖</span>
                <h4 style="margin:0;color:#818cf8;font-weight:700;">AI Campus Assistant</h4>
            </div>
            <p style="color:#94a3b8;font-size:0.88rem;line-height:1.7;margin:0;">
                Powered by Google Gemini and OpenAI. Ask about timetables,
                attendance policy, generate study plans, and get instant
                academic advice — available 24/7.
            </p>
            <div style="margin-top:14px;display:flex;gap:8px;flex-wrap:wrap;">
                <span class="metric-badge badge-purple">Gemini Ready</span>
                <span class="metric-badge badge-blue">OpenAI Ready</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with fc2:
    if os.path.exists(dash_img):
        st.image(dash_img, use_container_width=True)
    st.markdown(
        """
        <div class="glass-card" style="margin-top:0; border-top-left-radius:0; border-top-right-radius:0;">
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;">
                <span style="font-size:1.5rem;">📊</span>
                <h4 style="margin:0;color:#c084fc;font-weight:700;">Analytics Dashboard</h4>
            </div>
            <p style="color:#94a3b8;font-size:0.88rem;line-height:1.7;margin:0;">
                Track attendance percentages per subject, monitor GPA trends,
                view your daily timetable, and access performance insights
                on a single premium dashboard.
            </p>
            <div style="margin-top:14px;display:flex;gap:8px;flex-wrap:wrap;">
                <span class="metric-badge badge-green">Real-time Data</span>
                <span class="metric-badge badge-amber">GPA Tracker</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with fc3:
    if os.path.exists(camp_img):
        st.image(camp_img, use_container_width=True)
    st.markdown(
        """
        <div class="glass-card" style="margin-top:0; border-top-left-radius:0; border-top-right-radius:0;">
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;">
                <span style="font-size:1.5rem;">🏫</span>
                <h4 style="margin:0;color:#f472b6;font-weight:700;">Campus Intelligence</h4>
            </div>
            <p style="color:#94a3b8;font-size:0.88rem;line-height:1.7;margin:0;">
                Stay informed with official announcements, upcoming events,
                exam schedules, and live campus notifications categorized
                by priority level.
            </p>
            <div style="margin-top:14px;display:flex;gap:8px;flex-wrap:wrap;">
                <span class="metric-badge badge-red">Live Alerts</span>
                <span class="metric-badge badge-blue">Events Calendar</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")

# ════════════════════════════════════════════════════════════
# SECURITY & TRUST STRIP
# ════════════════════════════════════════════════════════════
section_heading("🔒", "Security & Compliance")

t1, t2, t3, t4 = st.columns(4, gap="medium")
trust_items = [
    ("🔐", "bcrypt Encryption",   "Passwords are hashed with bcrypt (12 rounds). Plaintext credentials are never stored."),
    ("🗄️", "JSON Database",        "Local flat-file database with OS-level file locking preventing concurrent write corruption."),
    ("🛡️", "Session Security",    "Streamlit session state is fully isolated per user and completely cleared on logout."),
    ("🔑", "Env-based Secrets",   "All API keys are stored in environment variables — never hardcoded in source code."),
]
for col, (icon, title, desc) in zip([t1, t2, t3, t4], trust_items):
    with col:
        st.markdown(
            f"""
            <div class="glass-card" style="text-align:center;padding:24px 18px;">
                <div style="font-size:2rem;margin-bottom:12px;">{icon}</div>
                <h5 style="color:#e2e8f0;font-weight:700;margin-bottom:8px;">{title}</h5>
                <p style="color:#64748b;font-size:0.82rem;line-height:1.6;margin:0;">{desc}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

# ════════════════════════════════════════════════════════════
# OFFICIAL FOOTER
# ════════════════════════════════════════════════════════════
render_official_footer()
