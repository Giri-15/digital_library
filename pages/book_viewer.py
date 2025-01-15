import streamlit as st
from PIL import Image
import io
from frontend_app.load_styles import load_css

def book_viewer():
    """Render the Book Viewer Page."""
    load_css()  

    if "selected_book" not in st.session_state or not st.session_state["selected_book"]:
        st.error("No book selected. Please go back to the home page.")
        if st.button("⬅ Return to Home"):
            st.session_state["page"] = "Home"
            st.rerun()
        return

    book = st.session_state["selected_book"]

    book_title = book.get("title", "Unknown Title")
    book_author = book.get("author", "Unknown Author")
    book_genre = book.get("genre", "Unknown Genre")
    book_pages = book.get("pages", "Unknown Pages")
    book_description = book.get("description", "No description available.")
    book_pdf_url = book.get("pdf_url")
    book_audio_url = book.get("audio_url")
    book_video_url = book.get("video_url")
    book_amazon_url = book.get("amazon_url", "#")

    

    if st.button("⬅ Return to Home"):
        st.session_state["selected_book"] = None
        st.session_state["page"] = "Home"
        st.rerun()

    with st.container():
        col1, col2 = st.columns([6, 4])

        with col1:
            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown(f"<h2 style='color: darkblue; margin-bottom: -10px;'>{book_title}</h2>", unsafe_allow_html=True)

            book_image = book.get("image")
            if book_image:
                try:
                    st.image(book_image, width=150)
                except Exception as e:
                    st.warning(f"⚠️ No valid image available. Error: {e}")

            tab_col, button_col = st.columns([7, 3])

            with tab_col:
                st.markdown("### **Select Content Type:**")
                tab_choice = st.radio(
                    "Select a content type:",
                    ["Read", "Audiobook", "Video"],
                    index=["Read", "Audiobook", "Video"].index(st.session_state.get("active_tab", "Read")),
                    horizontal=True,
                    label_visibility="collapsed"
                )

            st.markdown(f"""
        <div style="position: relative; height: 100%; display: flex; flex-direction: column; align-items: flex-end; top: 0;">
            <a href="{book_amazon_url}" target="_blank">
                <button style="background-color: darkblue; color: white; padding: 8px 10px; border: none; cursor: pointer; position: absolute; top: -60px; right: 0px; font-size: 14px;">
                    🛒 Buy on Amazon
                </button>
            </a>
        </div>
        """, unsafe_allow_html=True)

            st.session_state["active_tab"] = tab_choice

        with col2:
            st.markdown("<br><br>", unsafe_allow_html=True)

            st.write(f"**Author:** {book_author}")
            st.write(f"**Genre:** {book_genre}")
            st.write(f"**Pages:** {book_pages}")

            toggle_key = f"show_full_desc_{book_title}"
            st.session_state.setdefault(toggle_key, False)

            if st.session_state[toggle_key]:
                st.markdown(f"<p class='book-description'>{book_description}</p>", unsafe_allow_html=True)
            else:
                st.markdown(f"<p class='book-description'>{book_description[:150]}...</p>", unsafe_allow_html=True)

            if st.button("Read More" if not st.session_state[toggle_key] else "Show Less", key=f"toggle_desc_{book_title}"):
                st.session_state[toggle_key] = not st.session_state[toggle_key]
                st.rerun()

    with st.container():
        media_container = st.empty()
        media_container.empty()

        if st.session_state["active_tab"] == "Read":
            
            media_container.markdown(
                f'<iframe src="{book_pdf_url}" width="100%" height="600px"></iframe>' if book_pdf_url else "📕 E-Book not available.",
                unsafe_allow_html=True
            )

        elif st.session_state["active_tab"] == "Audiobook":

            if book_audio_url:

                if "spotify" in book_audio_url:
                    spotify_embed_url = book_audio_url.replace("open.spotify.com", "open.spotify.com/embed")
                    
                    media_container.markdown(f"""
                        <iframe src="{spotify_embed_url}" width="100%" height="232" frameborder="0" 
                                allow="autoplay; encrypted-media" style="border-radius: 12px;">
                        </iframe>
                    """, unsafe_allow_html=True)

                elif book_audio_url.endswith(".mp3") or book_audio_url.endswith(".ogg"):
                    media_container.audio(book_audio_url, format="audio/mp3")

                else:
                    media_container.write("🎧 Invalid or unsupported audio format.")

            else:
                media_container.write("🎧 Audiobook not available.")

        elif st.session_state["active_tab"] == "Video":
            media_container.video(book_video_url if book_video_url else "📺 Video not available.")