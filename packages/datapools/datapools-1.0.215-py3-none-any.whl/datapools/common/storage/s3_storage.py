import io
import tempfile
from contextlib import AbstractContextManager

import boto3
import botocore

from datapools.common.logger import logger

from datapools.common.types import InvalidUsageException

from .base_storage import BaseStorage


class S3Reader(AbstractContextManager):
    def __init__(self, bucket, key):
        self.bucket = bucket
        self.key = key

    def read(self):
        with tempfile.TemporaryFile() as f:
            self.bucket.download_fileobj(self.key, f)
            f.seek(0)
            res = f.read()

        # print(f"{res=}")
        return res

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class S3Storage(BaseStorage):
    def __init__(self, bucket_name):
        self.path = ""
        self.bucket_name = bucket_name
        self.s3 = boto3.resource("s3")
        self.bucket = self.s3.Bucket(self.bucket_name)

    def use_path(self, path):
        self.path = path
        return self

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.path = ""

    def getkey(self, storage_id):
        return self.path + storage_id

    async def put(self, storage_id, content: str | bytes):
        self.bucket.put_object(
            Body=content if isinstance(content, bytes) else content.encode(), Key=self.getkey(storage_id)
        )

    async def upload(self, storage_id, input_path):
        self.bucket.upload_file(input_path, self.getkey(storage_id))

    async def has(self, storage_id) -> bool:
        try:
            self.bucket.Object(self.getkey(storage_id)).load()
            return True
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "404":
                return False
            raise

    def get_reader(self, storage_id):
        return S3Reader(self.bucket, self.getkey(storage_id))

    async def remove(self, storage_id):
        res = self.bucket.delete_objects(
            Delete={
                "Objects": [
                    {"Key": self.getkey(storage_id)},
                ],
                "Quiet": True,
            },
        )
        print(res)
