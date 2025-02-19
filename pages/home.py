import streamlit as st
from PIL import Image as PILImage
from backend.services import get_books
from frontend_app.load_styles import load_css



def home():
    """Render the Home Page with uniformly sized book images."""
    load_css()

    st.markdown('<h1 class="fade-in">📚 Digital Library</h1>', unsafe_allow_html=True)
    st.markdown('<h2 class="bounce">Click on a book to explore it!</h2>', unsafe_allow_html=True)

    books = get_books()
    
    if books.empty:
        st.warning("⚠️ No books available.")
        return
    
    st.markdown('<div class="first-row-spacing"></div>', unsafe_allow_html=True)

    IMAGE_WIDTH, IMAGE_HEIGHT = 150, 230

    for i in range(0, len(books), 4):
        cols = st.columns(4)  
        with st.container():
            for j in range(4):
                if i + j < len(books):
                    book = books.iloc[i + j]
                    image_data = book["image"] 

                    with cols[j]:
                        if image_data:
                            try:
                               
                                if isinstance(image_data, PILImage.Image):
                                    image = image_data.resize((IMAGE_WIDTH, IMAGE_HEIGHT))
                                else:
                                   
                                    image = PILImage.open(image_data).resize((IMAGE_WIDTH, IMAGE_HEIGHT))

                                st.image(image, use_container_width=False)
                            except Exception as e:
                                st.warning(f"⚠️ Image error for {book['title']} ({e})")
                        else:
                            st.warning(f"⚠️ No valid image for {book['title']}")

                        
                        st.markdown(f"<p class='book-title'>{book['title']}</p>", unsafe_allow_html=True)

                       
                        if st.button("➡ Read More", key=f"read_more_{book['id']}"):
                            st.session_state["selected_book"] = book.to_dict()  
                            st.session_state["page"] = "View Book"
                            st.rerun()

        st.markdown('<hr style="border:1px solid gray;"/>', unsafe_allow_html=True)
