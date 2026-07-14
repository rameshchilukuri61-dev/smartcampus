import re
import streamlit as st

def is_valid_email(email: str) -> bool:
    """Validate email address format using regular expressions."""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email.strip()))

def is_valid_password(password: str) -> tuple:
    """
    Validate password complexity.
    Must be at least 6 characters, contain at least one letter and one number.
    """
    if len(password) < 6:
        return False, "Password must be at least 6 characters long."
    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one number."
    if not any(c.isalpha() for c in password):
        return False, "Password must contain at least one letter."
    return True, ""

def init_session():
    """Initialize essential session state variables for authentication and state sync."""
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "user" not in st.session_state:
        st.session_state.user = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "announcements" not in st.session_state:
        # Default starting Announcements
        st.session_state.announcements = [
            {
                "id": "a1",
                "title": "End Semester Exam Schedule Released",
                "content": "The End Semester Exams for all departments will commence on August 3rd, 2026. The detailed schedule is published on the portal and the notice boards. Please download the PDF and verify your slot dates.",
                "category": "Exams",
                "date": "2026-07-14",
                "time": "10:30 AM",
                "author": "Controller of Examinations"
            },
            {
                "id": "a2",
                "title": "Annual Tech Fest 'Innovate 2026' Registrations Open",
                "content": "Innovate 2026 is here! Events include Hackathons, Robo-Wars, Paper Presentations, and Coding Duels. Registrations are open till July 20th. Cash prizes up to $5,000 to be won!",
                "category": "Events",
                "date": "2026-07-12",
                "time": "02:00 PM",
                "author": "Student Activity Council"
            },
            {
                "id": "a3",
                "title": "Workshop: Getting Started with Deep Learning",
                "content": "A hands-on workshop on Neural Networks, CNNs, and Transformers will be conducted by industry experts from DeepMind on July 25th in Sem Hall 2. Limited seats available, registration mandatory.",
                "category": "Academic",
                "date": "2026-07-10",
                "time": "09:15 AM",
                "author": "AI Research Lab"
            },
            {
                "id": "a4",
                "title": "Campus Gym Renovation Notice",
                "content": "The central gymnasium will remain closed from July 15th to July 18th for floor resurfacing and installation of new cardio machines. We apologize for the inconvenience.",
                "category": "Facilities",
                "date": "2026-07-09",
                "time": "04:45 PM",
                "author": "Campus Administrator"
            }
        ]

def login(user_data):
    """Log in the user, set session state, and initialize context."""
    st.session_state.logged_in = True
    st.session_state.user = user_data
    # Re-initialize chat history for this user
    st.session_state.chat_history = []

def logout():
    """Clear login details and session storage, then trigger a page reload."""
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.chat_history = []
    st.rerun()
