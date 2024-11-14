import os
import boto3
from botocore.exceptions import NoCredentialsError, ClientError


def download_folder_from_s3(bucket_name, s3_folder, local_dir):
    """
    Download all the objects from S3 bucket to a local folder

    Parameters:
    bucket_name (str): The name of the S3 bucket.
    s3_folder (str): The path of the folder in the S3 bucket.
    local_dir: The local folder path.

    Returns:
    None
    """

    # Create an S3 client
    s3 = boto3.client("s3")

    # List objects within the specified S3 folder
    try:
        paginator = s3.get_paginator("list_objects_v2")
        for page in paginator.paginate(Bucket=bucket_name, Prefix=s3_folder):
            for obj in page.get("Contents", []):
                # Get the S3 file path
                s3_file_path = obj["Key"]

                if os.path.relpath(s3_file_path, s3_folder) == ".":
                    continue

                # Generate the local file path
                local_file_path = os.path.join(
                    local_dir, os.path.relpath(s3_file_path, s3_folder)
                )
                local_file_dir = os.path.dirname(local_file_path)

                # Create local directory if it doesn't exist
                if not os.path.exists(local_file_dir):
                    os.makedirs(local_file_dir)

                # Download the file
                try:
                    s3.download_file(bucket_name, s3_file_path, local_file_path)
                    print(f"Downloaded {s3_file_path} to {local_file_path}")
                except ClientError as e:
                    print(f"Failed to download {s3_file_path}: {e}")
    except NoCredentialsError:
        print("Credentials not available")
    except ClientError as e:
        print(f"Failed to list objects in {s3_folder}: {e}")


download_folder_from_s3(
    "aurawave-users-portraits", "Joshua-1731319691495", "./datasets/ohwx"
)
