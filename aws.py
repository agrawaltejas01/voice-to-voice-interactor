import boto3
from botocore.config import Config

from config import Config as configCreds

session = boto3.Session(aws_access_key_id=configCreds.awsAccessKey,
                        aws_secret_access_key=configCreds.awsSecretKey, region_name="ap-south-1")


class AWS:
    s3 = session.client("s3")
    polly = session.client("polly")


class AWS_S3:

    def __init__(self):
        aws = AWS()
        self.s3 = aws.s3

    def upload_file_to_s3(cls, bucket_name, object_name, content_type, data=None, file_path=None,):
        try:
            if file_path:
                with open(file_path, 'rb') as file_data:
                    response = cls.s3.put_object(
                        Bucket=bucket_name, Key=object_name, Body=file_data, ContentType=content_type)
            elif data:
                response = cls.s3.put_object(
                    Bucket=bucket_name, Key=object_name, Body=data, ContentType=content_type)
            else:
                raise ValueError("Either file_path or data must be provided")

            print(f"File uploaded successfully to {bucket_name}/{object_name}")
            return response
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def download_file_from_s3(cls, bucket_name, object_name, file_path):
        try:
            response = cls.s3.download_file(
                bucket_name, object_name, file_path)
            print(f"File downloaded successfully to {file_path}")
            return response
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
