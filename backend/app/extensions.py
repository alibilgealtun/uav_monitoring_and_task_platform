from flask_sqlalchemy import SQLAlchemy
from .utils.minio_utils import MinioUtils

db = SQLAlchemy()


def create_minio_client(app):
    """
    Creates and returns a Minio client using the app's configuration.

    Args:
        app (Flask): The Flask application instance.

    Returns:
        MinioUtils: The configured MinioUtil.
    """
    endpoint = app.config.get('MINIO_ENDPOINT')
    access_key = app.config.get('MINIO_ACCESS_KEY')
    secret_key = app.config.get('MINIO_SECRET_KEY')

    if not endpoint or not access_key:
        raise ValueError("MinIO configuration is missing required parameters.")

    return MinioUtils(endpoint, access_key, secret_key)
