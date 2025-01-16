import streamlit as st


def load_css():
    """Load external CSS for styling."""
    try:
        with open("frontend_app/styles.css", "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("⚠️ CSS file not found. Using default styling.")

def set_background(image_url, opacity=0.7):
    """Set background image from an online source with adjustable opacity."""
    st.markdown(f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(255, 255, 255, {opacity}), rgba(255, 255, 255, {opacity})), 
                        url("{image_url}") no-repeat center fixed;
            background-size: cover;
        }}
        </style>
    """, unsafe_allow_html=True)


