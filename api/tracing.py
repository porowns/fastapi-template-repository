from contextvars import ContextVar
from uuid import uuid4

from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)
from starlette.requests import Request

CORRELATION_ID_CTX_KEY = "correlation_id"
REQUEST_ID_CTX_KEY = "request_id"

_correlation_id_ctx_var: ContextVar[str] = ContextVar(
    CORRELATION_ID_CTX_KEY, default=None  # type: ignore
)
_request_id_ctx_var: ContextVar[str] = ContextVar(
    REQUEST_ID_CTX_KEY, default=None  # type: ignore
)


def get_correlation_id() -> str:
    return _correlation_id_ctx_var.get()


def get_request_id() -> str:
    return _request_id_ctx_var.get()


class RequestContextTracingMiddleware(BaseHTTPMiddleware):
    """
    Adds a correlation ID and request ID to the request and response headers.

    Clients should use X-Correlation-ID or X-Request-ID
    to correlate requests and responses.

    Python developers should use the following:
        get_correlation_id()
        get_request_id()
    functions to fetch IDs.
    """

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ):
        correlation_id = _correlation_id_ctx_var.set(
            request.headers.get("X-Correlation-ID", str(uuid4()))
        )
        request_id = _request_id_ctx_var.set(str(uuid4()))

        response = await call_next(request)
        response.headers["X-Correlation-ID"] = get_correlation_id()
        response.headers["X-Request-ID"] = get_request_id()

        _correlation_id_ctx_var.reset(correlation_id)
        _request_id_ctx_var.reset(request_id)

        return response
