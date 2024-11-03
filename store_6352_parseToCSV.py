import re
import csv
import boto3
import os

# AWS S3 bucket and folder structure
s3_bucket_name = 'pos-receipts-stm-files'
s3_source_folder = 'clustered_receipts'  # Source folder in S3 for receipts
s3_destination_folder = 'processed_receipts'  # Destination folder in S3 for parsed CSVs

# Initialize S3 client
s3_client = boto3.client('s3')

# List all .stm files in the S3 bucket under the source folder
objects = s3_client.list_objects_v2(Bucket=s3_bucket_name, Prefix=s3_source_folder)

if 'Contents' in objects:
    for obj in objects['Contents']:
        s3_key = obj['Key']  # S3 object key (file path)

        # Process only .stm files and filter for cafe 6352
        if s3_key.endswith(".stm") and '/6352/' in s3_key:
            # Extract cafe_id, date, and filename from the folder structure in S3 key
            try:
                _, _, cafe_id, date, filename = s3_key.split('/')
            except ValueError:
                print(f"Unexpected file structure for {s3_key}. Skipping.")
                continue

            # Temporary download path for the .stm file
            local_path = '/tmp/' + filename
            s3_client.download_file(s3_bucket_name, s3_key, local_path)

            # Use the original `.stm` filename for the CSV file, replacing the extension
            csv_filename = filename.replace('.stm', '.csv')
            
            # Open or create the CSV file for appending data
            with open(csv_filename, mode='a', newline='') as csv_file:
                writer = csv.writer(csv_file)
                
                # If the file is new, write the header row
                if os.stat(csv_filename).st_size == 0:
                    writer.writerow(["cafe_id", "date", "time", "order_no", "item", "price", "vat", "total_amount"])
                
                # Read and parse the .stm file
                with open(local_path, 'r') as file:
                    content = file.read()
                    
                    # Extract order number
                    order_no_match = re.search(r"Order No: (\d+)", content)
                    order_no = order_no_match.group(1) if order_no_match else None
                    
                    # Extract time from content (since date is in folder name)
                    time_match = re.search(r"\d{2}:\d{2}:\d{2}", content)  # Format: HH:MM:SS
                    time = time_match.group(0) if time_match else None
                    
                    # Extract total amount
                    total_amount_match = re.search(r"Total amount: ([\d.]+) EUR", content)
                    total_amount = total_amount_match.group(1) if total_amount_match else None
                    
                    # Find items and prices
                    items = re.findall(r"(\d+ - .+?) // ([\d.]+ EUR) // VAT: ([\d.]+%)", content)
                    
                    for item in items:
                        # Each item in items is a tuple (quantity - item_name, price, vat)
                        item_name = item[0]
                        price = item[1]
                        vat = item[2]
                        
                        # Write row to the CSV file for the specific cafe_id and date
                        writer.writerow([cafe_id, date, time, order_no, item_name, price, vat, total_amount])

            # Define the destination path in S3, preserving the original filename
            s3_destination_key = f"{s3_destination_folder}/cafe_{cafe_id}/date_{date}/{csv_filename}"
            
            # Upload the CSV file to the structured path in S3
            s3_client.upload_file(csv_filename, s3_bucket_name, s3_destination_key)
            print(f"Uploaded {csv_filename} to s3://{s3_bucket_name}/{s3_destination_key}")

            # Remove the local .stm and CSV files after processing
            os.remove(local_path)
            os.remove(csv_filename)

else:
    print("No .stm files found in the specified S3 folder.")

print("Parsing complete. Separate CSV files created for each date of cafe 6352 and uploaded to S3.")
