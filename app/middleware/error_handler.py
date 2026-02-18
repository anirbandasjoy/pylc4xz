from typing import Any
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import logging

from app.core.exceptions import BaseAPIException
from app.core.builders import ExceptionBuilder

logger = logging.getLogger(__name__)


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """Middleware to handle all exceptions and return consistent error responses"""

    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)

            # Handle 404 for routes that don't exist
            if response.status_code == 404:
                return self._handle_not_found(request)

            return response
        except Exception as exc:
            return await self.handle_exception(request, exc)

    async def handle_exception(self, request: Request, exc: Exception) -> JSONResponse:
        """Handle exception and return appropriate error response"""

        # Handle custom API exceptions
        if isinstance(exc, BaseAPIException):
            return self._handle_api_exception(request, exc)

        # Handle validation errors
        if isinstance(exc, RequestValidationError):
            return self._handle_validation_error(request, exc)

        # Handle HTTP exceptions
        if isinstance(exc, StarletteHTTPException):
            return self._handle_http_exception(request, exc)

        # Handle unknown exceptions
        return self._handle_unknown_exception(request, exc)

    def _handle_not_found(self, request: Request) -> JSONResponse:
        """Handle 404 for routes that don't exist"""
        logger.warning(f"Route not found: {request.method} {request.url.path}")
        return ExceptionBuilder.route_not_found(
            path=request.url.path,
            method=request.method,
        )

    def _handle_api_exception(
        self, request: Request, exc: BaseAPIException
    ) -> JSONResponse:
        """Handle custom API exceptions"""
        logger.warning(f"API Exception: {exc.detail} - {request.url}")

        response = ExceptionBuilder.error(
            message=exc.detail,
            error_code=exc.error_code,
            status_code=exc.status_code,
        )

        # Add extra data if present
        if exc.extra_data:
            content = eval(response.body.decode())
            content.update(exc.extra_data)
            response.body = JSONResponse(content=content).body

        return response

    def _handle_validation_error(
        self, request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        """Handle validation errors"""
        logger.warning(f"Validation Error: {exc.errors()} - {request.url}")
        return ExceptionBuilder.validation_error(errors=exc.errors())

    def _handle_http_exception(
        self, request: Request, exc: StarletteHTTPException
    ) -> JSONResponse:
        """Handle HTTP exceptions"""
        logger.warning(f"HTTP Exception: {exc.detail} - {request.url}")

        # Special handling for 404 exceptions
        if exc.status_code == 404:
            return ExceptionBuilder.not_found(
                resource="Resource",
                custom_message=str(exc.detail) or "Resource not found",
            )

        return ExceptionBuilder.error(
            message=str(exc.detail),
            error_code="HTTP_ERROR",
            status_code=exc.status_code,
        )

    def _handle_unknown_exception(
        self, request: Request, exc: Exception
    ) -> JSONResponse:
        """Handle unknown exceptions"""
        logger.error(f"Unhandled Exception: {str(exc)} - {request.url}", exc_info=True)
        return ExceptionBuilder.internal_error()
