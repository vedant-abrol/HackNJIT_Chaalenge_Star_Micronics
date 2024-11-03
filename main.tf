# main.tf

provider "aws" {
  region = "us-east-1"  # Set this to your preferred AWS region
}

# Create an S3 bucket for storing .stm files
resource "aws_s3_bucket" "stm_files_bucket" {
  bucket = "pos-receipts-stm-files"  # Choose a globally unique bucket name
  acl    = "private"                 # Private access by default

  # Optional: Enable versioning to keep track of file changes
  versioning {
    enabled = true
  }

  # Optional: Define lifecycle rules (e.g., delete files after a certain period)
  lifecycle_rule {
    enabled = true
    expiration {
      days = 365  # Files will expire after 1 year
    }
  }
}

# Output the bucket name
output "s3_bucket_name" {
  value = aws_s3_bucket.stm_files_bucket.bucket
}
