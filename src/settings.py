from typing import Literal

from pydantic_settings import BaseSettings

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "standard": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"},
    },
    "handlers": {
        "default": {
            "level": "DEBUG",
            "formatter": "standard",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",  # Default is stderr
        },
    },
    "loggers": {
        "default": {"handlers": ["default"], "level": "DEBUG", "propagate": False},  # root logger
    },
}


class AppSettings(BaseSettings):
    bucket_name: str
    rabbit_url: str
    chats_exchange: str
    s3_endpoint_url: str
    recognition_exchange: str
    messages_recognition_queue_name: str
    sentry_dsn: str | None = None
    environment: Literal["local", "stage", "production"] = "local"


settings = AppSettings()  # pyright: ignore[reportCallIssue]
