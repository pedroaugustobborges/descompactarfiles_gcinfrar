import streamlit as st
import os
import shutil
from rarfile import RarFile

# Function to decompress RAR file
def decompress_rar(rar_file):
    with RarFile(rar_file) as rf:
        rf.extractall("tempDir")
    return st.success("Decompressed RAR file: {} to tempDir".format(rar_file.name))

# Function to save uploaded file
def save_uploadedfile(uploadedfile):
    with open(os.path.join("tempDir", uploadedfile.name), "wb") as f:
        f.write(uploadedfile.getbuffer())
    return st.success("Saved File: {} to tempDir".format(uploadedfile.name))

# Function to list and download files from tempDir
def download_file(file_path):
    with open(file_path, "rb") as file:
        file_contents = file.read()
    return file_contents

def main():
    st.title("RAR File Decompressor")

    # File upload section
    rar_file = st.file_uploader("Upload RAR File", type=['rar'])
    if rar_file is not None:
        file_details = {"FileName": rar_file.name, "FileType": rar_file.type}
        st.write(file_details)
        save_uploadedfile(rar_file)

    # Decompress RAR file section
    if st.button("Decompress RAR File"):
        if os.path.exists("tempDir"):
            shutil.rmtree("tempDir")
        os.makedirs("tempDir", exist_ok=True)
        decompress_rar(rar_file)

    # Display and download individual files
    if os.path.exists("tempDir"):
        st.markdown("### Download Individual Files:")
        files_list = os.listdir("tempDir")
        for file in files_list:
            file_path = os.path.join("tempDir", file)
            if os.path.isfile(file_path):
                if st.button(file):
                    file_contents = download_file(file_path)
                    st.download_button(label="Download " + file, data=file_contents, file_name=file)

if __name__ == "__main__":
    main()
