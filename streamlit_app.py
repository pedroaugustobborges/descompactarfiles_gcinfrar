import streamlit as st
import rarfile
import os

def decompress_rar(uploaded_file, output_dir="output"):
  """Decompresses the uploaded RAR file and saves the extracted files to the specified directory.

  Args:
      uploaded_file (streamlit.uploadedfile.UploadedFile): The uploaded RAR file.
      output_dir (str, optional): The directory to save the extracted files. Defaults to "output".
  """
  # Create a temporary directory (if it doesn't exist)
  os.makedirs(output_dir, exist_ok=True)

  # Get the temporary file path
  file_path = os.path.join(output_dir, uploaded_file.name)

  # Write the uploaded file content to the temporary location
  with open(file_path, "wb") as f:
    f.write(uploaded_file.getbuffer())

  # Now use the temporary file path for decompression
  with rarfile.open(file_path) as rar:
    rar.extractall(output_dir)
  st.success(f"Decompressed {uploaded_file.name} to {output_dir}")

def download_file(file_path):
  """Creates a download link for a file at the specified path.

  Args:
      file_path (str): The path to the file to download.
  """
  with open(file_path, "rb") as f:
    data = f.read()
  st.download_button(label=os.path.basename(file_path), data=data, file_ext=os.path.splitext(file_path)[1])

st.title("RAR Decompression and Download App")
uploaded_file = st.file_uploader("Upload RAR File", type="rar")

if uploaded_file is not None:
  # Decompress the uploaded RAR file
  decompress_rar(uploaded_file)

  # Get a list of extracted files
  extracted_files = [os.path.join(output_dir, f) for f in os.listdir(output_dir) if not f.startswith(".")]  # Exclude hidden files

  if extracted_files:
    st.subheader("Extracted Files")
    for file_path in extracted_files:
      st.write(file_path)
      download_file(file_path)
  else:
    st.warning("No files were extracted from the RAR.")
