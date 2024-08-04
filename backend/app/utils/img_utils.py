import os
import time
import numpy as np
from PIL import Image
from flask import current_app
from .minio_utils import MinioUtils



class ImageUtils:
    @staticmethod
    def create_and_upload_images(task_id):
        """
        Generates dummy images, saves them locally, uploads them to a MinIO bucket, and returns their URLs.

        Args:
            task_id (int): The ID of the task for which images are being created.

        Returns:
            list: A list of URLs pointing to the uploaded images.
        """

        minio_cli = MinioUtils(current_app.config.get('MINIO_ENDPOINT'),
                               current_app.config.get('MINIO_ACCESS_KEY'),
                               current_app.config.get('MINIO_SECRET_KEY'))
        bucket_name = "task-images"

        #minio_cli.create_bucket(bucket_name)

        image_urls = []
        for i in range(5):
            try:
                image_path = ImageUtils.create_dummy_img(task_id, i)
                image_url = minio_cli.upload_image(bucket_name, image_path)
                image_urls.append(image_url)
            except Exception as e:
                print(e)

        return image_urls

    @staticmethod
    def create_dummy_img(task_id, index):
        """
        Generates a dummy image and saves it locally (to /tmp/ if not changed) and to minio.

        Args:
            task_id (int): The ID of the task for which the image is being created.
            index (int): The index of the image in the sequence.

        Returns:
            str: The local file path of the saved image.
        """
        local_file_path = current_app.config.get('LOCAL_FILE_PATH')

        # Generate random image data
        image_data = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
        image_pil = Image.fromarray(image_data, 'RGB')

        # Generate a unique timestamp for each image
        timestamp = int(time.time() * 1000)  # Milliseconds
        image_name = f"task_{task_id}_image_{timestamp}_{index}.png"
        image_path = os.path.join(local_file_path, image_name)

        try:
            image_pil.save(image_path)
        except Exception as e:
            print(e)

        return image_path
