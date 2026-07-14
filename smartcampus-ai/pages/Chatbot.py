import streamlit as st
from dashboard import gradient_header
from ai_engine import generate_response

def show():
    # Verify authentication
    if "user" not in st.session_state or st.session_state.user is None:
        st.warning("Please log in to use the AI Chatbot.")
        return

    gradient_header("💬 SmartCampus AI Assistant", "Ask about campus guidelines, timetable, canteen, WiFi, or exam details.")

    # Initialize chat history inside session state if missing
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display introductory system block
    if len(st.session_state.chat_history) == 0:
        st.markdown(
            """
            <div style='background: rgba(255, 255, 255, 0.02); border: 1px dashed rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 20px; margin-bottom: 20px;'>
                <h4 style='color: #00D4FF; margin-top: 0px;'>Hello! I am your SmartCampus AI Assistant.</h4>
                <p style='color: #94A3B8; font-size: 0.92rem; margin-bottom: 12px;'>
                    I have access to university guidelines and student info. Try clicking one of the sample prompts below, or type your own question in the input field!
                </p>
                <div style='display: flex; flex-wrap: wrap; gap: 8px;'>
                    <span style='background: rgba(108, 99, 255, 0.1); border: 1px solid rgba(108, 99, 255, 0.3); border-radius: 20px; padding: 4px 12px; font-size: 0.8rem; color: #8F8BFF;'>What is the minimum attendance?</span>
                    <span style='background: rgba(0, 212, 255, 0.1); border: 1px solid rgba(0, 212, 255, 0.3); border-radius: 20px; padding: 4px 12px; font-size: 0.8rem; color: #6BE7FF;'>Canteen menu and timings</span>
                    <span style='background: rgba(138, 43, 226, 0.1); border: 1px solid rgba(138, 43, 226, 0.3); border-radius: 20px; padding: 4px 12px; font-size: 0.8rem; color: #C59BFF;'>How do I connect to Campus Wi-Fi?</span>
                    <span style='background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 20px; padding: 4px 12px; font-size: 0.8rem; color: #A7F3D0;'>Where is the Central Library?</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Sidebar controls
    with st.sidebar:
        st.markdown("### ⚙️ Chat Options")
        if st.button("Clear Conversation History", key="clear_chat_btn", use_container_width=True):
            st.session_state.chat_history = []
            st.success("Conversation cleared!")
            st.rerun()

    # Display past chat messages
    for msg in st.session_state.chat_history:
        avatar = "👤" if msg["role"] == "user" else "🤖"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

    # User chat entry
    if prompt := st.chat_input("Ask a campus question..."):
        # Display student message
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
            
        # Log to history
        st.session_state.chat_history.append({"role": "user", "content": prompt})

        # Process and generate AI response
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("SmartCampus AI is thinking..."):
                response = generate_response(prompt, st.session_state.chat_history)
                st.markdown(response)

        # Log bot reply to history
        st.session_state.chat_history.append({"role": "assistant", "content": response})

show()
