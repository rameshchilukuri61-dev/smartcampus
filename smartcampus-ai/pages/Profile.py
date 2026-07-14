# pyrefly: ignore [missing-import]
import streamlit as st
from dashboard import gradient_header
from database import update_user, check_password, hash_password
from auth import is_valid_password

def show():
    if "user" not in st.session_state or st.session_state.user is None:
        st.warning("Please log in to manage your profile.")
        return

    user = st.session_state.user

    gradient_header("👤 Student Profile Settings", "Manage your personal details, academic affiliations, and security configurations.")

    # Two column layout: Left card summary, Right settings tab
    col_card, col_details = st.columns([1, 2])

    with col_card:
        # Styled profile card
        st.markdown(
            f"""
            <div class='glass-card' style='text-align: center;'>
                <div style='font-size: 5rem; margin-bottom: 10px;'>👨‍🎓</div>
                <h3 style='margin-bottom: 2px;'>{user.get('name')}</h3>
                <p style='color: #00D4FF; font-weight:600; margin-top: 0px; font-size: 0.9rem;'>{user.get('student_id')}</p>
                <hr style='border: 1px solid rgba(255,255,255,0.05); margin: 15px 0;'>
                <div style='text-align: left; font-size: 0.88rem; color: #CBD5E1;'>
                    <p style='margin-bottom:8px;'>🏢 <strong>Department</strong>: {user.get('department')}</p>
                    <p style='margin-bottom:8px;'>📧 <strong>Email</strong>: {user.get('email')}</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_details:
        tab_prof, tab_sec = st.tabs(["📝 Edit Profile Details", "🛡️ Account Security"])
        
        with tab_prof:
            with st.form("edit_profile_form"):
                new_name = st.text_input("Full Name", value=user.get("name"))
                
                departments = [
                    "Computer Science (CSE)",
                    "Electronics & Communication (ECE)",
                    "Electrical Engineering (EEE)",
                    "Mechanical Engineering (ME)",
                    "Civil Engineering (CE)",
                    "Information Technology (IT)"
                ]
                # Try to find current department index
                curr_dept = user.get("department", "")
                dept_index = 0
                for i, d in enumerate(departments):
                    if curr_dept in d:
                        dept_index = i
                        break
                        
                new_dept = st.selectbox("Department", options=departments, index=dept_index)
                
                # Structural IDs remain disabled/read-only for security integrity
                st.text_input("Student ID (Read-only)", value=user.get("student_id"), disabled=True)
                st.text_input("Registered Email (Read-only)", value=user.get("email"), disabled=True)
                
                submit_prof = st.form_submit_button("Update Settings")
                if submit_prof:
                    if not new_name.strip():
                        st.error("Name cannot be blank.")
                    else:
                        dept_clean = new_dept.split(" (")[0]
                        updated_fields = {
                            "name": new_name.strip(),
                            "department": dept_clean
                        }
                        # Update DB
                        if update_user(user["email"], updated_fields):
                            # Sync session state
                            user["name"] = new_name.strip()
                            user["department"] = dept_clean
                            st.session_state.user = user
                            st.success("🎉 Profile updated successfully!")
                            st.rerun()
                        else:
                            st.error("❌ Failed to save updates to the database.")

        with tab_sec:
            with st.form("edit_password_form"):
                st.write("#### 🔑 Update Account Password")
                current_pw = st.text_input("Current Password", type="password", placeholder="••••••••")
                new_pw = st.text_input("New Password", type="password", placeholder="At least 6 chars (letters + numbers)")
                confirm_pw = st.text_input("Confirm New Password", type="password", placeholder="••••••••")
                
                submit_sec = st.form_submit_button("Change Password")
                if submit_sec:
                    # Input validation
                    if not current_pw or not new_pw or not confirm_pw:
                        st.error("⚠️ All password fields are required.")
                    elif new_pw != confirm_pw:
                        st.error("⚠️ New passwords do not match.")
                    else:
                        # Authenticate current password
                        if not check_password(current_pw, user.get("password", "")):
                            st.error("❌ Current password incorrect. Verification failed.")
                        else:
                            # Validate complexity
                            ok, msg = is_valid_password(new_pw)
                            if not ok:
                                st.error(f"⚠️ {msg}")
                            else:
                                # Hash and store new password
                                updated_fields = {
                                    "password": hash_password(new_pw)
                                }
                                if update_user(user["email"], updated_fields):
                                    # Sync password in session state
                                    user["password"] = updated_fields["password"]
                                    st.session_state.user = user
                                    st.success("🎉 Password updated successfully!")
                                else:
                                    st.error("❌ Error updating password in database.")

show()
