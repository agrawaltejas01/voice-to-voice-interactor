import os
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv(".env"))


class Config:
    openAiApiKey = os.environ["OPENAI_API_KEY"]

    awsAccessKey = os.environ["AWS_ACCESS_KEY"]
    awsSecretKey = os.environ["AWS_SECRET_ACCESS_KEY"]

    pineConeApiKey = os.environ["PINECONE_API_KEY"]

    # Redis
    REDIS_HOST = os.environ["REDIS_HOST"]
    REDIS_USER = os.environ["REDIS_USER"]
    REDIS_PASS = os.environ["REDIS_PASS"]
    REDIS_PORT = os.environ["REDIS_PORT"]
