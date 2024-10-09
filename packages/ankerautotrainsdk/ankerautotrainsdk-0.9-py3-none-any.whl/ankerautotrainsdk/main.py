import requests
from os.path import join, dirname, abspath, basename, exists
from os import makedirs
from .types import *

class AnkerAutoTrainSDK:
    def __init__(self, url="https://dataloop.anker-in.com"):
        self.url = url

    def upload_image(self, image_path: str, directory: str)-> UploadImageResponse:
        url = f"{self.url}/get_upload_url"
        file_name = basename(image_path)

        response = requests.post(url, params={"directory": directory, "file_name": file_name})
        if response.status_code != 200:
            raise Exception(f"Error uploading file: {response.text}")
        response = response.json()
        upload_url = response["url"]
        # 然后put 到这个路径
        with open(image_path, "rb") as f:
            response = requests.put(upload_url, data=f)
            if response.status_code != 200:
                raise Exception(f"Error uploading file: {response.text}")
        return response

    def download_image(self, storage_id: str, bucket: str, object_name: str, directory: str)-> str:
        url = f"{self.url}/get_download_url"
        response = requests.post(url, params={"storage_id": storage_id, "bucket": bucket, "object_name": object_name})
        if response.status_code != 200:
            raise Exception(f"Error uploading file: {response.text}")
        response = response.json()
        download_url = response["url"]
        response = requests.get(download_url)
        # 保存到本地
        save_path = join(directory, object_name)
        # 判断目录是否存在
        if not exists(dirname(save_path)):
            makedirs(dirname(save_path))
        with open(save_path, "wb") as f:
            f.write(response.content)
        return save_path
