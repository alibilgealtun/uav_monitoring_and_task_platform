import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///uav_platform.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')
    
    # MinIO Configuration
    MINIO_ENDPOINT = os.getenv('MINIO_ENDPOINT', 'play.min.io:443')
    MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY', '2XvNYutcKQ3DVh7GppLz')
    MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY', 'aGZfaPlWl42spcENW6cJN6RgPMXdT6Ol215RBnNn')
    MINIO_SECURE = os.getenv('MINIO_SECURE', 'True').lower() in ['true', '1', 't']
