from typing import List, Union

from pydantic import AnyHttpUrl, BaseSettings, validator

from enum import Enum
import logging


class EnvironmentString(str, Enum):
    """
    Environments for the application.
    """

    LOCAL = "local"
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class Settings(BaseSettings):
    """
    Custom settings for this app.
    """

    PROJECT_NAME: str
    ENVIRONMENT: EnvironmentString
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(  # pylint: disable=no-self-argument
        cls, v: Union[str, List[str]]  # pylint: disable=unused-argument
    ) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Database
    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: str
    POSTGRES_CONNECTION_POOL_MIN_SIZE: int = 1
    POSTGRES_CONNECTION_POOL_MAX_SIZE: int = 20

    # Monitoring: https://sentry.io/
    SENTRY_ENABLED: bool = False
    SENTRY_DSN: str = ""

    # Remote logging: https://www.mezmo.com/
    LOGDNA_ENABLED: bool = False
    LOGDNA_KEY: str = ""

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
