import streamlit as st
import os
from pyunpack import Archive

def decompress_rar(rar_file_path, output_dir):
    try:
        Archive(rar_file_path).extractall(output_dir)
        return True
    except Exception as e:
        st.error(f"Error: {e}")
        return False

def main():
    st.title("RAR File Decompressor")

    # File upload section
    st.subheader("Upload RAR File")
    rar_file = st.file_uploader("Upload a RAR file", type=["rar"])

    if rar_file is not None:
        # Specify output directory
        output_dir = st.text_input("Output Directory", value="output")

        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Decompress on button click
        if st.button("Decompress"):
            st.info("Decompressing... This may take a while for large files.")
            decompress_rar(rar_file, output_dir)
            st.success("Decompression successful!")

if __name__ == "__main__":
    main()
