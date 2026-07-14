"""
SmartCampusAI — Login Page
===========================
Secure authentication form with bcrypt password verification.
Redirects authenticated users to the dashboard.
"""

import streamlit as st
from utils.styles import apply_custom_css
from auth.auth_utils import login_user, is_logged_in

# ── Page Configuration ────────────────────────────────────────
st.set_page_config(
    page_title="SmartCampusAI — Login",
    page_icon="🔒",
    layout="wide"
)

apply_custom_css()

# ── Already logged in redirect ────────────────────────────────
if is_logged_in():
    st.info("✅ You're already signed in.")
    st.page_link("pages/3_Dashboard.py", label="Go to Your Dashboard →", icon="📊")
    st.stop()

# ── Page Header ───────────────────────────────────────────────
st.markdown(
    """
    <div style="text-align:center; padding: 32px 0 24px;">
        <div style="font-size: 3rem; margin-bottom: 12px;">🔒</div>
        <h1 class="gradient-text" style="font-size: 2.4rem;">Welcome Back</h1>
        <p style="color: #64748b; font-size: 1rem; margin-top: 4px;">
            Sign in to access your SmartCampusAI account
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# ── Two-Column Layout ─────────────────────────────────────────
col_info, col_form = st.columns([1, 1], gap="large")

# ── Left: Info Panel ──────────────────────────────────────────
with col_info:
    st.markdown(
        """
        <div class="glass-card">
            <h3 style="color:#818cf8;">🏫 Student & Faculty Portal</h3>
            <p style="color:#94a3b8; margin-bottom: 20px;">
                Log in to unlock your personalized campus experience — from AI-assisted scheduling
                to real-time attendance monitoring.
            </p>
            <div class="stat-card green">
                <strong>🛡️ Secure Login</strong><br>
                <span style="font-size:0.85rem; color:#94a3b8;">
                    Passwords protected with bcrypt — industry standard for secure credential storage.
                </span>
            </div>
            <div class="stat-card purple">
                <strong>⚡ Instant Access</strong><br>
                <span style="font-size:0.85rem; color:#94a3b8;">
                    Your session persists across pages — no repeated logins required.
                </span>
            </div>
            <div class="stat-card pink">
                <strong>🤖 AI-Powered Features</strong><br>
                <span style="font-size:0.85rem; color:#94a3b8;">
                    After login, interact with the campus AI assistant and performance analytics.
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")
    st.page_link("pages/2_Register.py", label="Don't have an account? Register here →", icon="📝")
    st.page_link("app.py", label="← Back to Home", icon="🏠")

# ── Right: Login Form ─────────────────────────────────────────
with col_form:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("<h3 style='margin-bottom:20px;'>Enter Your Credentials</h3>", unsafe_allow_html=True)

    with st.form("login_form", clear_on_submit=False):
        username_or_email = st.text_input(
            "Username or Email",
            placeholder="e.g., alex_jones or alex@university.edu",
            label_visibility="visible"
        )
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Your secure password"
        )

        st.markdown("<br>", unsafe_allow_html=True)
        submit = st.form_submit_button("🔓 Sign In", use_container_width=True)

        if submit:
            if not username_or_email or not password:
                st.error("⚠️ Please fill in all fields.")
            else:
                with st.spinner("Authenticating..."):
                    success, message = login_user(username_or_email, password)
                if success:
                    st.toast(message, icon="🚀")
                    st.success(message)
                    st.switch_page("pages/3_Dashboard.py")
                else:
                    st.error(message)

    st.markdown("</div>", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────
st.markdown(
    """
    <div class="custom-footer">
        SmartCampusAI v2.0.0 &nbsp;|&nbsp; Secure Session Login
    </div>
    """,
    unsafe_allow_html=True
)
