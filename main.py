import streamlit as st
from pages.home import home
from pages.add_book import add_book_page
from pages.book_viewer import book_viewer
from frontend_app.load_styles import load_css, set_background

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

def main():
    st.set_page_config(page_title="Digital Library", layout="wide", initial_sidebar_state="collapsed")

    load_css()
    set_background("https://raw.githubusercontent.com/Giri-15/digital_library/main/background.jpg", opacity=0.7)

    # Initialize the session state for page navigation
    st.session_state.setdefault("page", "Home")

    custom_sidebar()

    pages = {
        "Home": home,
        "Add Book": add_book_page,
        "View Book": book_viewer
    }

    if st.session_state["page"] in pages:
        pages[st.session_state["page"]]()

if __name__ == "__main__":
    main()
