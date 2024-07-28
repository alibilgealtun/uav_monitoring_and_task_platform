from flask_sqlalchemy import SQLAlchemy
from minio import Minio

db = SQLAlchemy()

def create_minio_client(app):
    return Minio(
        app.config['MINIO_ENDPOINT'],
        access_key=app.config['MINIO_ACCESS_KEY'],
        secret_key=app.config['MINIO_SECRET_KEY'],
        secure=True
    )