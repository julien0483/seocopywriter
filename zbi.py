import streamlit as st
from docx import Document#exceptions
from io import BytesIO

# Function to create a Word document
def create_word_doc(text):
    doc = Document()
    doc.add_paragraph(text)
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# Streamlit app
st.title("Text to Word/PDF Converter")

# Text input from user
user_text = st.text_area("Enter your text here:")

# Button to generate Word document
if st.button("Generate Word Document"):
    if user_text:
        word_buffer = create_word_doc(user_text)
        st.download_button(label="Download Word Document",
                           data=word_buffer,
                           file_name="user_text.docx",
                           mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    else:
        st.warning("Please enter some text.")

# You can similarly add a PDF generation and download functionality if needed
