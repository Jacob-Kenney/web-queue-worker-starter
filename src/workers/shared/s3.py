import os

import boto3
from botocore.config import Config


class Bucket:
    def __init__(self, client, name: str):
        self._client = client
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    def exists(self) -> bool:
        buckets = self._client.list_buckets()["Buckets"]
        return any(b["Name"] == self._name for b in buckets)

    def create(self):
        self._client.create_bucket(Bucket=self._name)

    def upload_text(self, key: str, content: str):
        self._client.put_object(Bucket=self._name, Key=key, Body=content.encode())

    def download_text(self, key: str) -> str:
        response = self._client.get_object(Bucket=self._name, Key=key)
        return response["Body"].read().decode()

    def delete_object(self, key: str):
        self._client.delete_object(Bucket=self._name, Key=key)


class S3Client:
    def __init__(
        self,
        endpoint_url: str | None = None,
        access_key: str | None = None,
        secret_key: str | None = None,
    ):
        self._client = boto3.client(
            "s3",
            endpoint_url=endpoint_url or os.environ["MINIO_ENDPOINT"],
            aws_access_key_id=access_key or os.environ["MINIO_ROOT_USER"],
            aws_secret_access_key=secret_key or os.environ["MINIO_ROOT_PASSWORD"],
            config=Config(signature_version="s3v4"),
        )

    @property
    def client(self):
        return self._client

    def bucket(self, name: str) -> Bucket:
        bucket = Bucket(self._client, name)
        if not bucket.exists():
            bucket.create()
        return bucket


s3 = S3Client()
