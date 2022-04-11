import logging
import sys
from typing import Any
from typing import Dict
from typing import List
from typing import Tuple

from loguru import logger
from pydantic import PostgresDsn
from pydantic import SecretStr

from app.core.logging import InterceptHandler
from app.core.settings.base import BaseAppSettings


class AppSettings(BaseAppSettings):
    debug: bool = False
    docs_url: str = "/docs"
    # openapi_prefix: str = ""
    # openapi_prefix = "/dev" if ENVIRONMENT == 'development' else ''
    openapi_prefix = ""

    openapi_url: str = "/openapi.json"
    redoc_url: str = "/redoc"
    title: str = "World of Ramen application"
    description: str = "Backend service with python and fastapi"

    version: str = "0.0.0"

    database_url: PostgresDsn
    max_connection_count: int = 10
    min_connection_count: int = 10

    secret_key: SecretStr

    api_prefix: str = "/api"

    jwt_token_prefix: str = "Bearer"

    allowed_hosts: List[str] = ["*"]

    logging_level: int = logging.INFO
    loggers: Tuple[str, str] = ("uvicorn.asgi", "uvicorn.access")

    bucket_name: str = ""
    google_api_key: str = ""
    use_google_place_api: bool = False

    class Config:
        validate_assignment = True

    @property
    def fastapi_kwargs(self) -> Dict[str, Any]:
        return {
            "debug": self.debug,
            "docs_url": self.docs_url,
            "openapi_prefix": self.openapi_prefix,
            "openapi_url": self.openapi_url,
            "redoc_url": self.redoc_url,
            "title": self.title,
            "description": self.description,
            "version": self.version,
        }

    def configure_logging(self) -> None:
        logging.getLogger().handlers = [InterceptHandler()]
        for logger_name in self.loggers:
            logging_logger = logging.getLogger(logger_name)
            logging_logger.handlers = [InterceptHandler(level=self.logging_level)]

        logger.configure(handlers=[{"sink": sys.stderr, "level": self.logging_level}])
