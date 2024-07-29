import os
import time
import numpy as np
from PIL import Image
import io
from flask import current_app

def create_and_upload_images(task_id):
    """
    Generates random images, saves them locally, uploads them to a MinIO bucket, and returns their URLs.

    Args:
        task_id (int): The ID of the task for which images are being created.

    Returns:
        list: A list of URLs pointing to the uploaded images.
    """
    minio_client = current_app.minio_client
    bucket_name = "task-images"

    # Check if the bucket exists, and create it if not
    if not minio_client.bucket_exists(bucket_name):
        minio_client.make_bucket(bucket_name)
    else:
        print("Bucket already exists")

    local_file_path = current_app.config.get('LOCAL_FILE_PATH')

    image_urls = []

    for i in range(5):
        # Generate random image data
        image_data = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
        image_pil = Image.fromarray(image_data, 'RGB')

        # Generate a unique timestamp for each image
        timestamp = int(time.time() * 1000)  # Milliseconds
        image_name = f"task_{task_id}_image_{timestamp}_{i}.png"
        image_path = os.path.join(local_file_path, image_name)
        image_pil.save(image_path)

        # Upload image to MinIO
        minio_client.fput_object(bucket_name, image_name, image_path)

        # Construct the URL to access the image
        image_url = f"http://localhost:9000/{bucket_name}/{image_name}"
        image_urls.append(image_url)

    return image_urls