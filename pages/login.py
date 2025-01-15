import streamlit as st
from frontend_app.load_styles import load_css
from dotenv import load_dotenv
import os

load_dotenv()

USER_CREDENTIALS = {
    os.getenv("USER1_USERNAME"): {"password": os.getenv("USER1_PASSWORD"), "role": os.getenv("USER1_ROLE")}
}

def login():
    """User Login Page"""
    if st.session_state.get("authenticated", False):
        return  

    load_css()  

    col1, col2, col3 = st.columns([3, 4, 3])  

    with col2: 
        st.markdown("<h1 style='text-align: center;'>🔐 Login Here</h1>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        username = st.text_input("Username", key="username_input")
        password = st.text_input("Password", type="password", key="password_input")

        if st.button("Login", key="login_button"):
            if username in USER_CREDENTIALS and USER_CREDENTIALS[username]["password"] == password:
                st.session_state["authenticated"] = True
                st.session_state["user_role"] = USER_CREDENTIALS[username]["role"]
                st.session_state["page"] = "Home"
                st.success(f"✅ Welcome, {username.capitalize()}!")
                st.rerun()
            else:
                st.error("❌ Incorrect username or password. Please try again.")

def logout():
    """Logs out the user and redirects to login page"""
    st.session_state.clear()
    st.session_state["authenticated"] = False
    st.session_state["user_role"] = None
    st.session_state["page"] = "Login"
    st.rerun()
