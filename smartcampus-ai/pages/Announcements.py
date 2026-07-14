import datetime
# pyrefly: ignore [missing-import]
import streamlit as st
from dashboard import gradient_header

def show():
    if "user" not in st.session_state or st.session_state.user is None:
        st.warning("Please log in to view announcements.")
        return

    gradient_header("📢 Campus Announcements", "Stay updated with college notices, events, and examination announcements.")

    # Fetch announcements from session state (contains defaults loaded in auth.py)
    announcements = st.session_state.get("announcements", [])

    # Layout: Search bar and filter select box in columns
    col_search, col_filter = st.columns([2, 1])
    with col_search:
        search_query = st.text_input("🔍 Search notices", placeholder="Type keywords (e.g. hackathon, library, exam)...")
    with col_filter:
        categories = ["All Categories", "Academic", "Events", "Exams", "Facilities"]
        selected_category = st.selectbox("📁 Filter by Category", options=categories)

    # Filter announcements
    filtered_notices = announcements
    
    # Filter by category
    if selected_category != "All Categories":
        filtered_notices = [n for n in filtered_notices if n.get("category", "") == selected_category]
        
    # Search filter
    if search_query.strip():
        q = search_query.lower().strip()
        filtered_notices = [
            n for n in filtered_notices
            if q in n.get("title", "").lower() 
            or q in n.get("content", "").lower() 
            or q in n.get("author", "").lower()
        ]

    # Collapsible console to post a new announcement (Admin/Coordinator roleplay)
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("➕ Publish New Notice (Student Representative Mode)"):
        with st.form("publish_notice_form", clear_on_submit=True):
            n_title = st.text_input("Notice Title", placeholder="e.g. Cultural Auditions Schedule")
            n_category = st.selectbox("Category", options=["Academic", "Events", "Exams", "Facilities"])
            n_content = st.text_area("Content Description", placeholder="Write notice details here...")
            n_author = st.text_input("Publishing Authority", placeholder="e.g. Cultural Club Coordinator")
            
            submit_notice = st.form_submit_button("Broadcast Notice")
            if submit_notice:
                if not n_title.strip() or not n_content.strip() or not n_author.strip():
                    st.error("Please fill in all notice fields.")
                else:
                    now = datetime.datetime.now()
                    new_notice = {
                        "id": f"a{len(announcements) + 1}",
                        "title": n_title.strip(),
                        "content": n_content.strip(),
                        "category": n_category,
                        "date": now.strftime("%Y-%m-%d"),
                        "time": now.strftime("%I:%M %p"),
                        "author": n_author.strip()
                    }
                    # Prepend to make it appear first
                    st.session_state.announcements.insert(0, new_notice)
                    st.success("🎉 Announcement successfully broadcasted!")
                    st.rerun()

    st.markdown("<hr style='border: 1px solid rgba(255,255,255,0.05); margin: 1.5rem 0;'>", unsafe_allow_html=True)

    # Render results
    st.write(f"Showing **{len(filtered_notices)}** announcements:")
    
    if filtered_notices:
        for notice in filtered_notices:
            badge_class = f"badge-{notice.get('category', '').lower()}"
            with st.container():
                st.markdown(
                    f"""
                    <div class='announcement-card'>
                        <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;'>
                            <span class='badge {badge_class}'>{notice.get('category')}</span>
                            <small style='color: #94A3B8;'>{notice.get('date')} • {notice.get('time')}</small>
                        </div>
                        <h4 style='color: #FFFFFF; margin: 4px 0 8px 0; font-family: "Outfit", sans-serif;'>{notice.get('title')}</h4>
                        <p style='color: #E2E8F0; font-size: 0.95rem; line-height: 1.5; margin-bottom: 12px;'>
                            {notice.get('content')}
                        </p>
                        <div style='display: flex; justify-content: flex-end; align-items: center; border-top: 1px solid rgba(255, 255, 255, 0.05); padding-top: 8px;'>
                            <small style='color: #00D4FF; font-weight: 500;'>✍️ Issued by: {notice.get('author')}</small>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    else:
        st.info("🔍 No announcements found matching your filters. Try search options!")

show()
