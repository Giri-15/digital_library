import streamlit as st


def load_css():
    """Load external CSS for styling."""
    try:
        with open("frontend_app/styles.css", "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("⚠️ CSS file not found. Using default styling.")