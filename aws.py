import boto3
from botocore.config import Config

from config import Config

session = boto3.Session(aws_access_key_id=Config.awsAccessKey,
                        aws_secret_access_key=Config.awsSecretKey, region_name="ap-south-1")


class AWS:
    s3 = session.client("s3")
    polly = session.client("polly")
