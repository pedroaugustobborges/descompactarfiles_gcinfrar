import streamlit as st
from pyunpack import Archive
import tempfile
import os

def decompress_rar(rar_file, destination_path):
    try:
        Archive(rar_file).extractall(destination_path)
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
        with tempfile.TemporaryDirectory() as temp_dir:
            if decompress_rar(uploaded_file, temp_dir):
                st.success("File decompressed successfully!")
                decompressed_files = os.listdir(temp_dir)
                for file in decompressed_files:
                    st.markdown(f"[{file}]({os.path.join(temp_dir, file)})")

if __name__ == "__main__":
    main()
