from typing import Any, Optional
from fastapi import HTTPException, status


class BaseAPIException(HTTPException):
    """Base exception for all API errors"""

    def __init__(
        self,
        status_code: int,
        detail: str,
        error_code: Optional[str] = None,
        **kwargs: Any,
    ):
        super().__init__(status_code=status_code, detail=detail)
        self.error_code = error_code
        self.extra_data = kwargs


class NotFoundException(BaseAPIException):
    """Exception raised when a resource is not found"""

    def __init__(
        self,
        detail: str = "Resource not found",
        error_code: Optional[str] = None,
        **kwargs: Any,
    ):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
            error_code=error_code,
            **kwargs,
        )


class BadRequestException(BaseAPIException):
    """Exception raised for bad requests"""

    def __init__(
        self,
        detail: str = "Bad request",
        error_code: Optional[str] = None,
        **kwargs: Any,
    ):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
            error_code=error_code,
            **kwargs,
        )


class UnprocessableEntityException(BaseAPIException):
    """Exception raised for validation errors"""

    def __init__(
        self,
        detail: str = "Unprocessable entity",
        error_code: Optional[str] = None,
        **kwargs: Any,
    ):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
            error_code=error_code,
            **kwargs,
        )


class ConflictException(BaseAPIException):
    """Exception raised when a conflict occurs"""

    def __init__(
        self,
        detail: str = "Conflict",
        error_code: Optional[str] = None,
        **kwargs: Any,
    ):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,
            error_code=error_code,
            **kwargs,
        )


class ProductNotFoundException(NotFoundException):
    def __init__(self, product_id: int):
        super().__init__(
            detail=f"Product with id {product_id} not found",
            error_code="PRODUCT_NOT_FOUND",
            product_id=product_id,
        )


class ProductInvalidDataException(BadRequestException):
    def __init__(self, detail: str = "Invalid product data"):
        super().__init__(
            detail=detail,
            error_code="PRODUCT_INVALID_DATA",
        )


class ProductAlreadyExistsException(ConflictException):
    def __init__(self, detail: str = "Product already exists"):
        super().__init__(
            detail=detail,
            error_code="PRODUCT_ALREADY_EXISTS",
        )
