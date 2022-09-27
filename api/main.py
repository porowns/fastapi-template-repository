import sentry_sdk
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from api.settings import settings
from api.migrations import create_tables
from api.router import router
from api.tracing import RequestContextTracingMiddleware


def development():
    """
    Launched with `poetry run start` at root level
    Used strictly for debugging / local development.
    """
    create_tables()
    uvicorn.run(
        "api.main:api",
        host="localhost",
        port=8000,
        reload=True,
    )


def production():
    """
    Launched with `poetry run start` at root level
    Used strictly for debugging / local development.
    """
    uvicorn.run("api.main:api", host="0.0.0.0", port=8000)


def migrate():
    """
    Launched with `poetry run migrate` at root level
    Used strictly for debugging / local development.
    """
    create_tables()


def get_application():
    if settings.SENTRY_ENABLED:
        sentry_sdk.init(
            dsn=settings.SENTRY_DSN,
            # Set traces_sample_rate to 1.0 to capture 100%
            # of transactions for performance monitoring.
            # We recommend adjusting this value in production,
            traces_sample_rate=1.0,
        )

    _api = FastAPI(title=settings.PROJECT_NAME)  # pylint: disable=invalid-name

    # Add middleware
    _api.add_middleware(
        CORSMiddleware,
        allow_origins=[
            str(origin) for origin in settings.BACKEND_CORS_ORIGINS
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    _api.add_middleware(middleware_class=RequestContextTracingMiddleware)

    # Add router(s)
    _api.include_router(router=router)
    return _api


api = get_application()
if settings.SENTRY_ENABLED:
    api = SentryAsgiMiddleware(api)

if __name__ == "__main__":
    development()
