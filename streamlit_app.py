import streamlit as st
from pyunpack import Archive
import os

def decompress_rar(rar_file_path, destination_path):
    try:
        Archive(rar_file_path).extractall(destination_path)
        return True
    except Exception as e:
        st.error(f"Error occurred: {e}")
        return False

def main():
    st.title("RAR File Decompressor")
    
    # Upload RAR file
    st.sidebar.header("Upload RAR file")
    uploaded_file = st.sidebar.file_uploader("Choose a RAR file", type=["rar"])

    if uploaded_file:
        # Decompress and display files
        st.sidebar.header("Decompressed Files")
        destination_path = st.sidebar.text_input("Enter destination folder path", "output")
        if st.sidebar.button("Decompress"):
            if decompress_rar(uploaded_file, destination_path):
                st.success("File decompressed successfully!")
                decompressed_files = os.listdir(destination_path)
                for file in decompressed_files:
                    st.sidebar.markdown(f"[{file}]({os.path.join(destination_path, file)})")
            else:
                st.error("Failed to decompress file!")

if __name__ == "__main__":
    main()
