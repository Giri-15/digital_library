import streamlit as st
import base64
from pages.home import home
from pages.add_book import add_book_page
from pages.book_viewer import book_viewer
from pages.login import login, logout
from frontend_app.load_styles import load_css


def set_background():
    """Set background image with opacity 0.7"""
    try:
        bg_image_url = "https://raw.githubusercontent.com/Giri-15/digital_library/main/background.jpg"

        st.markdown(
            f"""
            <style>
            .stApp {{
                background: url("{bg_image_url}") no-repeat center center fixed;
                background-size: cover;
                filter: opacity(0.7); /* Set background image opacity to 70% */
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    except Exception as e:
        st.warning(f"⚠️ Error setting background: {e}")

def custom_sidebar():
    """Custom sidebar navigation for all users."""
    with st.sidebar:
        st.markdown("## 📂 Digital Library")

        if st.button("🏠 Home", key="home_button"):
            st.session_state["page"] = "Home"
            st.rerun()

        if st.button("➕ Add Book", key="add_book_button"):
            st.session_state["page"] = "Add Book"
            st.rerun()

        if st.button("🚪 Logout", key="logout_button"):
            logout()

def main():
    st.set_page_config(page_title="Digital Library", layout="wide", initial_sidebar_state="collapsed")

    load_css()
    set_background()

    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
        st.session_state["user_role"] = None
        st.session_state["page"] = "Login"

    if not st.session_state["authenticated"]:
        login()
    else:
        custom_sidebar()

        pages = {
            "Home": home,
            "Add Book": add_book_page,
            "View Book": book_viewer
        }

        st.session_state.setdefault("page", "Home")

        if st.session_state["page"] in pages:
            pages[st.session_state["page"]]()  

if __name__ == "__main__":
    main()
