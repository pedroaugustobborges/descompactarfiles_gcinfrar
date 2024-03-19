import streamlit as st
import patoolib
import os

def decompress_rar(rar_file_path, destination_path):
    try:
        patoolib.extract_archive(rar_file_path, outdir=destination_path, program="unrar")
        return True
    except Exception as e:
        st.error(f"Error occurred: {e}")
        return False

def main():
    st.title("RAR File Decompressor")

    # Upload RAR file
    uploaded_file = st.file_uploader("Upload RAR file", type=["rar"])

    if uploaded_file:
        # Decompress the uploaded file
        temp_dir = st.write(tempfile.mkdtemp())
        if decompress_rar(uploaded_file, temp_dir):
            st.success("File decompressed successfully!")
            decompressed_files = os.listdir(temp_dir)
            for file in decompressed_files:
                st.markdown(f"[{file}]({os.path.join(temp_dir, file)})")

if __name__ == "__main__":
    main()
