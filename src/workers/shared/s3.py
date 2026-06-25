import os

import s3fs


class S3Client:
    def __init__(
        self,
        endpoint_url: str | None = None,
        access_key: str | None = None,
        secret_key: str | None = None,
    ):
        self._fs = s3fs.S3FileSystem(
            endpoint_url=endpoint_url or os.environ["MINIO_ENDPOINT"],
            key=access_key or os.environ["MINIO_ROOT_USER"],
            secret=secret_key or os.environ["MINIO_ROOT_PASSWORD"],
        )

    def upload(self, bucket: str, key: str, content: str):
        location = f"{bucket}/{key}"
        self._fs.write_text(location, content)
        return location

    def download(self, bucket: str, key: str) -> str:
        return self._fs.read_text(f"{bucket}/{key}")


s3 = S3Client()
