from fastapi import APIRouter, File, UploadFile

from langchain_document_loader.services.document_service import (
    process_pdf_file,
    upload_s3_file,
)
from langchain_document_loader.web.api.documents.document_schema import ResponseSchema

router = APIRouter()


@router.post("/upload-pdf-to-s3/", response_model=ResponseSchema)
async def upload_pdf_to_s3(file: UploadFile = File(...)) -> ResponseSchema:
    """This function uploads a pdf file to s3 and returns its url.

    :param  file: a file to be uploaded to s3
    :returns: a StandardResponse instance that contains either the file url or error
    """
    # call the pdf upload service
    return upload_s3_file(file)


@router.post("/process-pdf/", response_model=ResponseSchema)
def process_pdf(s3_url: str) -> ResponseSchema:
    """This function processes a pdf file referenced by s3_url.

    :param  s3_url: url of the pdf file in an s3 bucket
    :returns: a CommonResponse instance that contains either the document text or error
    """
    # call the process pdf service
    return process_pdf_file(s3_url)
