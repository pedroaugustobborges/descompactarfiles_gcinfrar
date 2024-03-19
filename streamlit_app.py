import streamlit as st
import rarfile
import zipfile
import os
import shutil
from io import BytesIO

# This function checks and installs unrar if not present (For local runs, in Streamlit Cloud you need to ensure unrar is available)
def check_and_install_unrar():
    if shutil.which("unrar") is None:
        import subprocess
        subprocess.run(["apt-get", "install", "unrar"], check=True)

# Check and install unrar at the beginning
check_and_install_unrar()

# Function to extract files
def extract_file(file_path, extract_to_dir):
    if file_path.endswith('.rar'):
        with rarfile.RarFile(file_path) as opened_rar:
            opened_rar.extractall(extract_to_dir)
            st.success(f'{file_path} extracted.')
    elif file_path.endswith('.zip'):
        with zipfile.ZipFile(file_path, 'r') as opened_zip:
            opened_zip.extractall(extract_to_dir)
            st.success(f'{file_path} extracted.')

# Streamlit UI
st.title('File Decompressor')

uploaded_files = st.file_uploader("Choose a RAR or ZIP file", accept_multiple_files=True, type=['rar', 'zip'])

extract_to_dir = 'extracted_files/'

if not os.path.exists(extract_to_dir):
    os.makedirs(extract_to_dir)

if st.button('Extract Files'):
    for uploaded_file in uploaded_files:
        # Save uploaded file to disk
        with open(os.path.join(extract_to_dir, uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())
        # Extract files
        extract_file(os.path.join(extract_to_dir, uploaded_file.name), extract_to_dir)

# List extracted files to download
extracted_files = os.listdir(extract_to_dir)
if extracted_files:
    st.write('Extracted Files:')
    for file_name in extracted_files:
        full_path = os.path.join(extract_to_dir, file_name)
        if os.path.isfile(full_path):  # Ensure it's a file before offering it for download
            with open(full_path, "rb") as f:
                st.download_button(label=f"Download {file_name}", data=f, file_name=file_name, mime="application/octet-stream")
        else:
            # Optionally notify about directories, or you can choose not to display them at all
            st.write(f"{file_name} is a directory and cannot be downloaded directly.")
