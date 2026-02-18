from typing import Any, Generic, TypeVar, Optional
from pydantic import BaseModel, Field
from fastapi import status
from fastapi.responses import JSONResponse


T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    """Standard API response wrapper"""

    success: bool = Field(..., description="Indicates if the request was successful")
    message: str = Field(..., description="Human-readable message")
    data: Optional[T] = Field(None, description="Response data")
    error_code: Optional[str] = Field(None, description="Error code if an error occurred")
    metadata: Optional[dict[str, Any]] = Field(None, description="Additional metadata")

    class Config:
        arbitrary_types_allowed = True


class PaginatedResponse(BaseModel, Generic[T]):
    """Response for paginated data"""

    success: bool = True
    items: list[T] = Field(..., description="List of items")
    total: int = Field(..., description="Total number of items")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of items per page")
    total_pages: int = Field(..., description="Total number of pages")
    has_next: bool = Field(..., description="Whether there is a next page")
    has_prev: bool = Field(..., description="Whether there is a previous page")


class PaginationParams(BaseModel):
    """Pagination parameters"""

    skip: int = Field(0, ge=0, description="Number of items to skip")
    limit: int = Field(100, ge=1, le=100, description="Number of items to return")

    @property
    def page(self) -> int:
        return self.skip // self.limit + 1 if self.limit else 1


def success_response(
    data: Any = None,
    message: str = "Success",
    status_code: int = status.HTTP_200_OK,
    metadata: Optional[dict[str, Any]] = None,
) -> JSONResponse:
    """Create a success response"""
    response = ApiResponse(
        success=True,
        message=message,
        data=data,
        metadata=metadata,
    )
    return JSONResponse(content=response.model_dump(), status_code=status_code)


def created_response(
    data: Any,
    message: str = "Resource created successfully",
) -> JSONResponse:
    """Create a 201 Created response"""
    return success_response(data=data, message=message, status_code=status.HTTP_201_CREATED)


def no_content_response() -> JSONResponse:
    """Create a 204 No Content response"""
    return JSONResponse(content=None, status_code=status.HTTP_204_NO_CONTENT)


def paginated_response(
    items: list[Any],
    total: int,
    skip: int,
    limit: int,
    message: str = "Success",
) -> JSONResponse:
    """Create a paginated response"""
    total_pages = (total + limit - 1) // limit if limit else 0
    page = skip // limit + 1 if limit else 1

    response = PaginatedResponse(
        success=True,
        items=items,
        total=total,
        page=page,
        page_size=limit,
        total_pages=total_pages,
        has_next=page < total_pages,
        has_prev=page > 1,
    )

    return JSONResponse(content=response.model_dump(), status_code=status.HTTP_200_OK)
