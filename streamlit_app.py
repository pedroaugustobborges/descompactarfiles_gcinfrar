import streamlit as st
import patoolib
import os

def decompress_rar(rar_file_path, extract_path):
    try:
        patoolib.extract_archive(rar_file_path, outdir=extract_path)
        return True
    except Exception as e:
        st.error(f"Error: {e}")
        return False

def main():
    st.title("RAR File Decompressor")
    st.write("This app allows you to decompress RAR files and download the extracted files one by one.")

    rar_file = st.file_uploader("Upload a RAR file", type=["rar"])
    if rar_file is not None:
        extract_path = st.text_input("Extraction Path", value="extracted_files")
        if st.button("Decompress"):
            if not os.path.exists(extract_path):
                os.makedirs(extract_path)
            if decompress_rar(rar_file, extract_path):
                st.success("Extraction completed successfully.")
                files = os.listdir(extract_path)
                selected_file = st.selectbox("Select a file to download:", files)
                if st.button("Download Selected File"):
                    file_path = os.path.join(extract_path, selected_file)
                    with open(file_path, "rb") as f:
                        st.download_button(label="Download", data=f, file_name=selected_file)
            else:
                st.error("Extraction failed.")

if __name__ == "__main__":
    main()
