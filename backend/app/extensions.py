from flask_sqlalchemy import SQLAlchemy
from minio import Minio


db = SQLAlchemy()

def create_minio_client(app):
    endpoint = app.config.get('MINIO_ENDPOINT')
    access_key = app.config.get('MINIO_ACCESS_KEY')
    secret_key = app.config.get('MINIO_SECRET_KEY')

    if not endpoint or not access_key:
        raise ValueError("MinIO configuration is missing required parameters.")

    return Minio(
        endpoint,
        access_key=access_key,
        secret_key=secret_key,
        secure=False
    )
