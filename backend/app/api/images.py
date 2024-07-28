from flask import current_app
import numpy as np
from PIL import Image
import io

def create_and_upload_images(task_id):
    minio_client = current_app.minio_client
    bucket_name = "task-images"
    if not minio_client.bucket_exists(bucket_name):
        minio_client.make_bucket(bucket_name)

    image_urls = []
    for i in range(5):
        image_data = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
        image_pil = Image.fromarray(image_data, 'RGB')

        image_bytes_io = io.BytesIO()
        image_pil.save(image_bytes_io, format='PNG')
        image_bytes_io.seek(0)

        image_name = f"task_{task_id}_image_{i}.png"

        minio_client.put_object(
            bucket_name, image_name, image_bytes_io, image_bytes_io.getbuffer().nbytes,
            content_type="image/png"
        )

        image_url = f"https://play.min.io:9443/{bucket_name}/{image_name}"
        image_urls.append(image_url)

    return image_urls