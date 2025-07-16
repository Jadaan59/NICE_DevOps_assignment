import boto3
import os
import sys

# This script uploads all files from the sample_files/ directory to the specified S3 bucket.
# You must have AWS credentials configured (via aws configure or environment variables).

def main():
    if len(sys.argv) > 1:
        bucket_name = sys.argv[1]
    else:
        bucket_name = input("Enter the S3 bucket name: ")

    folder = 'sample_files'
    s3 = boto3.client('s3')

    if not os.path.isdir(folder):
        print(f"Folder '{folder}' does not exist.")
        return

    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    if not files:
        print(f"No files found in '{folder}'.")
        return

    for filename in files:
        file_path = os.path.join(folder, filename)
        print(f"Uploading {filename} to bucket {bucket_name}...")
        try:
            s3.upload_file(file_path, bucket_name, filename)
            print(f"Uploaded: {filename}")
        except Exception as e:
            print(f"Failed to upload {filename}: {e}")

if __name__ == "__main__":
    main() 