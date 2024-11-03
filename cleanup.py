import os  # Import the os module

# Define the temporary directory used for extracting files
temp_dir = 'extracted_stm_files'  # Update this to the actual directory path if different

# Clean up: Remove files first, then directories
def cleanup_temp_directory(temp_dir):
    if not os.path.exists(temp_dir):
        print(f"The directory '{temp_dir}' does not exist.")
        return

    for root, dirs, files in os.walk(temp_dir, topdown=False):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            os.remove(file_path)
            print(f"Deleted file: {file_path}")
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            os.rmdir(dir_path)
            print(f"Deleted directory: {dir_path}")

    # Finally, remove the root temporary directory itself
    os.rmdir(temp_dir)
    print(f"Deleted root directory: {temp_dir}")

if __name__ == "__main__":
    cleanup_temp_directory(temp_dir)
    print("Temporary files and directories have been cleaned up.")
