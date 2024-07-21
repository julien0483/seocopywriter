import os
import streamlit as st

# Set the path to the text file
file_path = os.path.join("prompt", "prompt.txt")

# Check if the file exists
if os.path.exists(file_path):
    # Read the content of the file
    with open(file_path, 'r') as prompt_file:
        structure_text = prompt_file.read()

    # Display the content on the screen using Streamlit
    st.write(structure_text)
else:
    st.write("The file 'prompt.txt' does not exist in the 'prompt' directory.")
