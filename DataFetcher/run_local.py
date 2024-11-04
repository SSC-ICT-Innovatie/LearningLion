import os
import zipfile
from DataFetcher.libraries.classes.kamervragen import KamerVragen
from DataFetcher.libraries.data_classes.range_enum import Range

def run_local_datafetcher(range=Range.Tiny):
  ran = range
  kamervragen = KamerVragen(100)
  files = kamervragen.getAllTypes(downloadTypes=['Antwoord schriftelijke vragen'], range=ran)
  print(f"Downloaded {len(files)} files")
  print(f"Files: {files[:5]}")
  # Create the zip file directly without using a temporary directory
  zip_filename = "downloaded_files.zip"
  with zipfile.ZipFile(zip_filename, 'w') as zipf:
      for file_info in files:
          file_path = file_info["file"]  # Extract the path
          
          # Ensure the file exists before adding
          if os.path.isfile(file_path):
              print(f"Adding {file_path} to zip file")
              zipf.write(file_path, os.path.basename(file_path))  # Add file with its basename
          else:
              print(f"File not found and skipped: {file_path}")

  print(f"Files have been zipped successfully! Archive created at: {zip_filename}")