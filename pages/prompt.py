import os
import streamlit as st

# Set the path to the text file
file_path = os.path.join("prompt", "prompt.txt")

# Check if the file exists
if os.path.exists(file_path):
    # Read the content of the file
    with open(file_path, 'r') as prompt_file:
        prompt_text = prompt_file.read()
else:
    prompt_text = ""

file_path = os.path.join("prompt", "extraction_prompt.txt")

# Check if the file exists
if os.path.exists(file_path):
    # Read the content of the file
    with open(file_path, 'r') as prompt_file:
        extraction_prompt_text = prompt_file.read()
else:
    extraction_prompt_text = ""

# Display the text area for editing the content
st.title("Writing Prompt")
edited_text = st.text_area("Edit the content of prompt.txt", prompt_text, height=300)

# Add a button to save the changes
if st.button("Save prompt changes"):
    with open(file_path, 'w') as prompt_file:
        prompt_file.write(edited_text)
    st.success("Changes saved successfully!")

st.title("Extracting data prompt Prompt")
edited_text = st.text_area("Edit the content of extraction_prompt.txt", extraction_prompt_text, height=300)

# Add a button to save the changes
if st.button("Save extraction prompt "):
    with open(file_path, 'w') as prompt_file:
        prompt_file.write(edited_text)
    st.success("Changes saved successfully!")
