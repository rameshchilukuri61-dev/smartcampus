"""
SmartCampusAI — Registration Page
====================================
New user account creation with bcrypt-hashed password storage,
full input validation, and JSON database persistence.
"""

import streamlit as st
from utils.styles import apply_custom_css
from auth.auth_utils import register_user, is_logged_in

# ── Page Configuration ────────────────────────────────────────
st.set_page_config(
    page_title="SmartCampusAI — Register",
    page_icon="📝",
    layout="wide"
)

apply_custom_css()

# ── Already logged in redirect ────────────────────────────────
if is_logged_in():
    st.info("✅ You already have an active session.")
    st.page_link("pages/3_Dashboard.py", label="Go to Dashboard →", icon="📊")
    st.stop()

# ── Page Header ───────────────────────────────────────────────
st.markdown(
    """
    <div style="text-align:center; padding: 32px 0 24px;">
        <div style="font-size: 3rem; margin-bottom: 12px;">📝</div>
        <h1 class="gradient-text" style="font-size: 2.4rem;">Create Your Account</h1>
        <p style="color: #64748b; font-size: 1rem; margin-top: 4px;">
            Join SmartCampusAI — registration takes under 30 seconds
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
            <h3 style="color:#c084fc;">🔐 Secure Registration</h3>
            <p style="color:#94a3b8; margin-bottom:20px;">
                Your data is protected from day one. Passwords are hashed with bcrypt 
                before storage — your plaintext password is never saved.
            </p>

            <div class="stat-card purple">
                <strong>📋 Requirements</strong><br>
                <ul style="margin:8px 0 0; color:#94a3b8; font-size:0.88rem; padding-left:18px;">
                    <li>Username: 3–30 characters, letters/numbers/underscores only</li>
                    <li>Email: Valid institutional or personal address</li>
                    <li>Password: Minimum 6 characters</li>
                </ul>
            </div>

            <div class="stat-card green">
                <strong>🔒 Data Privacy</strong><br>
                <span style="font-size:0.85rem; color:#94a3b8;">
                    All data is stored locally in a JSON database. No third-party sharing. 
                    No tracking. Complete academic privacy guaranteed.
                </span>
            </div>

            <div class="stat-card" style="border-left-color:#818cf8;">
                <strong>⚡ What You Get</strong><br>
                <ul style="margin:8px 0 0; color:#94a3b8; font-size:0.88rem; padding-left:18px;">
                    <li>Personalized campus dashboard</li>
                    <li>AI-powered schedule assistant</li>
                    <li>Attendance & performance tracker</li>
                    <li>Real-time campus announcements</li>
                </ul>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")
    st.page_link("pages/1_Login.py", label="Already have an account? Sign in →", icon="🔒")
    st.page_link("app.py", label="← Back to Home", icon="🏠")

# ── Right: Registration Form ──────────────────────────────────
with col_form:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("<h3 style='margin-bottom:20px;'>Registration Details</h3>", unsafe_allow_html=True)

    with st.form("register_form", clear_on_submit=False):
        username = st.text_input(
            "Choose a Username",
            placeholder="e.g., alex_jones"
        )
        email = st.text_input(
            "Email Address",
            placeholder="e.g., alex.jones@university.edu"
        )
        password = st.text_input(
            "Create Password",
            type="password",
            placeholder="Minimum 6 characters"
        )
        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            placeholder="Repeat your password"
        )

        # Live password strength indicator
        if password:
            strength = len(password)
            if strength < 6:
                st.warning("⚠️ Password too short")
            elif strength < 10:
                st.info("🔑 Password: Moderate strength")
            else:
                st.success("🛡️ Password: Strong")

        st.markdown("<br>", unsafe_allow_html=True)
        submit = st.form_submit_button("🚀 Create Account", use_container_width=True)

        if submit:
            with st.spinner("Creating your account..."):
                success, message = register_user(username, email, password, confirm_password)

            if success:
                st.toast(message, icon="✅")
                st.success(message)
                st.info("🔀 Redirecting to Login page...")
                import time
                time.sleep(1)
                st.switch_page("pages/1_Login.py")
            else:
                st.error(message)

    st.markdown("</div>", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────
st.markdown(
    """
    <div class="custom-footer">
        SmartCampusAI v2.0.0 &nbsp;|&nbsp; Secure Account Registration
    </div>
    """,
    unsafe_allow_html=True
)
