# import zipfile
# import os

# # Define the path to the zip file and the extraction folder
# zip_file_path = 'PrintJobData_20241102.zip'  # Update this if the zip file is in another directory
# extraction_folder = 'receipts'  # Folder where .stm files will be extracted

# # Ensure the extraction folder exists
# os.makedirs(extraction_folder, exist_ok=True)

# # Open the zip file and extract only .stm files
# with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
#     # Loop through all the files in the zip archive
#     for file in zip_ref.namelist():
#         # Check if the file is an .stm file
#         if file.endswith('.stm'):
#             # Extract the .stm file to the specified extraction folder
#             zip_ref.extract(file, extraction_folder)

# print("Extraction complete. .stm files are now in the 'receipts' folder.")


import zipfile
import boto3
import os

# Define the path to your zip file and S3 bucket details
zip_file_path = 'PrintJobData_20241102.zip'
s3_bucket_name = 'pos-receipts-stm-files'
s3_folder = 'stm_files'  # Optional folder inside the S3 bucket to store the .stm files

# Initialize the S3 client
s3_client = boto3.client('s3')

# Temporary directory to extract files
temp_dir = 'extracted_stm_files'

# Create the temp directory if it doesn't exist
os.makedirs(temp_dir, exist_ok=True)

# Extract .stm files from the zip archive
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    for file_info in zip_ref.infolist():
        if file_info.filename.endswith('.stm'):
            # Extract the file to the temp directory
            zip_ref.extract(file_info, temp_dir)
            file_path = os.path.join(temp_dir, file_info.filename)
            
            # Define the S3 key (path in S3 bucket)
            s3_key = f"{s3_folder}/{file_info.filename}" if s3_folder else file_info.filename
            
            # Upload the .stm file to S3
            s3_client.upload_file(file_path, s3_bucket_name, s3_key)
            print(f"Uploaded {file_info.filename} to s3://{s3_bucket_name}/{s3_key}")

# Cleanup: Remove the temp directory and extracted files
for file_name in os.listdir(temp_dir):
    os.remove(os.path.join(temp_dir, file_name))
os.rmdir(temp_dir)

print("All .stm files have been uploaded to S3.")
