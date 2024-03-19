import streamlit as st
import rarfile
import zipfile
import os
import shutil
from io import BytesIO


st.set_page_config(
    page_title='Descompactar Arquivos - GCINFRA',
    layout='wide',
    page_icon="https://media.licdn.com/dms/image/C4D0BAQHXylmAyGyD3A/company-logo_200_200/0/1630570245289?e=2147483647&v=beta&t=Dxas2us5gteu0P_9mdkQBwJEyg2aoc215Vrk2phu7Bs",
    initial_sidebar_state='auto'
)

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

# Function to clean extracted files directory
def clean_extracted_files_directory(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
            st.success(f'Limpou {filename}.')
        except Exception as e:
            st.error(f'Failed to delete {filename}. Reason: {e}')

# Function to compress directories before download
def compress_directory(path_to_dir, output_filename):
    shutil.make_archive(output_filename, 'zip', path_to_dir)
    return output_filename + '.zip'

# Streamlit UI
st.title('Descompactador de Arquivos 📦')

uploaded_files = st.file_uploader("Escolha um arquivo RAR ou ZIP", accept_multiple_files=True, type=['rar', 'zip'])

extract_to_dir = 'extracted_files/'

if not os.path.exists(extract_to_dir):
    os.makedirs(extract_to_dir)

if st.button('Extrair Arquivos'):
    for uploaded_file in uploaded_files:
        # Save uploaded file to disk
        with open(os.path.join(extract_to_dir, uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())
        # Extract files
        extract_file(os.path.join(extract_to_dir, uploaded_file.name), extract_to_dir)

# Add a button to clean the extracted files directory
if st.button('Limpar Cache'):
    clean_extracted_files_directory(extract_to_dir)

# List extracted files and directories to download
extracted_files = os.listdir(extract_to_dir)
if extracted_files:
    st.write('Extracted Files and Folders:')
    for file_name in extracted_files:
        full_path = os.path.join(extract_to_dir, file_name)
        if os.path.isfile(full_path):
            with open(full_path, "rb") as f:
                st.download_button(label=f"Download {file_name}", data=f, file_name=file_name, mime="application/octet-stream")
        elif os.path.isdir(full_path):
            zip_path = compress_directory(full_path, os.path.join("temp", file_name))
            with open(zip_path, "rb") as f:
                st.download_button(label=f"Download {file_name}.zip", data=f, file_name=os.path.basename(zip_path), mime="application/zip")
