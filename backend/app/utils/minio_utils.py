import os
from minio import Minio


class MinioUtils:
    def __init__(self, endpoint, access_key, secret_key, secure=False):
        self.endpoint = endpoint
        self.client = Minio(endpoint, access_key=access_key, secret_key=secret_key, secure=secure)

    def create_bucket(self, bucket_name):
        """
            Creates a bucket if it doesn't already exist.
        :param bucket_name:
        :return:
        """
        try:
            if not self.client.bucket_exists(bucket_name):
                self.client.make_bucket(bucket_name)
            else:
                print("Bucket exists.")
        except Exception as e:
            print(f"Error creating bucket: {e}")

    def upload_image(self, bucket_name, image_path):
        """
        Uploads an image to a MinIO bucket.

        Args:
            bucket_name (str): The name of the bucket.
            image_path (str): The local file path of the image to be uploaded.

        Returns:
            str: The URL of the uploaded image.
        """
        image_name = os.path.basename(image_path)
        image_url = f"{self.endpoint}/{bucket_name}/{image_name}"
        """
        try:
            self.client.fput_object(bucket_name, image_name, image_path)
        except Exception as e:
            print(f"Error in putting object for {bucket_name}, {image_name}\n Error: ", e)
        """
        return image_url
