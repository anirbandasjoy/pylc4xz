"""
Global builders for creating consistent API responses.

This module provides reusable builders for:
- API responses
- Paginated responses
- Error responses
- Exception responses

Usage:
    from app.core.builders import ResponseBuilder, PaginationBuilder, ExceptionBuilder

    # Success response
    response = ResponseBuilder.success(
        data={"id": 1, "name": "Product"},
        message="Product created successfully"
    )

    # Paginated response
    response = PaginationBuilder.build(
        items=products,
        total=100,
        skip=0,
        limit=10
    )

    # Error response
    response = ExceptionBuilder.not_found(
        resource="Product",
        resource_id=1
    )
"""

from typing import Any, Optional, TypeVar, Generic, List
from fastapi import status
from fastapi.responses import JSONResponse
from pydantic import BaseModel


T = TypeVar("T")


class ResponseBuilder:
    """Global builder for creating consistent API responses"""

    @staticmethod
    def _build_response(
        success: bool,
        message: str,
        data: Optional[Any] = None,
        error_code: Optional[str] = None,
        metadata: Optional[dict[str, Any]] = None,
    ) -> dict:
        """Build standard response structure"""
        response = {
            "success": success,
            "message": message,
        }

        if data is not None:
            response["data"] = data

        if error_code:
            response["error_code"] = error_code

        if metadata:
            response["metadata"] = metadata

        return response

    @staticmethod
    def success(
        data: Any = None,
        message: str = "Success",
        status_code: int = status.HTTP_200_OK,
        metadata: Optional[dict[str, Any]] = None,
    ) -> JSONResponse:
        """Create a success response

        Args:
            data: Response data
            message: Success message
            status_code: HTTP status code (default: 200)
            metadata: Optional metadata dictionary

        Returns:
            JSONResponse with success structure
        """
        response_data = ResponseBuilder._build_response(
            success=True,
            message=message,
            data=data,
            metadata=metadata,
        )

        return JSONResponse(content=response_data, status_code=status_code)

    @staticmethod
    def created(
        data: Any,
        message: str = "Resource created successfully",
    ) -> JSONResponse:
        """Create a 201 Created response

        Args:
            data: Created resource data
            message: Success message

        Returns:
            JSONResponse with 201 status
        """
        return ResponseBuilder.success(
            data=data,
            message=message,
            status_code=status.HTTP_201_CREATED,
        )

    @staticmethod
    def no_content() -> JSONResponse:
        """Create a 204 No Content response

        Returns:
            JSONResponse with 204 status
        """
        return JSONResponse(content=None, status_code=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def error(
        message: str,
        error_code: Optional[str] = None,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        **extra_data: Any,
    ) -> JSONResponse:
        """Create an error response

        Args:
            message: Error message
            error_code: Optional error code
            status_code: HTTP status code (default: 400)
            **extra_data: Additional fields to include in response

        Returns:
            JSONResponse with error structure
        """
        response_data = ResponseBuilder._build_response(
            success=False,
            message=message,
            error_code=error_code,
        )

        if extra_data:
            response_data.update(extra_data)

        return JSONResponse(content=response_data, status_code=status_code)


class PaginationBuilder:
    """Global builder for creating paginated responses"""

    @staticmethod
    def _calculate_pagination_info(total: int, skip: int, limit: int) -> dict:
        """Calculate pagination metadata

        Args:
            total: Total number of items
            skip: Number of items to skip
            limit: Number of items per page

        Returns:
            Dictionary with pagination metadata
        """
        page = (skip // limit) + 1 if limit else 1
        total_pages = (total + limit - 1) // limit if limit else 0

        return {
            "page": page,
            "page_size": limit,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_prev": page > 1,
            "total": total,
        }

    @staticmethod
    def build(
        items: List[Any],
        total: int,
        skip: int = 0,
        limit: int = 100,
        message: str = "Success",
        **metadata: Any,
    ) -> JSONResponse:
        """Build a paginated response

        Args:
            items: List of items for current page
            total: Total number of items across all pages
            skip: Number of items skipped
            limit: Number of items per page
            message: Success message
            **metadata: Additional metadata to include

        Returns:
            JSONResponse with paginated structure
        """
        pagination_info = PaginationBuilder._calculate_pagination_info(
            total=total, skip=skip, limit=limit
        )

        response_data = {
            "success": True,
            "message": message,
            "items": items,
            "pagination": pagination_info,
        }

        if metadata:
            response_data["metadata"] = metadata

        return JSONResponse(content=response_data, status_code=status.HTTP_200_OK)

    @staticmethod
    def from_params(
        items: List[Any],
        total: int,
        pagination_params: Any,
        message: str = "Success",
        **metadata: Any,
    ) -> JSONResponse:
        """Build paginated response from pagination parameters object

        Args:
            items: List of items for current page
            total: Total number of items
            pagination_params: Object with skip and limit attributes
            message: Success message
            **metadata: Additional metadata

        Returns:
            JSONResponse with paginated structure
        """
        return PaginationBuilder.build(
            items=items,
            total=total,
            skip=pagination_params.skip,
            limit=pagination_params.limit,
            message=message,
            **metadata,
        )


class ExceptionBuilder:
    """Global builder for creating exception responses"""

    # Common error codes
    NOT_FOUND = "NOT_FOUND"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    BAD_REQUEST = "BAD_REQUEST"
    UNAUTHORIZED = "UNAUTHORIZED"
    FORBIDDEN = "FORBIDDEN"
    CONFLICT = "CONFLICT"
    INTERNAL_ERROR = "INTERNAL_ERROR"
    ROUTE_NOT_FOUND = "ROUTE_NOT_FOUND"

    @staticmethod
    def not_found(
        resource: str,
        resource_id: Optional[Any] = None,
        custom_message: Optional[str] = None,
    ) -> JSONResponse:
        """Create a 404 Not Found response

        Args:
            resource: Resource type (e.g., "Product", "User")
            resource_id: ID of the resource
            custom_message: Optional custom message

        Returns:
            JSONResponse with 404 status
        """
        if custom_message:
            message = custom_message
        elif resource_id:
            message = f"{resource} with id '{resource_id}' not found"
        else:
            message = f"{resource} not found"

        return ResponseBuilder.error(
            message=message,
            error_code=ExceptionBuilder.NOT_FOUND,
            status_code=status.HTTP_404_NOT_FOUND,
            resource=resource,
            resource_id=resource_id,
        )

    @staticmethod
    def validation_error(
        errors: List[Any],
        message: str = "Validation error",
    ) -> JSONResponse:
        """Create a 422 Validation Error response

        Args:
            errors: List of validation errors
            message: Error message

        Returns:
            JSONResponse with 422 status
        """
        return ResponseBuilder.error(
            message=message,
            error_code=ExceptionBuilder.VALIDATION_ERROR,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            errors=errors,
        )

    @staticmethod
    def bad_request(
        message: str,
        error_code: Optional[str] = None,
        **extra_data: Any,
    ) -> JSONResponse:
        """Create a 400 Bad Request response

        Args:
            message: Error message
            error_code: Optional error code
            **extra_data: Additional fields

        Returns:
            JSONResponse with 400 status
        """
        return ResponseBuilder.error(
            message=message,
            error_code=error_code or ExceptionBuilder.BAD_REQUEST,
            status_code=status.HTTP_400_BAD_REQUEST,
            **extra_data,
        )

    @staticmethod
    def conflict(
        message: str,
        error_code: Optional[str] = None,
        **extra_data: Any,
    ) -> JSONResponse:
        """Create a 409 Conflict response

        Args:
            message: Error message
            error_code: Optional error code
            **extra_data: Additional fields

        Returns:
            JSONResponse with 409 status
        """
        return ResponseBuilder.error(
            message=message,
            error_code=error_code or ExceptionBuilder.CONFLICT,
            status_code=status.HTTP_409_CONFLICT,
            **extra_data,
        )

    @staticmethod
    def route_not_found(path: str, method: str) -> JSONResponse:
        """Create a 404 Route Not Found response

        Args:
            path: Request path
            method: Request method

        Returns:
            JSONResponse with 404 status
        """
        return ResponseBuilder.error(
            message=f"Route '{method} {path}' not found",
            error_code=ExceptionBuilder.ROUTE_NOT_FOUND,
            status_code=status.HTTP_404_NOT_FOUND,
            path=path,
            method=method,
        )

    @staticmethod
    def internal_error(
        message: str = "Internal server error",
        error_code: Optional[str] = None,
    ) -> JSONResponse:
        """Create a 500 Internal Server Error response

        Args:
            message: Error message
            error_code: Optional error code

        Returns:
            JSONResponse with 500 status
        """
        return ResponseBuilder.error(
            message=message,
            error_code=error_code or ExceptionBuilder.INTERNAL_ERROR,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    @staticmethod
    def unauthorized(
        message: str = "Unauthorized",
        error_code: Optional[str] = None,
    ) -> JSONResponse:
        """Create a 401 Unauthorized response

        Args:
            message: Error message
            error_code: Optional error code

        Returns:
            JSONResponse with 401 status
        """
        return ResponseBuilder.error(
            message=message,
            error_code=error_code or ExceptionBuilder.UNAUTHORIZED,
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    @staticmethod
    def forbidden(
        message: str = "Forbidden",
        error_code: Optional[str] = None,
    ) -> JSONResponse:
        """Create a 403 Forbidden response

        Args:
            message: Error message
            error_code: Optional error code

        Returns:
            JSONResponse with 403 status
        """
        return ResponseBuilder.error(
            message=message,
            error_code=error_code or ExceptionBuilder.FORBIDDEN,
            status_code=status.HTTP_403_FORBIDDEN,
        )


# Convenience imports
__all__ = [
    "ResponseBuilder",
    "PaginationBuilder",
    "ExceptionBuilder",
]
