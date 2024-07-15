import streamlit as st
import os
from pathlib import Path

# Define the folder to save PDF templates
PDF_TEMPLATES_FOLDER = Path("pdf_templates")
PDF_TEMPLATES_FOLDER.mkdir(exist_ok=True)

# Function to save uploaded file
def save_uploaded_file(uploaded_file):
    try:
        with open(PDF_TEMPLATES_FOLDER / uploaded_file.name, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return True
    except Exception as e:
        st.error(f"Error: {e}")
        return False

# Function to list all PDFs
def list_pdfs():
    return [f for f in PDF_TEMPLATES_FOLDER.iterdir() if f.is_file() and f.suffix == '.pdf']

# Function to delete a PDF file
def delete_pdf(file_path):
    try:
        os.remove(file_path)
        st.success(f"Deleted {file_path.name}")
    except Exception as e:
        st.error(f"Error: {e}")

# Streamlit layout
st.title("PDF Templates Manager")

# Section for uploading PDFs
st.header("Upload PDF Template")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
if uploaded_file is not None:
    if save_uploaded_file(uploaded_file):
        st.success(f"Uploaded {uploaded_file.name}")

# Section for viewing and deleting PDFs
st.header("Manage PDF Templates")
pdf_files = list_pdfs()

if pdf_files:
    for pdf_file in pdf_files:
        col1, col2 = st.columns([4, 1])
        col1.write(pdf_file.name)
        if col2.button("Delete", key=pdf_file.name):
            delete_pdf(pdf_file)
else:
    st.info("No PDF templates found.")
