import streamlit as st
import rarfile
import zipfile
import os
import tempfile

# Function to extract RAR file
def extract_rar(rar_path, output_path):
    with rarfile.RarFile(rar_path) as rf:
        rf.extractall(output_path)
    return output_path

# Function to extract ZIP file
def extract_zip(zip_path, output_path):
    with zipfile.ZipFile(zip_path, 'r') as zf:
        zf.extractall(output_path)
    return output_path

# Streamlit UI
st.title('File Decompressor')

# File uploader allows user to add any type of file
uploaded_file = st.file_uploader("Choose a RAR or ZIP file...")

if uploaded_file is not None:
    # Save uploaded file to a temporary directory
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        file_path = tmp_file.name

    # Specify output directory (you can modify this)
    output_dir = tempfile.mkdtemp()
    
    # Determine file type and extract accordingly
    try:
        if uploaded_file.name.lower().endswith('.rar'):
            extract_rar(file_path, output_dir)
            st.success('RAR file extracted successfully!')
        elif uploaded_file.name.lower().endswith('.zip'):
            extract_zip(file_path, output_dir)
            st.success('ZIP file extracted successfully!')
        else:
            st.error('Unsupported file format. Please upload a RAR or ZIP file.')
        
        if os.path.exists(output_dir):
            # Optionally, list extracted files
            extracted_files = os.listdir(output_dir)
            st.write('Extracted Files:')
            for file_name in extracted_files:
                st.write(file_name)
                
    except Exception as e:
        st.error(f'An error occurred: {e}')

else:
    st.write("No file uploaded yet.")
