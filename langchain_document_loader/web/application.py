from importlib import metadata

from fastapi import FastAPI
from fastapi.responses import UJSONResponse

from langchain_document_loader.web.api.router import api_router
from langchain_document_loader.web.lifetime import (
    register_shutdown_event,
    register_startup_event,
)


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    app = FastAPI(
        title="langchain_document_loader",
        version=metadata.version("langchain_document_loader"),
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
    )

    # Adds startup and shutdown events.
    register_startup_event(app)
    register_shutdown_event(app)

    # Main router for the API.
    app.include_router(router=api_router, prefix="/api")

    return app
