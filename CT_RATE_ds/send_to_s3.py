import boto3
import os

s3_client = boto3.client("s3")

bucket_name = "data-volume-test-rate"
s3_path = "/"

local_dir = "~/Builds/builds/CT-RATE/data_volumes"

for root, _, files in os.walk(local_dir):
    for file in files:
        local_file_path = os.path.join(root, file)
        s3_file_path = os.path.join(
            s3_path, os.path.relpath(local_file_path, local_dir)
        )

        s3_client.upload_file(local_file_path, bucket_name, s3_file_path)
        print(f"Uploaded {local_file_path} to s3://{bucket_name}/{s3_file_path}")
