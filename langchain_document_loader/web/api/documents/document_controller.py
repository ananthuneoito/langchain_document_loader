from botocore.exceptions import NoCredentialsError
from fastapi import APIRouter, File, HTTPException, UploadFile
from langchain.document_loaders import S3FileLoader

from langchain_document_loader.services.s3_services import S3Uploader
from langchain_document_loader.settings import settings
from langchain_document_loader.web.api.documents.document_schema import ResponseSchema

router = APIRouter()


@router.post("/upload-pdf-to-s3/", response_model=ResponseSchema)
async def upload_pdf_to_s3(file: UploadFile = File(...)) -> ResponseSchema:
    """This function uploads a pdf file to s3 and returns its url.

    :param  file: a file to be uploaded to s3
    :returns: a StandardResponse instance that contains either the file url or error
    :raises HTTPException: If failed to upload the document to s3
    """
    try:
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


@router.post("/process-pdf/", response_model=ResponseSchema)
def process_pdf(s3_url: str) -> ResponseSchema:
    """This function processes a pdf file referenced by s3_url.

    :param  s3_url: url of the pdf file in an s3 bucket
    :returns: a CommonResponse instance that contains either the document text or error
    :raises HTTPException: If failed to process the document
    """
    try:
        url = s3_url.replace("https://", "")
        segments = url.split("/")
        bucket_name = segments[0].replace(".s3.amazonaws.com", "")
        file_name = segments[-1]
        loader = S3FileLoader(bucket_name, file_name)
        docs = loader.load()

        return ResponseSchema(
            message="Successfully fetched the document contents.",
            error=False,
            data={"docs": docs},
        )
    except NoCredentialsError as error:
        raise HTTPException(status_code=settings.http_not_found, detail=str(error))
