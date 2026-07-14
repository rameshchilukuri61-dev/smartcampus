import math
import streamlit as st
from dashboard import gradient_header, card
from database import update_user

def calculate_consecutive_needed(attended, total, target=75):
    """Calculate the number of consecutive classes a student must attend to reach the target."""
    if total == 0:
        return 0
    current_percentage = (attended / total) * 100
    if current_percentage >= target:
        return 0
    
    t_val = target / 100.0
    # Formula: (attended + x) / (total + x) >= target_ratio
    # => attended + x >= target_ratio * total + target_ratio * x
    # => x * (1 - target_ratio) >= target_ratio * total - attended
    # => x >= (target_ratio * total - attended) / (1 - target_ratio)
    needed = (t_val * total - attended) / (1.0 - t_val)
    return max(0, math.ceil(needed))

def calculate_missable_classes(attended, total, target=75):
    """Calculate the number of classes a student can miss before falling below the target."""
    if total == 0 or (attended / total * 100) < target:
        return 0
    
    t_val = target / 100.0
    # Formula: attended / (total + y) >= target_ratio
    # => attended >= target_ratio * total + target_ratio * y
    # => target_ratio * y <= attended - target_ratio * total
    # => y <= (attended - target_ratio * total) / target_ratio
    # => y <= (attended / target_ratio) - total
    missable = (attended / t_val) - total
    return max(0, math.floor(missable))

def show():
    if "user" not in st.session_state or st.session_state.user is None:
        st.warning("Please log in to track your attendance.")
        return

    user = st.session_state.user
    attendance = user.get("attendance", {})

    gradient_header("📊 Academic Attendance Tracker", "Manage your class percentages and calculate target requirements.")

    # Calculate overall attendance
    total_conducted = sum(v.get("total", 0) for v in attendance.values())
    total_attended = sum(v.get("attended", 0) for v in attendance.values())
    overall_p = (total_attended / total_conducted * 100) if total_conducted > 0 else 0.0

    # Layout overview metrics
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    with col_stat1:
        color = "#10B981" if overall_p >= 75 else "#EF4444"
        card("Overall Attendance", f"{overall_p:.1f}%", "University target is 75%", "📉" if overall_p < 75 else "📈", color)
    with col_stat2:
        card("Total Classes Attended", f"{total_attended} classes", f"Out of {total_conducted} lectures", "🏫", "#6C63FF")
    with col_stat3:
        status_text = "Good Standing" if overall_p >= 75 else "Attendance Shortage"
        status_color = "#10B981" if overall_p >= 75 else "#EF4444"
        card("Eligibility Status", status_text, "Required for exams", "🎓", status_color)

    st.markdown("<hr style='border: 1px solid rgba(255,255,255,0.05); margin: 2rem 0;'>", unsafe_allow_html=True)

    # Attendance logs list and class adjustments
    st.markdown("### 📚 Subject-Wise Lecture Logs")
    
    # We will display columns for each subject
    for subject, record in attendance.items():
        attended = record.get("attended", 0)
        total = record.get("total", 0)
        percentage = (attended / total * 100) if total > 0 else 0.0
        
        # Determine status bar color and thresholds
        if percentage >= 85:
            bar_color = "success"
            text_color = "#10B981"
            emoji = "🟢 Excellent"
        elif percentage >= 75:
            bar_color = "info"
            text_color = "#6C63FF"
            emoji = "🟡 Satisfactory"
        else:
            bar_color = "danger"
            text_color = "#EF4444"
            emoji = "🔴 Critical Limit"

        # Inside a glass card, render columns
        with st.container():
            st.markdown(f"<div class='glass-card'>", unsafe_allow_html=True)
            
            c1, c2, c3 = st.columns([4, 4, 3])
            
            with c1:
                st.markdown(f"<h4 style='margin-bottom:2px;'>{subject}</h4>", unsafe_allow_html=True)
                st.markdown(f"<span style='color: {text_color}; font-weight:600; font-size:0.9rem;'>{emoji} ({percentage:.1f}%)</span>", unsafe_allow_html=True)
                st.progress(percentage / 100.0)
                st.write(f"Attended: **{attended}** | Conducted: **{total}**")
                
            with c2:
                # Direct interaction buttons to log attendance in session state and JSON DB
                st.write("🔧 **Log Today's Lecture**")
                btn_col1, btn_col2 = st.columns(2)
                with btn_col1:
                    if st.button("➕ Present", key=f"pres_{subject}", use_container_width=True):
                        # Update session user
                        user["attendance"][subject]["attended"] += 1
                        user["attendance"][subject]["total"] += 1
                        # Update database
                        if update_user(user["email"], {"attendance": user["attendance"]}):
                            st.success(f"Logged Present in {subject}")
                            st.rerun()
                with btn_col2:
                    if st.button("➖ Absent", key=f"abs_{subject}", use_container_width=True):
                        # Update session user
                        user["attendance"][subject]["total"] += 1
                        # Update database
                        if update_user(user["email"], {"attendance": user["attendance"]}):
                            st.success(f"Logged Absent in {subject}")
                            st.rerun()
                            
            with c3:
                # Custom calculator block
                st.write("📊 **Calculations**")
                if percentage < 75:
                    needed = calculate_consecutive_needed(attended, total, 75)
                    st.markdown(
                        f"<p style='color:#FCA5A5; font-size:0.85rem; margin-bottom: 0px;'>⚠️ Must attend <strong>{needed}</strong> consecutive lectures to reach 75%.</p>",
                        unsafe_allow_html=True
                    )
                else:
                    missable = calculate_missable_classes(attended, total, 75)
                    if missable > 0:
                        st.markdown(
                            f"<p style='color:#A7F3D0; font-size:0.85rem; margin-bottom: 0px;'>✅ You can safely miss up to <strong>{missable}</strong> lectures without dropping below 75%.</p>",
                            unsafe_allow_html=True
                        )
                    else:
                        st.markdown(
                            f"<p style='color:#E2E8F0; font-size:0.85rem; margin-bottom: 0px;'>⚖️ On the border! You cannot miss the next class.</p>",
                            unsafe_allow_html=True
                        )
            
            st.markdown("</div>", unsafe_allow_html=True)
            
    # Interactive Custom Target Calculator
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🧮 Custom Target Attendance Calculator")
    
    with st.expander("Calculate requirements for arbitrary attendance goals"):
        calc_col1, calc_col2, calc_col3 = st.columns(3)
        with calc_col1:
            sub_choice = st.selectbox("Select Subject", options=list(attendance.keys()))
        with calc_col2:
            target_goal = st.number_input("Target Percentage (%)", min_value=1.0, max_value=100.0, value=80.0, step=5.0)
        with calc_col3:
            st.write("")
            st.write("")
            calc_btn = st.button("Compute Target", use_container_width=True)
            
        if calc_btn:
            sub_rec = attendance[sub_choice]
            sub_att = sub_rec["attended"]
            sub_tot = sub_rec["total"]
            current_sub_p = (sub_att / sub_tot * 100) if sub_tot > 0 else 0
            
            st.markdown(f"**Current attendance in {sub_choice}**: `{sub_att}/{sub_tot}` ({current_sub_p:.1f}%)")
            
            if current_sub_p < target_goal:
                consec = calculate_consecutive_needed(sub_att, sub_tot, target_goal)
                st.warning(
                    f"👉 To achieve **{target_goal}%** attendance, you need to attend the next **{consec}** classes of **{sub_choice}** consecutively without missing."
                )
            else:
                miss = calculate_missable_classes(sub_att, sub_tot, target_goal)
                st.success(
                    f"👉 You are currently exceeding your goal! You can afford to miss up to **{miss}** classes in **{sub_choice}** before falling below **{target_goal}%**."
                )

show()
