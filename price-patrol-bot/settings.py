import logging.config
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    TELEGRAM_TOKEN: str
    ADMINS: list[int]
    SQLITE_DSN: str
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


settings = Settings()  # type: ignore


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default_formatter": {
            "format": "[%(asctime)s] [%(levelname)7s] [%(name)s] > %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    "handlers": {
        "stream_handler": {
            "class": "logging.StreamHandler",
            "formater": "default_formatter",
        }
    },
    "loggers": {
        "root": {
            "handlers": ["stream_handler"],
            "level": settings.LOG_LEVEL,
            "propagate": True,
        }
    },
}


logging.config.dictConfig(LOGGING_CONFIG)
