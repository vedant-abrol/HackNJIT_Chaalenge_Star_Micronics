

---

# HackNJIT Challenge - POS Receipt Data Analysis

## Project Overview

This project, developed for the HackNJIT 2024 Challenge, is focused on analyzing POS (Point of Sale) receipt data in `.stm` format from various cafes. The goal was to store, organize, and process unstructured receipt data in an AWS infrastructure and extract valuable insights to be visualized through PowerBI. The project utilizes AWS services like S3 and Athena for data storage and querying, with Terraform used for cloud infrastructure setup. PowerBI provides the data visualization interface, allowing stakeholders to view trends and analytics over the receipt data.

## Inspiration

The inspiration behind this project was the need to transform unstructured and varied-format POS receipt data into a structured, queryable dataset for analysis and visualization. By leveraging cloud services, we aimed to make it scalable and efficient to analyze and visualize data from thousands of receipt files. Additionally, this project showcases how to build a robust pipeline to handle unstructured data formats, which is a common challenge in the retail and F&B industries.

## What We Learned

Through this project, we learned:
- How to set up cloud infrastructure using Terraform to automate resource provisioning.
- Parsing and organizing unstructured data formats in `.stm` files using Python.
- Leveraging AWS S3 for scalable storage and AWS Athena for querying structured data.
- Creating interactive dashboards in PowerBI to visualize the analyzed data.
- Troubleshooting and optimizing AWS Lambda functions to handle event-based data processing.

## Project Workflow

1. **Data Ingestion**:
   - The unstructured `.stm` receipt files from various cafes were uploaded to an S3 bucket (`pos-receipts-stm-files`).
   - S3 bucket structure: 
     - Each `.stm` file was organized by cafe ID and date within the bucket for easy access and querying.
   
2. **Data Processing**:
   - **Lambda Function**: AWS Lambda was set up to trigger each time a new `.stm` file was uploaded. It would parse the receipt data, extract relevant fields like order number, date, time, item names, prices, and VAT details, and save it as a structured CSV file.
   - **Python Scripts**: Custom scripts were created to parse the `.stm` format, extract necessary details, and structure the data in CSV files, one for each date within each cafe ID.

3. **Data Storage & Querying**:
   - Processed CSV files were stored back into the S3 bucket, with Athena configured to query the structured CSV data.
   - Using Athena, SQL-like queries could be executed to analyze data by date, cafe, item sales, and VAT collection.

4. **Data Visualization**:
   - **PowerBI Dashboard**: The structured data queried from Athena was visualized in PowerBI. Dashboards were created to present daily sales, top items sold, VAT summaries, and revenue per cafe.
   - **Embedded Dashboard**: A PowerBI embedded dashboard was implemented in a React app for easy access to the visualizations.

5. **Infrastructure as Code (IaC)**:
   - The entire AWS setup, including the S3 bucket and Athena database, was provisioned using Terraform, making it easy to replicate the infrastructure.

## Challenges Faced

- **Handling Unstructured Data**: The `.stm` files had varied formatting across cafes, making parsing challenging. Custom regular expressions were implemented to accurately extract details.
- **File Size and GitHub Limitations**: Managing large `.terraform` files and AWS provider packages exceeded GitHub’s file size limit, requiring advanced git management techniques.
- **Permissions**: Ensuring Lambda had the correct IAM policies to access the S3 bucket and write parsed data files.

## How We Built It

1. **Parsing & Organizing Data**: We wrote Python scripts to parse `.stm` files and organize them by cafe ID and date, using AWS Lambda for serverless processing.
2. **AWS S3 for Storage**: S3 buckets were structured to store both raw `.stm` files and processed CSV files, organized by cafe and date.
3. **AWS Athena for Querying**: Once CSV files were stored, Athena was used to run queries on the data without needing a traditional database.
4. **Terraform for IaC**: The AWS infrastructure was set up and managed using Terraform for reproducibility and efficient resource management.
5. **PowerBI for Visualization**: PowerBI dashboards were created to visualize insights such as sales trends, daily totals, and top items, enabling quick decision-making.

## Folder Structure

```
/project-root
├── clustered_receipts/            # Organized .stm files by cafe ID and date
├── organized_receipts_by_date/    # Organized receipts by date for each cafe
├── public/                        # React app’s public assets
├── receipts/                      # Raw receipt files
├── src/                           # Source code for React app with PowerBI embedded dashboard
├── .gitignore                     # Ignoring .terraform files and large files
├── main.tf                        # Terraform configuration file for AWS setup
├── cleanup.py                     # Script to clean S3 bucket for new data ingestion
├── cluster.py                     # Script to organize raw receipts by cafe and date
├── README.md                      # Detailed project documentation
└── other configuration files
```

## Built With

- **Languages**: Python, JavaScript (React)
- **Cloud Services**: AWS S3, AWS Lambda, AWS Athena
- **IaC**: Terraform
- **Data Visualization**: PowerBI
- **Version Control**: Git & GitHub

## Getting Started

### Prerequisites

- AWS account with access to S3, Lambda, and Athena.
- Terraform installed locally to set up cloud infrastructure.
- PowerBI account to create dashboards.
- Node.js and npm to run the React app for the embedded PowerBI dashboard.

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/vedant-abrol/HackNJIT_Challenge_Star_Micronics.git
   cd HackNJIT_Challenge_Star_Micronics
   ```

2. **Set up AWS Infrastructure with Terraform**:
   ```bash
   terraform init
   terraform apply
   ```

3. **Set up the Lambda Function**:
   - Deploy the Lambda function to process `.stm` files in the S3 bucket.
   - Configure IAM policies to give the Lambda function access to S3 and Athena.

4. **Run the React App**:
   ```bash
   cd src
   npm install
   npm start
   ```

   The PowerBI dashboard will be accessible at `http://localhost:3000`.

### Usage

1. **Upload .stm Files**: Upload `.stm` files to the S3 bucket under the `receipts/` folder.
2. **Processing & Structuring Data**: Lambda automatically processes the uploaded files, extracts information, and saves it as CSV files in the `processed_receipts` folder in S3.
3. **Analyze with Athena**: Run queries on the structured data in Athena for insights.
4. **Visualize in PowerBI**: Use PowerBI for dashboards, accessible through the embedded React app.

## Future Improvements

- **Automated Data Insights**: Implement AWS Glue for ETL processes to automate data preparation for Athena.
- **Enhanced Visualizations**: Integrate additional metrics and real-time data updates in PowerBI.
- **Error Handling**: Improve Lambda error handling for varied `.stm` formats.

## License

Distributed under License.

---
