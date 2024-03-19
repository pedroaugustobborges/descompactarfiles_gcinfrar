import streamlit as st
from pyunpack import Archive
import os
import shutil

def decompress_rar(uploaded_file):
    # Save the uploaded file to a temporary directory
    temp_dir = "temp"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    file_path = os.path.join(temp_dir, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Decompress the file
    output_dir = os.path.join("decompressed", uploaded_file.name.split('.')[0])
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    Archive(file_path).extractall(output_dir)
    
    # Clean up the temporary file
    os.remove(file_path)
    return output_dir

st.title('RAR File Decompressor')

uploaded_file = st.file_uploader("Choose a RAR file", type="rar")
if uploaded_file is not None:
    output_dir = decompress_rar(uploaded_file)
    st.success(f"File decompressed. Extracted files are in: {output_dir}")

    # Optionally, list the files that were extracted
    extracted_files = os.listdir(output_dir)
    st.write("Extracted Files:")
    for file in extracted_files:
        st.write(file)
