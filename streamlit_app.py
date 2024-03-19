import os
import streamlit as st
import patoolib
import shutil

# Function to save the uploaded file to a temporary directory
def save_uploadedfile(uploadedfile):
    with open(os.path.join("tempDir", uploadedfile.name), "wb") as f:
        f.write(uploadedfile.getbuffer())
    return st.success(f"Saved File: {uploadedfile.name} to tempDir")

# Function to decompress a RAR file
def decompress_rar(file_path, dest_path):
    try:
        patoolib.extract_archive(file_path, outdir=dest_path)
        st.success("File decompressed successfully")
    except Exception as e:
        st.error(f"Error decompressing file: {e}")

# Streamlit UI
st.title("RAR File Decompressor")
rar_file = st.file_uploader("Upload a RAR File", type=['rar'])

if rar_file is not None:
    # Save the uploaded RAR file
    if not os.path.exists('tempDir'):
        os.makedirs('tempDir')
    save_uploadedfile(rar_file)
    
    # Decompress the RAR file
    decompress_path = os.path.join('tempDir', 'decompressed')
    os.makedirs(decompress_path, exist_ok=True)
    decompress_rar(os.path.join('tempDir', rar_file.name), decompress_path)
    
    # List files and allow downloading
    decompressed_files = os.listdir(decompress_path)
    if decompressed_files:
        st.write("Decompressed Files:")
        for file in decompressed_files:
            st.write(file)
            with open(os.path.join(decompress_path, file), "rb") as f:
                st.download_button(label=f"Download {file}", data=f, file_name=file, mime='application/octet-stream')

# Cleanup tempDir after use (optional, consider when/how you want to clean up)
# shutil.rmtree('tempDir')
