import boto3
import os
import sys

def main():
    """
    Script to upload all files from the sample_files/ directory to an S3 bucket.
    
    Usage:
        python upload_sample_files.py <bucket_name>
        python upload_sample_files.py  # Will prompt for bucket name
    """
    if len(sys.argv) > 1:
        bucket_name = sys.argv[1]
    else:
        bucket_name = input("Enter the S3 bucket name: ")

    if not bucket_name.strip():
        print("Error: Bucket name cannot be empty")
        sys.exit(1)

    folder = 'sample_files'
    s3 = boto3.client('s3')

    # Check if sample_files directory exists
    if not os.path.isdir(folder):
        print(f" Error: Folder '{folder}' does not exist.")
        print("Please create the 'sample_files' directory and add some files to upload.")
        return

    # Get list of files to upload
    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    if not files:
        print(f"No files found in '{folder}' directory.")
        print("Please add some files to the 'sample_files' directory before running this script.")
        return

    print(f"Found {len(files)} files to upload to bucket: {bucket_name}")
    print("=" * 50)

    successful_uploads = 0
    failed_uploads = 0

    for filename in files:
        file_path = os.path.join(folder, filename)
        print(f"Uploading {filename}...")
        
        try:
            s3.upload_file(file_path, bucket_name, filename)
            print(f"Successfully uploaded: {filename}")
            successful_uploads += 1
        except Exception as e:
            print(f"Failed to upload {filename}: {e}")
            failed_uploads += 1

    print("=" * 50)
    print(f"Upload Summary:")
    print(f"Successful: {successful_uploads}")
    print(f"Failed: {failed_uploads}")
    print(f"Total files: {len(files)}")

    if successful_uploads > 0:
        print(f"\n Successfully uploaded {successful_uploads} files to S3 bucket: {bucket_name}")
    else:
        print("\n No files were uploaded successfully.")

if __name__ == "__main__":
    main() 