from functools import partial
from tempfile import NamedTemporaryFile
from typing import IO, TypedDict
from uuid import uuid4

import boto3
from botocore.response import StreamingBody

CHUNK_SIZE = 8096


class GetObjectResponse(TypedDict):
    Body: StreamingBody


class S3Connection:

    def __init__(self, endpoint_url: str) -> None:
        self._endpoint_url = endpoint_url
        self._session = boto3.Session()
        self._client = self._session.client(
            service_name="s3",
            endpoint_url=endpoint_url,
        )

    def get_file(self, bucket_name: str, file_url: str) -> IO:
        filename = file_url.split("/")[-1]
        response: GetObjectResponse = self._client.get_object(Bucket=bucket_name, Key=filename)
        file = response["Body"]
        tempfile = NamedTemporaryFile("rb+")
        for chunk in iter(partial(file.read, CHUNK_SIZE), b""):
            tempfile.write(chunk)

        tempfile.seek(0)
        return tempfile
