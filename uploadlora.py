import os
import boto3
from botocore.exceptions import NoCredentialsError, ClientError

LORA_FILENAME = "pytorch_lora_weights.safetensors"


def upload_file_to_s3(file_name, bucket, object_name=None):
    """
    Upload a file from a local file path to a S3 bucket.

    Parameters:
    file_name (str): The local file path to save the downloaded file.
    bucket (str): The name of the S3 bucket.
    object_name (str): The key/path of the file in the S3 bucket.

    Returns:
    None
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Create an S3 client
    s3 = boto3.client("s3")

    try:
        # Upload the file
        s3.upload_file(file_name, bucket, object_name)
        print(f"File {file_name} uploaded to {bucket}/{object_name}")
    except FileNotFoundError:
        print(f"The file {file_name} was not found")
    except NoCredentialsError:
        print("Credentials not available")
    except Exception as e:
        print(f"An error occurred: {e}")


def file_exists(folder, filename):
    # Construct the full path to the file
    full_path = os.path.join(folder, filename)
    return os.path.exists(full_path)


s3_bucket = ""
s3_dataset_folder = ""

if file_exists("./output/models", LORA_FILENAME):
    upload_file_to_s3(
        "./output/models/" + LORA_FILENAME,
        s3_bucket,
        s3_dataset_folder + LORA_FILENAME,
    )
    print(
        {
            "output": {
                "s3_bucket": s3_bucket,
                "s3_object_key": s3_dataset_folder + LORA_FILENAME,
            }
        }
    )
else:
    print({"output": "training failed!"})
