from fastapi.routing import APIRouter

from langchain_document_loader.web.api import documents, monitoring

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(documents.router)
