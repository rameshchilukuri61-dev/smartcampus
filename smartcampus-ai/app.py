import os
import streamlit as st
from dotenv import load_dotenv

# Set page config at the very top
st.set_page_config(
    page_title="SmartCampus AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load environment variables
load_dotenv()

# Import local auth and database helpers
from auth import init_session, logout, is_valid_email, is_valid_password, login as auth_login
from database import authenticate_user, register_user

# Initialize user session
init_session()

def inject_custom_css():
    """Reads assets/styles.css and injects it into the Streamlit app container."""
    css_path = os.path.join(os.path.dirname(__file__), "assets", "styles.css")
    if os.path.exists(css_path):
        try:
            with open(css_path, "r") as f:
                css_content = f.read()
            st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
        except Exception as e:
            print(f"Error loading CSS: {e}")

def show_login():
    """Render the student login page."""
    inject_custom_css()
    
    col1, col2 = st.columns([1, 5])
    with col1:
        logo_path = os.path.join("assets", "logo.png")
        if os.path.exists(logo_path):
            st.image(logo_path, width=80)
    with col2:
        st.markdown("<h1 class='gradient-text' style='margin-bottom:0px; font-size: 2.3rem;'>SmartCampus AI</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color:#94A3B8; margin-top:-5px; font-size:0.95rem;'>Your Intelligent Academic Companion</p>", unsafe_allow_html=True)
    
    st.markdown("<hr style='border: 1px solid rgba(255,255,255,0.05); margin: 1.5rem 0;'>", unsafe_allow_html=True)
    
    # Form Container
    col_c, _ = st.columns([2, 1])
    with col_c:
        st.markdown("### 🔒 Student Portal Login")
        with st.form("login_form", clear_on_submit=False):
            email = st.text_input("Institutional Email Address", placeholder="e.g. student@example.com")
            password = st.text_input("Password", type="password", placeholder="••••••••")
            remember_me = st.checkbox("Remember me on this device")
            
            submit = st.form_submit_button("Sign In")
            if submit:
                if not email or not password:
                    st.error("⚠️ Email and password are required.")
                elif not is_valid_email(email):
                    st.error("⚠️ Please enter a valid email address.")
                else:
                    user = authenticate_user(email, password)
                    if user:
                        auth_login(user)
                        st.success("🎉 Login successful! Loading dashboard...")
                        st.rerun()
                    else:
                        st.error("❌ Invalid email or password. Please try again.")

def show_register():
    """Render the student registration page."""
    inject_custom_css()
    
    col1, col2 = st.columns([1, 5])
    with col1:
        logo_path = os.path.join("assets", "logo.png")
        if os.path.exists(logo_path):
            st.image(logo_path, width=80)
    with col2:
        st.markdown("<h1 class='gradient-text' style='margin-bottom:0px; font-size: 2.3rem;'>SmartCampus AI</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color:#94A3B8; margin-top:-5px; font-size:0.95rem;'>Your Intelligent Academic Companion</p>", unsafe_allow_html=True)
        
    st.markdown("<hr style='border: 1px solid rgba(255,255,255,0.05); margin: 1.5rem 0;'>", unsafe_allow_html=True)
    
    col_c, _ = st.columns([2, 1])
    with col_c:
        st.markdown("### 📝 Student Registration")
        with st.form("register_form"):
            name = st.text_input("Full Name", placeholder="e.g. Jane Doe")
            email = st.text_input("Institutional Email Address", placeholder="e.g. jane@example.com")
            student_id = st.text_input("Student ID / Roll Number", placeholder="e.g. 23CS002")
            
            departments = [
                "Computer Science (CSE)",
                "Electronics & Communication (ECE)",
                "Electrical Engineering (EEE)",
                "Mechanical Engineering (ME)",
                "Civil Engineering (CE)",
                "Information Technology (IT)"
            ]
            department = st.selectbox("Department", options=departments)
            
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                password = st.text_input("Password", type="password", placeholder="At least 6 characters (letter+number)")
            with col_p2:
                confirm_password = st.text_input("Confirm Password", type="password", placeholder="••••••••")
                
            submit = st.form_submit_button("Register Account")
            if submit:
                if not name or not email or not student_id or not password or not confirm_password:
                    st.error("⚠️ All fields are required.")
                elif not is_valid_email(email):
                    st.error("⚠️ Please enter a valid email address.")
                elif password != confirm_password:
                    st.error("⚠️ Passwords do not match.")
                else:
                    ok, msg = is_valid_password(password)
                    if not ok:
                        st.error(f"⚠️ {msg}")
                    else:
                        dept_name = department.split(" (")[0]
                        success, res = register_user(name, email, student_id, dept_name, password)
                        if success:
                            st.success("🎉 Registration successful! Use the navigation menu on the left to head to the Login page.")
                        else:
                            st.error(f"❌ Registration failed: {res}")

# Setup page routing using modern Streamlit navigation API
if not st.session_state.logged_in:
    # Pages when unauthenticated
    login_page = st.Page(show_login, title="Login", icon="🔒")
    register_page = st.Page(show_register, title="Register", icon="📝")
    
    pg = st.navigation({
        "Authentication Portal": [login_page, register_page]
    })
else:
    # Pages when authenticated (pointing to files in the pages/ directory)
    home_page = st.Page("pages/Home.py", title="Home Dashboard", icon="🏠")
    chatbot_page = st.Page("pages/Chatbot.py", title="AI Assistant", icon="💬")
    attendance_page = st.Page("pages/Attendance.py", title="Attendance", icon="📊")
    timetable_page = st.Page("pages/Timetable.py", title="Timetable", icon="📅")
    announcements_page = st.Page("pages/Announcements.py", title="Announcements", icon="📢")
    profile_page = st.Page("pages/Profile.py", title="Profile", icon="👤")
    
    pg = st.navigation({
        "Portal": [home_page, chatbot_page],
        "Academic Tracker": [attendance_page, timetable_page],
        "General & Profile": [announcements_page, profile_page]
    })

# Apply global styling
inject_custom_css()

# Render sidebar header if logged in
if st.session_state.logged_in:
    st.sidebar.markdown(
        f"""
        <div style='text-align: center; margin-bottom: 20px;'>
            <h2 style='color:#00D4FF; margin-bottom: 0px;'>SmartCampus AI</h2>
            <p style='color:#94A3B8; font-size: 0.8rem; margin-top: 0px;'>Hello, {st.session_state.user['name']}</p>
        </div>
        """, 
        unsafe_allow_html=True
    )

# Execute the routed page logic
pg.run()

# Render logout action at the bottom of the sidebar if logged in
if st.session_state.logged_in:
    st.sidebar.markdown("<br><hr style='border: 1px solid rgba(255,255,255,0.05);'>", unsafe_allow_html=True)
    st.sidebar.write(f"🏷️ **ID**: `{st.session_state.user['student_id']}`")
    st.sidebar.write(f"🏢 **Dept**: `{st.session_state.user['department']}`")
    if st.sidebar.button("Logout", key="sidebar_logout_btn", use_container_width=True):
        logout()
