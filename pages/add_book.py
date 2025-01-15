import streamlit as st
from backend.services import add_book, convert_image_to_blob, validate_book_data
from PIL import Image
import io

def add_book_page():
    """Render the Add Book Page."""

    if st.button("⬅ Return to Home"):
        st.session_state["page"] = "Home"
        st.rerun()

    st.title("📚 Add a New Book")

    book_data = {
        "title": st.text_input("Book Title"),
        "author": st.text_input("Author"),
        "description": st.text_area("Book Description"),
        "genre": st.multiselect("Genre", ["Fiction", "Non-fiction", "Fantasy", "Sci-Fi", "Biography", "Mystery", "Other"]),
        "pages": st.number_input("Pages", min_value=1),
        "pdf_url": st.text_input("PDF URL"),
        "audio_url": st.text_input("Audio URL"),
        "video_url": st.text_input("Video URL"),
        "amazon_url": st.text_input("Amazon URL"),
        "image_data": None 
    }

    image_file = st.file_uploader("Upload Book Cover Image", type=["jpg", "png", "jpeg"])

    if image_file:
        book_data["image_data"] = convert_image_to_blob(image_file)

        image = Image.open(image_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)

    if st.button("Save Book"):
        if validate_book_data(book_data):
            if add_book(book_data):
                st.success(f"✅ Book '{book_data['title']}' added successfully!")
                st.session_state["page"] = "Home"
                st.rerun()
            else:
                st.error("❌ Failed to add book.")
        else:
            st.error("⚠️ Please fill all required fields.")
