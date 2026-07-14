import datetime
import streamlit as st
from dashboard import gradient_header, card

def show():
    # Double check authentication
    if "user" not in st.session_state or st.session_state.user is None:
        st.warning("Please log in to view this page.")
        return

    user = st.session_state.user

    # Fetch dynamic date info
    now = datetime.datetime.now()
    date_str = now.strftime("%A, %B %d, %Y")
    current_day = now.strftime("%A")

    # Header with welcome message
    gradient_header(f"Welcome back, {user['name']}! 👋", f"Portal Dashboard • {date_str}")

    # Metrics section (3 columns)
    col1, col2, col3 = st.columns(3)
    
    # Calculate overall attendance
    attendance_data = user.get("attendance", {})
    total_classes = sum(v.get("total", 0) for v in attendance_data.values())
    attended_classes = sum(v.get("attended", 0) for v in attendance_data.values())
    overall_attendance = (attended_classes / total_classes * 100) if total_classes > 0 else 0.0
    
    # Check if overall attendance is below threshold
    att_color = "#10B981" if overall_attendance >= 75 else "#EF4444"

    with col1:
        card(
            title="Overall Attendance",
            value=f"{overall_attendance:.1f}%",
            description="Minimum requirement: 75%",
            icon="📊",
            border_color=att_color
        )
    with col2:
        card(
            title="Cumulative GPA",
            value="8.92 / 10.0",
            description="Ranked Top 10% in Department",
            icon="🏆",
            border_color="#00D4FF"
        )
    with col3:
        # Get next class from timetable
        today_timetable = [slot for slot in user.get("timetable", []) if slot.get("day", "") == current_day]
        # If weekend, default to Monday
        if not today_timetable:
            today_timetable = [slot for slot in user.get("timetable", []) if slot.get("day", "") == "Monday"]
            next_class_desc = "Next class on Monday"
        else:
            next_class_desc = "Scheduled for today"
            
        next_class_val = "Free Day"
        if today_timetable:
            first_slot = today_timetable[0]
            next_class_val = f"{first_slot.get('subject')} ({first_slot.get('time')})"
            
        card(
            title="Upcoming Period",
            value=next_class_val,
            description=next_class_desc,
            icon="📅",
            border_color="#8A2BE2"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Main Grid (2 columns: Left for Timetable & Attendance, Right for announcements)
    col_left, col_right = st.columns([5, 4])

    with col_left:
        st.markdown("### 📅 Dynamic Schedule Summary")
        
        # Determine schedule display
        display_day = current_day
        is_weekend = current_day in ["Saturday", "Sunday"]
        if is_weekend:
            display_day = "Monday"
            st.info("ℹ️ Showing schedule for Monday (Weekend mode).")
            
        schedule = [slot for slot in user.get("timetable", []) if slot.get("day", "") == display_day]
        
        if schedule:
            # Styled schedule table
            html_table = "<table class='timetable-table'><tr><th>Time</th><th>Subject</th><th>Room No.</th></tr>"
            for slot in schedule:
                html_table += f"<tr><td>{slot.get('time')}</td><td><strong>{slot.get('subject')}</strong></td><td>{slot.get('room')}</td></tr>"
            html_table += "</table>"
            st.markdown(html_table, unsafe_allow_html=True)
        else:
            st.info("🎉 No classes scheduled for today!")
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Course alert warning if attendance drops
        low_att_courses = []
        for name, val in attendance_data.items():
            att = (val["attended"] / val["total"] * 100) if val["total"] > 0 else 0
            if att < 75:
                low_att_courses.append(f"{name} ({att:.0f}%)")
                
        if low_att_courses:
            st.markdown(
                f"""
                <div style='background-color: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.2); border-radius: 8px; padding: 15px;'>
                    <h5 style='color: #EF4444; margin-top: 0px; margin-bottom: 5px;'>🚨 Critical Attendance Warning</h5>
                    <p style='color: #FCA5A5; margin-bottom: 0px; font-size: 0.9rem;'>
                        Your attendance in <strong>{', '.join(low_att_courses)}</strong> is currently below the mandatory 75% limit. 
                        Please plan to attend upcoming classes to restore eligibility.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                """
                <div style='background-color: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.15); border-radius: 8px; padding: 15px;'>
                    <h5 style='color: #10B981; margin-top: 0px; margin-bottom: 5px;'>✅ Academic Eligibility Status</h5>
                    <p style='color: #A7F3D0; margin-bottom: 0px; font-size: 0.9rem;'>
                        Excellent! Your attendance is above 75% in all registered courses. You are fully eligible for semester examinations.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

    with col_right:
        st.markdown("### 📢 Important Notices")
        
        # Get announcements from session state
        notices = st.session_state.get("announcements", [])[:3] # Show top 3
        
        for notice in notices:
            badge_class = f"badge-{notice.get('category', '').lower()}"
            st.markdown(
                f"""
                <div class='announcement-card'>
                    <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;'>
                        <span class='badge {badge_class}'>{notice.get('category')}</span>
                        <small style='color: #94A3B8;'>{notice.get('date')} • {notice.get('time')}</small>
                    </div>
                    <strong style='color: #FFFFFF; font-size: 1rem;'>{notice.get('title')}</strong>
                    <p style='color: #CBD5E1; font-size: 0.88rem; margin-top: 6px; margin-bottom: 0px; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;'>
                        {notice.get('content')}
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

# Execute page display
show()
