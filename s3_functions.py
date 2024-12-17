import os
from os import environ

import boto3

s3_endpoint_url = environ.get("S3_ENDPOINT") or environ.get("AWS_S3_ENDPOINT")
s3_access_key = environ.get("S3_ACCESS_KEY") or environ.get("AWS_ACCESS_KEY_ID")
s3_secret_key = environ.get("S3_SECRET_KEY") or environ.get("AWS_SECRET_ACCESS_KEY")
s3_bucket_name = environ.get("S3_BUCKET") or environ.get("AWS_S3_BUCKET")
s3_region = environ.get("AWS_DEFAULT_REGION", "None")


def upload_s3_file(local_path: str, s3_path: str):
    # Initialize S3 client
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=s3_access_key,
        aws_secret_access_key=s3_secret_key,
        endpoint_url=s3_endpoint_url,
        region_name="eu-central-1",
    )

    response = s3_client.upload_file(local_path, s3_bucket_name, s3_path)

    print(f'upload_log_to_aws response: {response}')

def download_s3_folder(s3_folder: str, local_dir: str):
    # Initialize S3 client
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=s3_access_key,
        aws_secret_access_key=s3_secret_key,
        endpoint_url=s3_endpoint_url,
        region_name="eu-central-1",
    )

    # Ensure the local directory exists
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)

    # List objects within the specified S3 folder
    paginator = s3_client.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=s3_bucket_name, Prefix=s3_folder):
        if "Contents" in page:
            for obj in page["Contents"]:
                # Extract the file path and file name
                s3_key = obj["Key"]
                local_file_path = os.path.join(
                    local_dir, os.path.relpath(s3_key, s3_folder)
                )

                # Create local directory structure if it doesn't exist
                local_file_dir = os.path.dirname(local_file_path)
                if not os.path.exists(local_file_dir):
                    os.makedirs(local_file_dir)

                # Download the file
                print(f"Downloading {s3_key} to {local_file_path}")
                s3_client.download_file(s3_bucket_name, s3_key, local_file_path)


if __name__ == "__main__":
    # Usage example
    s3_folder = "onnx-community/gliner_multi-v2.1"  # The folder path in S3
    local_dir = "models/"  # Local path to save the files

    download_s3_folder(s3_folder, local_dir)
