from typing import BinaryIO

import boto3
from botocore.exceptions import NoCredentialsError
from fastapi import HTTPException

from langchain_document_loader.settings import settings


class S3Uploader:
    """Upload files to S3 bucket."""

    def __init__(self, access_key: str, secret_key: str, bucket_name: str):
        """
        Initialize S3Uploader with AWS S3 credentials and bucket name.

        :param access_key: AWS access key ID
        :param secret_key: AWS secret key
        :param bucket_name: name of the S3 bucket
        """
        print("access_key", access_key)
        print("secret_key", secret_key)
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )
        self.bucket_name = bucket_name

    def upload(self, file: BinaryIO, filename: str) -> str:
        """
        Upload a file to AWS S3 and return its public URL.

        :param file: file object to upload
        :param filename: name of the file in S3
        :return: public URL of the uploaded file in AWS S3
        :raises HTTPException: if the file was not found/ AWS credentials fails
        """
        try:
            self.s3.upload_fileobj(
                file,
                self.bucket_name,
                filename,
                ExtraArgs={"ACL": "public-read"},
            )

            return f"https://{self.bucket_name}.s3.amazonaws.com/{filename}"

        except FileNotFoundError:
            raise HTTPException(
                status_code=settings.http_not_found, detail="The file was not found.",
            )

        except NoCredentialsError:
            raise HTTPException(
                status_code=settings.http_not_found, detail="Credentials not available",
            )
