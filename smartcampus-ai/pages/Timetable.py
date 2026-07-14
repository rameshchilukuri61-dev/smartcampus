# pyrefly: ignore [missing-import]
import streamlit as st
from dashboard import gradient_header
from database import update_user
import uuid

def show():
    if "user" not in st.session_state or st.session_state.user is None:
        st.warning("Please log in to manage your timetable.")
        return

    user = st.session_state.user
    timetable = user.get("timetable", [])

    gradient_header("📅 Lecture Timetable Planner", "Customize your weekly schedule, class times, and lecture hall locations.")

    # Sidebar Options
    with st.sidebar:
        st.markdown("### 🛠️ Schedule Settings")
        
        # Form to add new schedule slots
        st.markdown("**Add Schedule Slot**")
        with st.form("add_slot_form", clear_on_submit=True):
            day_opt = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
            day = st.selectbox("Day of Week", options=day_opt)
            
            time_opt = [
                "09:00 - 10:00",
                "10:15 - 11:15",
                "11:30 - 12:30",
                "12:30 - 13:30 (Lunch)",
                "13:30 - 14:30",
                "14:45 - 15:45",
                "16:00 - 17:00"
            ]
            time_slot = st.selectbox("Time Duration", options=time_opt)
            
            # Subject field
            subjects = list(user.get("attendance", {}).keys()) + ["Seminar", "Lab Practical", "Club Meeting", "Other"]
            subject = st.selectbox("Subject/Event", options=subjects)
            
            # Custom subject if other selected
            custom_subject = st.text_input("Custom Title (Optional)", placeholder="Use if 'Other' selected")
            
            room = st.text_input("Lecture Room / Hall", placeholder="e.g. LH-104 or Lab-3")
            
            submit_slot = st.form_submit_button("Add to Timetable")
            if submit_slot:
                final_subject = custom_subject.strip() if subject == "Other" and custom_subject.strip() else subject
                if not room.strip():
                    st.error("Please enter a room location.")
                else:
                    new_slot = {
                        "id": str(uuid.uuid4())[:8],
                        "day": day,
                        "time": time_slot,
                        "subject": final_subject,
                        "room": room.strip().upper()
                    }
                    # Check duplicate day/time combination
                    if any(s.get("day") == day and s.get("time") == time_slot for s in timetable):
                        st.error(f"Collision detected! A slot already exists on {day} during {time_slot}.")
                    else:
                        timetable.append(new_slot)
                        user["timetable"] = timetable
                        if update_user(user["email"], {"timetable": timetable}):
                            st.success(f"Added {final_subject} on {day} at {time_slot}!")
                            st.rerun()

    # Main view: List by day of week
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    
    # Select day tab
    selected_tab = st.selectbox("📅 Filter Schedule by Day", options=["Weekly Grid View"] + days_of_week)

    if selected_tab == "Weekly Grid View":
        st.markdown("### 🗓️ Weekly Schedule Summary")
        
        # We will render a beautifully formatted weekly schedule
        for day in days_of_week:
            day_slots = [s for s in timetable if s.get("day") == day]
            # Sort slots by time range
            day_slots = sorted(day_slots, key=lambda x: x.get("time", ""))
            
            st.markdown(f"#### 📅 {day}")
            if day_slots:
                # Build custom HTML table
                html_table = "<table class='timetable-table'><tr><th>Time Slot</th><th>Subject</th><th>Room Location</th></tr>"
                for slot in day_slots:
                    html_table += f"<tr><td>{slot.get('time')}</td><td><strong>{slot.get('subject')}</strong></td><td>{slot.get('room')}</td></tr>"
                html_table += "</table>"
                st.markdown(html_table, unsafe_allow_html=True)
            else:
                st.markdown("<p style='color:#94A3B8; font-style:italic;'>No lectures scheduled.</p>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            
    else:
        # Display schedule details for specific day with DELETE buttons
        st.markdown(f"### 🗓️ Lecture list for {selected_tab}")
        day_slots = [s for s in timetable if s.get("day") == selected_tab]
        day_slots = sorted(day_slots, key=lambda x: x.get("time", ""))
        
        if day_slots:
            for i, slot in enumerate(day_slots):
                with st.container():
                    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                    col1, col2, col3 = st.columns([5, 3, 2])
                    with col1:
                        st.markdown(f"<h4 style='margin:0px;'>{slot.get('subject')}</h4>", unsafe_allow_html=True)
                        st.write(f"⏰ **Time**: {slot.get('time')}")
                    with col2:
                        st.write(f"🏢 **Location**: Room `{slot.get('room')}`")
                    with col3:
                        # Delete action
                        # Use a unique key
                        slot_id = slot.get("id", str(i))
                        if st.button("🗑️ Delete", key=f"del_{slot_id}", use_container_width=True):
                            # Remove slot
                            timetable = [s for s in timetable if s.get("id", str(i)) != slot_id]
                            user["timetable"] = timetable
                            if update_user(user["email"], {"timetable": timetable}):
                                st.success("Slot deleted successfully!")
                                st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info(f"No lectures scheduled for {selected_tab}. Enjoy your free time!")

show()
