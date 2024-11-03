# import os
# import shutil

# source_directory = 'receipts/SMA Hackathon'
# destination_directory = 'clustered_receipts'

# # Clear the destination directory if it already exists
# if os.path.exists(destination_directory):
#     shutil.rmtree(destination_directory)
# os.makedirs(destination_directory, exist_ok=True)

# # Counter for subfolders created
# subfolder_count = 0

# # Loop through all files in the source directory
# for filename in os.listdir(source_directory):
#     if filename.endswith(".stm"):
#         # Extract the last 4 digits (cafe ID) from the filename
#         cafe_id = filename[-8:-4]
        
#         # Extract the date (YYYYMMDD) from the filename
#         date = filename.split('_')[0].split('-')[2]  # Get YYYYMMDD part

#         # Create a subdirectory for the cafe ID if it doesn't already exist
#         cafe_folder = os.path.join(destination_directory, cafe_id)
#         if not os.path.exists(cafe_folder):
#             os.makedirs(cafe_folder)
#             subfolder_count += 1
        
#         # Create a subdirectory for the date within the cafe folder
#         date_folder = os.path.join(cafe_folder, date)
#         os.makedirs(date_folder, exist_ok=True)
        
#         # Move the .stm file to the corresponding date folder within the cafe folder
#         src_file = os.path.join(source_directory, filename)
#         dst_file = os.path.join(date_folder, filename)
#         shutil.move(src_file, dst_file)

# # Display the count of cafe subfolders created
# print(f"Number of cafe subfolders created: {subfolder_count}")
# print("Files have been organized by cafe ID and date!")


import os
import boto3

# Set up AWS S3
s3_bucket_name = 'pos-receipts-stm-files'
source_folder = 'stm_files'             # Source folder containing the unorganized .stm files
destination_folder = 'clustered_receipts' # Destination folder in S3 for organized files

# Initialize the S3 client
s3_client = boto3.client('s3')

# Pagination control
continuation_token = None

while True:
    # List objects with pagination in the source folder
    if continuation_token:
        objects = s3_client.list_objects_v2(
            Bucket=s3_bucket_name,
            Prefix=source_folder,
            ContinuationToken=continuation_token
        )
    else:
        objects = s3_client.list_objects_v2(
            Bucket=s3_bucket_name,
            Prefix=source_folder
        )
    
    # Check if objects were found in the specified S3 folder
    if 'Contents' in objects:
        for obj in objects['Contents']:
            s3_key = obj['Key']
            
            # Process only .stm files
            if s3_key.endswith(".stm"):
                filename = os.path.basename(s3_key)
                
                # Extract the last 4 digits (cafe ID) from the filename
                cafe_id = filename[-8:-4]
                
                # Extract the date (YYYYMMDD) from the filename
                try:
                    date = filename.split('_')[0].split('-')[2]  # Adjust this if needed
                except IndexError:
                    print(f"Date extraction failed for {filename}. Skipping.")
                    continue

                # Define the S3 destination path in the organized structure
                organized_s3_key = f"{destination_folder}/{cafe_id}/{date}/{filename}"
                
                # Check if the file already exists in the destination folder
                try:
                    s3_client.head_object(Bucket=s3_bucket_name, Key=organized_s3_key)
                    print(f"File {organized_s3_key} already exists in destination. Skipping.")
                    continue  # Skip if the file exists
                except s3_client.exceptions.ClientError as e:
                    # If the file does not exist, proceed with download and upload
                    if e.response['Error']['Code'] != '404':
                        print(f"Error checking existence of {organized_s3_key}: {e}")
                        continue

                # Download the file temporarily to the local system
                local_path = filename
                try:
                    s3_client.download_file(s3_bucket_name, s3_key, local_path)
                    # Upload the file to the new organized S3 location
                    s3_client.upload_file(local_path, s3_bucket_name, organized_s3_key)
                    print(f"Uploaded {filename} to s3://{s3_bucket_name}/{organized_s3_key}")
                except Exception as e:
                    print(f"Error processing {filename}: {e}")
                finally:
                    # Clean up the local file if it exists
                    if os.path.exists(local_path):
                        os.remove(local_path)

        # Check if there are more pages of results
        if objects.get('IsTruncated'):
            continuation_token = objects['NextContinuationToken']
        else:
            break
    else:
        print("No .stm files found in the specified S3 bucket and folder.")
        break

print("All .stm files have been organized by cafe ID and date in S3.")
