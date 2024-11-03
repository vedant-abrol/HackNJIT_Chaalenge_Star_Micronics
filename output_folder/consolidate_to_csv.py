import os
import csv
import re

def parse_txt_file(file_path, company_name):
    """
    Parses a single text file to extract order data with Star Document Markup specifications.
    Returns a dictionary with the order details and includes company information.
    """
    order_data = {'company': company_name}
    items = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            # Extract key details ignoring Star Document Markup tags
            if line.startswith("Order ID:"):
                order_data['order_id'] = line.split(": ")[1]
            elif line.startswith("Total Price:"):
                order_data['total_price'] = line.split(": ")[1]
            elif line.startswith("VAT Amount:"):
                order_data['vat_amount'] = line.split(": ")[1]
            elif line.startswith("-"):
                # Parse item details, ignoring Star Document Markup tags like [align] or [magnify]
                parts = re.sub(r"\[.*?\]", "", line).split(" x ")
                quantity = parts[0].strip(" -")
                item_name = parts[1].split(" @ ")[0]
                price_vat = parts[1].split(" @ ")[1].split(", VAT: ")
                price = price_vat[0].strip(" EUR")
                vat = price_vat[1].split("% (")
                vat_rate = vat[0]
                vat_value = vat[1].strip(" EUR)")
                items.append({
                    'quantity': quantity,
                    'item_name': item_name,
                    'price': price,
                    'vat_rate': vat_rate,
                    'vat_value': vat_value
                })
    order_data['items'] = items
    return order_data

def consolidate_txt_files_to_csv(output_folder, csv_file_path, company_name):
    """
    Consolidates all .txt files in the output_folder into a single CSV file,
    including a column for company name.
    """
    with open(csv_file_path, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        # Write header with a Company column
        writer.writerow(['Company', 'Order ID', 'Total Price', 'VAT Amount', 'Item Quantity', 'Item Name', 'Item Price', 'Item VAT Rate', 'Item VAT Value'])
        
        # Process each .txt file in the output folder
        for filename in os.listdir(output_folder):
            if filename.endswith(".txt"):
                file_path = os.path.join(output_folder, filename)
                order_data = parse_txt_file(file_path, company_name)
                
                # Write each item in the order as a row in the CSV
                for item in order_data['items']:
                    writer.writerow([
                        order_data['company'],
                        order_data['order_id'],
                        order_data['total_price'],
                        order_data['vat_amount'],
                        item['quantity'],
                        item['item_name'],
                        item['price'],
                        item['vat_rate'],
                        item['vat_value']
                    ])

# Set paths and company name
output_folder = '/Users/vedantabrol/Downloads/SMA Hackathon 2024-11-3/SMA Hackathon/output_folder'
csv_file_path = '/Users/vedantabrol/Downloads/SMA Hackathon 2024-11-3/SMA Hackathon/consolidated_orders_with_company.csv'
company_name = "CompanyName"  # Replace with actual company name if it's extractable from files

# Run the consolidation function
consolidate_txt_files_to_csv(output_folder, csv_file_path, company_name)
print(f"Consolidated data with company info saved to {csv_file_path}")
