import streamlit as st
import rarfile
import os
import tempfile

# Function to extract RAR file
def extract_rar(rar_path, output_path):
    with rarfile.RarFile(rar_path) as rf:
        rf.extractall(output_path)
    return output_path

# Streamlit UI
st.title('RAR File Decompressor')

# File uploader allows user to add any type of file
uploaded_file = st.file_uploader("Choose a file...")

if uploaded_file is not None:
    # Save uploaded file to a temporary directory
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        rar_path = tmp_file.name

    # Specify output directory (you can modify this)
    output_dir = tempfile.mkdtemp()
    
    # Extract the RAR file
    try:
        extract_rar(rar_path, output_dir)
        st.success('Files extracted successfully!')
        st.write(f'Extracted files are in: {output_dir}')
        
        # Optionally, list extracted files
        extracted_files = os.listdir(output_dir)
        st.write('Extracted Files:')
        for file_name in extracted_files:
            st.write(file_name)
            
    except Exception as e:
        st.error(f'An error occurred: {e}')

else:
    st.write("No file uploaded yet.")



