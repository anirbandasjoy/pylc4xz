from typing import Optional
from fastapi import APIRouter, Query, status, Response, Depends

from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.services.product_service import ProductService, product_service
from app.core.dependencies import PaginationDep, SearchQueryDep
from app.core.builders import ResponseBuilder, PaginationBuilder, ExceptionBuilder
from app.core.exceptions import ProductNotFoundException
from app.core.constants import ResponseMessage


router = APIRouter(prefix="/api/v1/products", tags=["products"])


def get_product_service() -> ProductService:
    """Dependency to get product service instance"""
    return product_service


@router.get("", status_code=status.HTTP_200_OK)
async def get_all_products(
    pagination: PaginationDep,
    category: Optional[str] = Query(None, description="Filter by category"),
    service: ProductService = Depends(get_product_service),
):
    """Get all products with optional category filter and pagination"""
    products, total = service.get_all(
        skip=pagination.skip, limit=pagination.limit, category=category
    )

    return PaginationBuilder.from_params(
        items=[ProductResponse(**p).model_dump() for p in products],
        total=total,
        pagination_params=pagination,
        message=ResponseMessage.SUCCESS.value,
    )


@router.get("/search", status_code=status.HTTP_200_OK)
async def search_products(
    query: SearchQueryDep,
    pagination: PaginationDep,
    service: ProductService = Depends(get_product_service),
):
    """Search products by name, description, or category"""
    if not query:
        return ExceptionBuilder.bad_request(
            message="Please provide a search query",
            error_code="MISSING_QUERY",
        )

    products, total = service.search_products(
        query=query, skip=pagination.skip, limit=pagination.limit
    )

    return PaginationBuilder.from_params(
        items=[ProductResponse(**p).model_dump() for p in products],
        total=total,
        pagination_params=pagination,
        message=f"Found {total} products matching '{query}'",
    )


@router.get("/category/{category}", status_code=status.HTTP_200_OK)
async def get_products_by_category(
    category: str,
    pagination: PaginationDep,
    service: ProductService = Depends(get_product_service),
):
    """Get products by category"""
    products, total = service.get_by_category(
        category=category, skip=pagination.skip, limit=pagination.limit
    )

    return PaginationBuilder.from_params(
        items=[ProductResponse(**p).model_dump() for p in products],
        total=total,
        pagination_params=pagination,
        message=f"Products in {category} category",
    )


@router.get("/{product_id}", status_code=status.HTTP_200_OK)
async def get_product(
    product_id: int,
    service: ProductService = Depends(get_product_service),
):
    """Get a single product by ID"""
    product = service.get_by_id(product_id)

    if not product:
        return ExceptionBuilder.not_found(
            resource="Product",
            resource_id=product_id,
        )

    return ResponseBuilder.success(
        data=ProductResponse(**product).model_dump(),
        message="Product retrieved successfully",
    )


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreate,
    service: ProductService = Depends(get_product_service),
):
    """Create a new product"""
    product = service.create(product_data)
    return ResponseBuilder.created(
        data=ProductResponse(**product).model_dump(),
        message=ResponseMessage.CREATED.value,
    )


@router.put("/{product_id}", status_code=status.HTTP_200_OK)
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    service: ProductService = Depends(get_product_service),
):
    """Update a product (full update)"""
    updated_product = service.update(product_id, product_data)

    if not updated_product:
        return ExceptionBuilder.not_found(
            resource="Product",
            resource_id=product_id,
        )

    return ResponseBuilder.success(
        data=ProductResponse(**updated_product).model_dump(),
        message=ResponseMessage.UPDATED.value,
    )


@router.patch("/{product_id}", status_code=status.HTTP_200_OK)
async def partial_update_product(
    product_id: int,
    product_data: ProductUpdate,
    service: ProductService = Depends(get_product_service),
):
    """Partially update a product"""
    updated_product = service.update(product_id, product_data)

    if not updated_product:
        return ExceptionBuilder.not_found(
            resource="Product",
            resource_id=product_id,
        )

    return ResponseBuilder.success(
        data=ProductResponse(**updated_product).model_dump(),
        message=ResponseMessage.UPDATED.value,
    )


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
    service: ProductService = Depends(get_product_service),
):
    """Delete a product"""
    success = service.delete(product_id)

    if not success:
        return ExceptionBuilder.not_found(
            resource="Product",
            resource_id=product_id,
        )

    return ResponseBuilder.no_content()


@router.patch("/{product_id}/stock", status_code=status.HTTP_200_OK)
async def update_product_stock(
    product_id: int,
    quantity: int = Query(..., ge=0, description="New stock quantity"),
    service: ProductService = Depends(get_product_service),
):
    """Update product stock"""
    product = service.update_stock(product_id, quantity)

    if not product:
        return ExceptionBuilder.not_found(
            resource="Product",
            resource_id=product_id,
        )

    return ResponseBuilder.success(
        data=ProductResponse(**product).model_dump(),
        message="Stock updated successfully",
    )
