"""Utilities for initializing servers and jobs."""

import logging
import logging.handlers
import os
from typing import Optional
from typing import Dict


from fastapi import FastAPI
from fastapi import Request
from fastapi.exceptions import (
    RequestValidationError,
    HTTPException as StarletteHTTPException,
)
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)

from starlette_context import context
from starlette_context.middleware import RawContextMiddleware
import once


from .utils.request_utils import get_span_id, format_exception
from .gcp_log_formatter import GcpLogFormatter


def setup_fastapi(
    app: FastAPI,
    additional_headers: Optional[Dict[str, str]] = None,
) -> FastAPI:
    """Initialization for a FastAPI server."""

    @app.exception_handler(StarletteHTTPException)
    async def custom_http_exception_handler(
        request: Request, exc: StarletteHTTPException
    ):
        if exc.status_code < 500:
            logging.warning(f"{exc}\\n{format_exception(exc)}")
        else:
            logging.error(
                f"Exception occurred for {request.url.path}:\n{format_exception(exc)}"
            )
        return await http_exception_handler(request, exc)

    @app.exception_handler(RequestValidationError)
    async def custom_http_422_error_handler(
        request: Request, exc: RequestValidationError
    ):
        logging.warning(f"{exc}\\n{format_exception(exc)}")

        return await request_validation_exception_handler(request, exc)

    @app.middleware("http")
    async def log_hook(request: Request, call_next):
        context.data["http_request"] = {
            "request_method": request.method,
            "request_url": str(request.url),
            "user_agent": request.headers.get("User-Agent"),
            "remote_ip": request.client.host if request.client else None,
            "referer": request.headers.get("Referer"),
            "protocol": request.url.scheme,
        }

        context.data["span_id"] = get_span_id(request)

        if additional_headers is not None:
            for header_key in additional_headers.keys():
                header_value = additional_headers.get(header_key)
                if header_value:  # Check if header_value is not None or empty
                    context.data[header_key] = request.headers.get(header_value)

        # This will not include patient's sign in email
        # Only emails used to access resources behind IAP
        if "x-goog-authenticated-user-email" in request.headers:
            # Put IAP data in context for subsequent logs associated with this request
            context.data["iap_email"] = request.headers[
                "x-goog-authenticated-user-email"
            ]

            # Logging IAP information
            logging.info(
                f"{context.data['http_request']['request_method'] } {context.data['http_request']['request_url']} by {context.data['iap_email']}"
            )
        else:
            logging.warning("Request not authenticated by IAP")
            logging.info(
                f"{context.data['http_request']['request_method'] } {context.data['http_request']['request_url']}"
            )

        # Strangely named `call_next` actually routes the request to the proper
        # http handler, passing through any other middleware along the way.

        response = await call_next(request)

        return response

    # Middleware is like an onion, and we'd like this to be the outermost layer, so
    # we add it last.
    app.add_middleware(RawContextMiddleware)

    _setup_gcp_logging()

    print("finished startup job")

    return app


@once.once
def _setup_gcp_logging() -> None:
    """Do needed setup for running in GCP.

    For now just initializes cloud logging, tracing, and opentelemtry.
    It can be called multiple times (from multiple threads), but will only run
    once. However, it will block all callers until complete.
    """
    if not os.environ.get("IS_TEST") == "true":
        from google.cloud import (
            logging as glogging,
        )  # pylint: disable=import-outside-toplevel

        client = glogging.Client()
        client.setup_logging(log_level=logging.INFO)
    # We set force=True incase any of our imports used the root logger before main even ran,
    # which would create a config we need to override
    logging.basicConfig(
        level=logging.INFO,
        force=True,
    )

    logging.getLogger().handlers[0].setFormatter(
        GcpLogFormatter("[%(module)s:%(lineno)d]: %(message)s")
    )

    # Format logging for Uvicorn FastAPI
    uvicorn_logger = logging.getLogger("uvicorn.access")
    uvicorn_handler = logging.StreamHandler()
    uvicorn_handler.setFormatter(GcpLogFormatter("%(levelname)s: %(message)s"))
    uvicorn_logger.addHandler(uvicorn_handler)

    logging.getLogger("ddtrace").setLevel(logging.WARNING)
    logging.getLogger("ddtrace.internal.writer.writer").setLevel(logging.ERROR)

    # logging.getLogger("uvicorn.error").disabled = True
    logging.getLogger("uvicorn.access").disabled = True
    logging.getLogger("uvicorn.warning").disabled = True

    logging.info("GCP setup complete.")
