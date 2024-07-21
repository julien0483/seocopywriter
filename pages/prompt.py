import os
import streamlit as st

# Set the path to the text file
file_path = os.path.join("prompt", "prompt.txt")

# Check if the file exists
if os.path.exists(file_path):
    # Read the content of the file
    with open(file_path, 'r') as prompt_file:
        structure_text = prompt_file.read()
else:
    structure_text = ""

# Display the text area for editing the content
edited_text = st.text_area("Edit the content of prompt.txt", structure_text, height=300)

# Add a button to save the changes
if st.button("Save Changes"):
    with open(file_path, 'w') as prompt_file:
        prompt_file.write(edited_text)
    st.success("Changes saved successfully!")
