import enum
from pathlib import Path
from tempfile import gettempdir

from pydantic import BaseSettings
from yarl import URL

TEMP_DIR = Path(gettempdir())


class LogLevel(str, enum.Enum):  # noqa: WPS600
    """Possible log levels."""

    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class Settings(BaseSettings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """

    host: str = "0.0.0.0"  # noqa:S104
    port: int = 8000
    # quantity of workers for uvicorn
    workers_count: int = 1
    # Enable uvicorn reloading
    reload: bool = False
    AWS_ACCESS_ID: str = "AKIA26YAGLWB7RZFYEE6"
    AWS_ACCESS_KEY: str = "uVEfDZKdBt2Ok0tGSMqKge9BL2PuuhjyfqoeaTVY"
    S3_BUCKET: str = "langchain-document-process"

    # Current environment
    environment: str = "dev"

    log_level: LogLevel = LogLevel.INFO
    http_not_found: int = 400

    @property
    def redis_url(self) -> URL:
        """
        Assemble REDIS URL from settings.

        :return: redis URL.
        """
        path = ""
        if self.redis_base is not None:
            path = f"/{self.redis_base}"
        return URL.build(
            scheme="redis",
            host=self.redis_host,
            port=self.redis_port,
            user=self.redis_user,
            password=self.redis_pass,
            path=path,
        )

    class Config:
        env_file = ".env"
        env_prefix = "LANGCHAIN_DOCUMENT_LOADER_"
        env_file_encoding = "utf-8"


settings = Settings()
