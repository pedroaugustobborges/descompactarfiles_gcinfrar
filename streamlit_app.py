import streamlit as st
import rarfile

def decompress_rar(uploaded_file, output_dir="output"):
  """Decompresses the uploaded RAR file and saves the extracted files to the specified directory.

  Args:
      uploaded_file (streamlit.uploadedfile.UploadedFile): The uploaded RAR file.
      output_dir (str, optional): The directory to save the extracted files. Defaults to "output".
  """
  with rarfile.open(uploaded_file) as rar:
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
  extracted_files = [os.path.join("output", f) for f in os.listdir("output")]

  if extracted_files:
    st.subheader("Extracted Files")
    for file_path in extracted_files:
      st.write(file_path)
      download_file(file_path)
  else:
    st.warning("No files were extracted from the RAR.")

