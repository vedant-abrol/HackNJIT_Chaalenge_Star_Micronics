import zipfile
import os

# Define the path to the zip file and the extraction folder
zip_file_path = 'PrintJobData_20241102.zip'  # Update this if the zip file is in another directory
extraction_folder = 'receipts'  # Folder where .stm files will be extracted

# Ensure the extraction folder exists
os.makedirs(extraction_folder, exist_ok=True)

# Open the zip file and extract only .stm files
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    # Loop through all the files in the zip archive
    for file in zip_ref.namelist():
        # Check if the file is an .stm file
        if file.endswith('.stm'):
            # Extract the .stm file to the specified extraction folder
            zip_ref.extract(file, extraction_folder)

print("Extraction complete. .stm files are now in the 'receipts' folder.")
