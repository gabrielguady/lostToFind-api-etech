import os
from abc import ABC, abstractmethod

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
from datetime import datetime

from core import exceptions, models


class BaseBehavior(ABC):
    @abstractmethod
    def run(self):
        raise NotImplementedError('You must subclass and implement the trace rule validation')


class MediaViewBehavior(BaseBehavior):

    def __init__(self, **kwargs):
        self.valid_extensions = ['.jpeg', '.jpg', '.png']
        self.s3_client = self.s3_client_init()
        self.bucket_name = os.environ.get('AWS_STORAGE_BUCKET_NAME')
        self.type_item = kwargs.get('type_item')
        self.id_item = kwargs.get('id_item')
        self.file_obj = kwargs.get('file_obj')
        self.current_time = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        self.file_extension = os.path.splitext(self.file_obj.name)[1]
        self.file_key = f'{self.type_item}_{self.id_item}_{self.current_time}{self.file_extension}'

    @staticmethod
    def s3_client_init():
        return boto3.client('s3',
                            endpoint_url=os.environ.get('AWS_S3_ENDPOINT_URL'),
                            aws_access_key_id=os.environ.get('AWS_S3_ACCESS_KEY_ID'),
                            aws_secret_access_key=os.environ.get('AWS_S3_SECRET_ACCESS_KEY'),
                            config=Config(signature_version='s3v4'),
                            region_name='sa-east-1',
                            verify=False)

    def upload_media(self):
        try:
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=self.file_key,
                Body=self.file_obj,
                ContentType=self.file_obj.content_type,
            )
            return f"{self.s3_client.meta.endpoint_url}/{self.bucket_name}/{self.file_key}"
        except Exception as e:
            raise exceptions.NotUploadMediaMinioException

    def create_media_found_item(self):
        if self.id_item and self.id_item != 'NaN' and self.id_item.isdigit():
            item_id = int(self.id_item)
        else:
            raise ValueError(f"ID inválido: {self.id_item}")

        try:
            found_item = models.FoundItem.objects.get(id=item_id)
        except models.FoundItem.DoesNotExist:
            raise ValueError(f"Item perdido com ID {item_id} não encontrado.")

        url = self.upload_media()
        models.FileImageItem.objects.create(
            filename=self.file_obj.name,
            remote_name=url,
            found_item=found_item
        )

    def create_media_lost_item(self):
        if self.id_item and self.id_item != 'NaN' and self.id_item.isdigit():
            item_id = int(self.id_item)
        else:
            raise ValueError(f"ID inválido: {self.id_item}")

        try:
            lost_item = models.LostItem.objects.get(id=item_id)
        except models.LostItem.DoesNotExist:
            raise ValueError(f"Item perdido com ID {item_id} não encontrado.")

        url = self.upload_media()
        models.FileImageItem.objects.create(
            filename=self.file_obj.name,
            remote_name=url,
            lost_item=lost_item
        )
    def validate_file(self):
        if not self.file_obj.name.endswith(tuple(self.valid_extensions)):
            raise exceptions.InvalidFileException

    def run(self):
        self.validate_file()
        if self.type_item == 'lost_item':
            return self.create_media_lost_item()
        elif self.type_item == 'found_item':
            return self.create_media_found_item()
