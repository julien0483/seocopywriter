import streamlit as st
from docx import Document
from io import BytesIO

# Function to create a Word document
def create_word_doc(texts):
    doc = Document()
    for text in texts:
        doc.add_paragraph(text)
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# Streamlit app
st.title("Text to Word Converter")

# Text input from user
text1 = st.text_area("Enter your first text here:")
text2 = st.text_area("Enter your second text here:")

# Button to generate Word document
if st.button("Generate Word Document"):
    if text1 and text2:
        combined_texts = [text1, text2]
        word_buffer = create_word_doc(combined_texts)
        st.download_button(label="Download Word Document",
                           data=word_buffer,
                           file_name="combined_texts.docx",
                           mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    else:
        st.warning("Please enter text in both fields.")
