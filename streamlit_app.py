import streamlit as st
import rarfile
import tempfile
import os

def decompress_rar(rar_file_path, destination_path):
    try:
        with rarfile.RarFile(rar_file_path) as rf:
            rf.extractall(destination_path)
        return True
    except Exception as e:
        st.error(f"Error occurred: {e}")
        return False

def main():
    st.title("RAR File Decompressor")

    # Upload RAR file
    uploaded_file = st.file_uploader("Upload RAR file", type=["rar"])

    if uploaded_file:
        # Create a temporary directory
        temp_dir = tempfile.mkdtemp()
        temp_rar_file = os.path.join(temp_dir, "uploaded_file.rar")
        with open(temp_rar_file, "wb") as f:
            f.write(uploaded_file.read())
        
        # Decompress the uploaded file
        if decompress_rar(temp_rar_file, temp_dir):
            st.success("File decompressed successfully!")
            decompressed_files = os.listdir(temp_dir)
            for file in decompressed_files:
                st.markdown(f"[{file}]({os.path.join(temp_dir, file)})")

if __name__ == "__main__":
    main()
