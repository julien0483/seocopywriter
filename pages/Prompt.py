import streamlit as st
import os

# Get the absolute path of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Define the file path relative to the current script's directory
file_path = os.path.join(current_dir, '..', 'prompt', 'prompt.txt')
# Function to read the file
def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Function to write to the file
def write_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)

# Read the current content of the file
try:
    current_content = read_file(file_path)
except FileNotFoundError:
    current_content = ""  # Handle case where file might not exist

# Streamlit layout
st.title("Edit Text in prompt.txt")
st.write("Edit the content of the file below:")

# Text area for editing the file content
edited_content = st.text_area("Edit here:", current_content, height=300)

# Button to save the edited content
if st.button("Save"):
    write_file(file_path, edited_content)
    st.success("File updated successfully!")
