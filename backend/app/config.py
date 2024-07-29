import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """
    Configuration class for the Flask application.
    """
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///uav_platform.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    LOCAL_FILE_PATH = os.getenv('LOCAL_FILE_PATH')
    # MinIO Configuration
    MINIO_ENDPOINT = os.getenv('MINIO_ENDPOINT')
    MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY')
    MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY')