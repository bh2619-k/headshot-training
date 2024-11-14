import subprocess
import platform
import runpod
import asyncio
import sys
import os
import boto3
from botocore.exceptions import NoCredentialsError, ClientError

LORA_FILENAME = "pytorch_lora_weights.safetensors"


def file_exists(folder, filename):
    # Construct the full path to the file
    full_path = os.path.join(folder, filename)
    return os.path.exists(full_path)


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


def training(job):
    """
    Runpod serverless function to train a Flux.1 [dev] combining dreambooth and lora method.

    Parameters:
    s3_dataset_bucket (str): The name of the S3 bucket.
    s3_dataset_folder (str): The S3 folder including the image datasets.

    Returns:
    s3_bucket (str): The bucket name of saving the lora weight.
    s3_object_key (str): The S3 object key of saving the lora weight.
    """

    job_input = job["input"]
    s3_bucket = job_input["s3_dataset_bucket"]
    s3_dataset_folder = job_input["s3_dataset_folder"]

    if not isinstance(s3_bucket, str) or not isinstance(s3_dataset_folder, str):
        return {"error": "You need to pass the correct parameters"}

    download_folder_from_s3(s3_bucket, s3_dataset_folder, "./datasets/ohwx")

    script_path = "./train.sh"
    bash_path = "C:\\Program Files\\Git\\bin\\bash.exe"

    # Using Popen to run the Bash script
    print("The type of OS is", platform.system())
    if platform.system() == "Windows":
        process = subprocess.Popen(
            [bash_path, script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    else:
        process = subprocess.Popen(
            [script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )

    # Read the output line by line in real-time
    try:
        while True:
            output = process.stdout.readline()  # Read a line from the output
            if output:  # If there’s output, print it
                print("Captured Output:", output.strip())
            elif process.poll() is not None:  # If the process has ended
                break
    except KeyboardInterrupt:
        print("Process interrupted.")
    finally:
        # Ensure that we close the process
        process.stdout.close()
        process.stderr.close()

        if file_exists("./output/models", LORA_FILENAME):
            upload_file_to_s3(
                "./output/models/" + LORA_FILENAME,
                s3_bucket,
                s3_dataset_folder + "/" + LORA_FILENAME,
            )
            return {
                "output": {
                    "s3_bucket": s3_bucket,
                    "s3_object_key": s3_dataset_folder + "/" + LORA_FILENAME,
                }
            }
        else:
            return {"output": "training failed!"}


if __name__ == "__main__":
    # Use WindowsSelectorEventLoopPolicy on Windows
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    # Start the serverless handler
    runpod.serverless.start({"handler": training})
