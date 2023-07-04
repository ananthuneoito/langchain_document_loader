from botocore.exceptions import NoCredentialsError
from fastapi import HTTPException, UploadFile
from langchain.document_loaders import S3FileLoader

from langchain_document_loader.services.s3_services import S3Uploader
from langchain_document_loader.settings import settings
from langchain_document_loader.web.api.documents.document_schema import ResponseSchema


def process_pdf_file(s3_url: str) -> ResponseSchema:
    """This function processes a pdf file referenced by s3_url.

    :param  s3_url: url of the pdf file in an s3 bucket
    :returns: a CommonResponse instance that contains either the document text or error
    :raises HTTPException: If failed to process the document
    """
    try:
        # parse the url to get bucket name and object key
        url = s3_url.replace("https://", "")
        segments = url.split("/")
        bucket_name = segments[0].replace(".s3.amazonaws.com", "")
        file_name = segments[-1]

        # Load the pdf file from S3 by using S3FileLoader
        loader = S3FileLoader(bucket_name, file_name)
        docs = loader.load()

        return ResponseSchema(
            message="Successfully fetched the document contents.",
            error=False,
            data={"docs": docs},
        )
    except NoCredentialsError as error:
        raise HTTPException(status_code=settings.http_not_found, detail=str(error))


def upload_s3_file(file: UploadFile) -> ResponseSchema:
    """This function uploads a pdf file to s3 and returns its url.

    :param  file: a file to be uploaded to s3
    :returns: a StandardResponse instance that contains either the file url or error
    :raises HTTPException: If failed to upload the document to s3
    """
    try:
        # upload the pdf file using this class
        uploader = S3Uploader(
            settings.AWS_ACCESS_ID,
            settings.AWS_ACCESS_KEY,
            settings.S3_BUCKET,
        )

        response = uploader.upload(file.file, file.filename)
        return ResponseSchema(
            data={"file_url": response},
            message="Upload successful",
            error=False,
        )
    except NoCredentialsError as error:
        raise HTTPException(status_code=settings.http_not_found, detail=str(error))
