from typing import Annotated, Optional
from fastapi import Depends, Query
from app.core.responses import PaginationParams


async def get_pagination_params(
    skip: Annotated[int, Query(ge=0, description="Number of items to skip")] = 0,
    limit: Annotated[
        int, Query(ge=1, le=100, description="Number of items to return")
    ] = 100,
) -> PaginationParams:
    """Dependency for pagination parameters"""
    return PaginationParams(skip=skip, limit=limit)


async def get_product_id(
    product_id: Annotated[int, Query(description="Product ID", ge=1)] = ...,
) -> int:
    """Dependency for product ID"""
    return product_id


async def get_search_query(
    query: Annotated[
        Optional[str], Query(min_length=1, description="Search query")
    ] = None,
) -> Optional[str]:
    """Dependency for search query"""
    return query


# Type aliases for dependency injection
PaginationDep = Annotated[PaginationParams, Depends(get_pagination_params)]
SearchQueryDep = Annotated[Optional[str], Depends(get_search_query)]
ProductIdDep = Annotated[int, Query(..., description="Product ID", ge=1)]
