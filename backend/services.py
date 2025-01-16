from sqlalchemy import text
from backend.database import get_db_engine
import pandas as pd
from PIL import Image
import os
import io



def get_books():
    """Fetch books from the database and convert BLOB images to displayable format."""
    engine = get_db_engine()
    query = text("SELECT id, title, author, description, genre, pages, pdf_url, audio_url, video_url, amazon_url, image_data FROM books")

    with engine.connect() as connection:
        result = connection.execute(query)
        df = pd.DataFrame(result.fetchall(), columns=result.keys()) 

    def convert_blob_to_image_home(blob):
        """Convert BLOB data to a PIL Image if available"""
        try:
            if isinstance(blob, bytes):
                return Image.open(io.BytesIO(blob)) 
            return None
        except Exception as e:
            print(f"Error loading image: {e}")
            return None  

    df["image"] = df["image_data"].apply(convert_blob_to_image_home)
    df.drop(columns=["image_data"], inplace=True) 

    return df  


def get_book_by_id(book_id):
    """Fetch a specific book by ID."""
    engine = get_db_engine()
    if engine is None:
        return None
    
    query = text("SELECT * FROM books WHERE id = :book_id")
    with engine.connect() as connection:
        result = connection.execute(query, {"book_id": book_id}).mappings().first()
        return dict(result) if result else None

def add_book(book_data):
    """Add a new book to the database."""
    engine = get_db_engine()
    if engine is None:
        return False
    
    query = text("""
        INSERT INTO books (title, author, description, genre, pages, pdf_url, audio_url, video_url, amazon_url, image_data)
        VALUES (:title, :author, :description, :genre, :pages, :pdf_url, :audio_url, :video_url, :amazon_url, :image_data)
    """)
    
    with engine.connect() as connection:
        try:
            connection.execute(query, book_data)
            return True
        except Exception as e:
            print(f"Error adding book: {e}")
            return False

def delete_book(book_id):
    """Delete a book by ID."""
    engine = get_db_engine()
    if engine is None:
        return False
    
    query = text("DELETE FROM books WHERE id = :book_id")
    with engine.connect() as connection:
        try:
            connection.execute(query, {"book_id": book_id})
            return True
        except Exception as e:
            print(f"Error deleting book: {e}")
            return False

def convert_image_to_blob(image_file):
    try:
        return image_file.read()
    except Exception as e:
        print(f"❌ Error reading image: {e}")
        return None
    


def validate_book_data(book_data):
    """Ensure all required book fields are provided."""
    required_fields = ["title", "author", "description", "genre", "pages", "pdf_url", "audio_url", "video_url", "amazon_url", "image_data"]
    return all(field in book_data and book_data[field] for field in required_fields)

