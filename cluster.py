import os
import shutil

source_directory = 'receipts'
destination_directory = 'clustered_receipts'

# Ensure the destination directory exists
os.makedirs(destination_directory, exist_ok=True)

# Loop through all files in the source directory
for filename in os.listdir(source_directory):
    if filename.endswith(".stm"):
        # Extract the last 4 digits (cafe ID) from the filename
        cafe_id = filename[-8:-4]
        
        # Create a subdirectory for the cafe ID if it doesn't already exist
        cafe_folder = os.path.join(destination_directory, cafe_id)
        os.makedirs(cafe_folder, exist_ok=True)
        
        # Move the .stm file to the corresponding cafe folder
        src_file = os.path.join(source_directory, filename)
        dst_file = os.path.join(cafe_folder, filename)
        shutil.move(src_file, dst_file)

print("Files have been organized by cafe ID!")
