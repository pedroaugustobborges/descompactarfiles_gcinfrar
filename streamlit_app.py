import os
import rarfile

def decompress_rar(uploaded_file, output_dir="output"):
  """Decompresses the uploaded RAR file and saves the extracted files to the specified directory.

  Args:
      uploaded_file (streamlit.uploadedfile.UploadedFile): The uploaded RAR file.
      output_dir (str, optional): The directory to save the extracted files. Defaults to "output".
  """
  # Get the temporary file path
  file_path = os.path.join("temp", uploaded_file.name)

  # Write the uploaded file content to the temporary location
  with open(file_path, "wb") as f:
    f.write(uploaded_file.getbuffer())

  # Now use the temporary file path for decompression
  with rarfile.open(file_path) as rar:
    rar.extractall(output_dir)
  st.success(f"Decompressed {uploaded_file.name} to {output_dir}")
