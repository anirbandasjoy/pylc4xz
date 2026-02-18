# Global Builders Usage Guide

This guide shows how to use the global `ResponseBuilder`, `PaginationBuilder`, and `ExceptionBuilder` throughout your FastAPI application.

## Import

```python
from app.core.builders import ResponseBuilder, PaginationBuilder, ExceptionBuilder
```

## ResponseBuilder

### Success Response

```python
@router.get("/users/{user_id}")
async def get_user(user_id: int):
    user = get_user_from_db(user_id)

    if not user:
        return ExceptionBuilder.not_found(resource="User", resource_id=user_id)

    return ResponseBuilder.success(
        data=user,
        message="User retrieved successfully",
        metadata={"permissions": ["read", "write"]},
    )
```

**Response:**
```json
{
  "success": true,
  "message": "User retrieved successfully",
  "data": {
    "id": 1,
    "name": "John Doe"
  },
  "metadata": {
    "permissions": ["read", "write"]
  }
}
```

### Created Response (201)

```python
@router.post("/users")
async def create_user(user_data: UserCreate):
    user = create_user_in_db(user_data)

    return ResponseBuilder.created(
        data=user,
        message="User created successfully",
    )
```

### No Content Response (204)

```python
@router.delete("/users/{user_id}")
async def delete_user(user_id: int):
    delete_user_from_db(user_id)

    return ResponseBuilder.no_content()
```

### Custom Status Code

```python
return ResponseBuilder.success(
    data={"accepted": True},
    message="Request accepted",
    status_code=202,  # Accepted
)
```

## PaginationBuilder

### Basic Pagination

```python
@router.get("/products")
async def get_products(pagination: PaginationDep):
    products, total = product_service.get_all(
        skip=pagination.skip,
        limit=pagination.limit
    )

    return PaginationBuilder.from_params(
        items=products,
        total=total,
        pagination_params=pagination,
        message="Products retrieved successfully",
    )
```

**Response:**
```json
{
  "success": true,
  "message": "Products retrieved successfully",
  "items": [
    {"id": 1, "name": "Product 1"},
    {"id": 2, "name": "Product 2"}
  ],
  "pagination": {
    "page": 1,
    "page_size": 10,
    "total_pages": 5,
    "has_next": true,
    "has_prev": false,
    "total": 50
  }
}
```

### Manual Pagination

```python
return PaginationBuilder.build(
    items=products,
    total=100,
    skip=0,
    limit=10,
    message="Products list",
    filters={"category": "Electronics"},  # Additional metadata
)
```

## ExceptionBuilder

### Not Found (404)

```python
# Automatic message
return ExceptionBuilder.not_found(
    resource="Product",
    resource_id=123,
)

# Custom message
return ExceptionBuilder.not_found(
    resource="Product",
    custom_message="Product not found in catalog",
)

# Without ID
return ExceptionBuilder.not_found(resource="Products")
```

**Response:**
```json
{
  "success": false,
  "message": "Product with id '123' not found",
  "error_code": "NOT_FOUND",
  "resource": "Product",
  "resource_id": 123
}
```

### Validation Error (422)

```python
errors = [
    {"field": "email", "message": "Invalid email format"},
    {"field": "age", "message": "Must be greater than 18"}
]

return ExceptionBuilder.validation_error(
    errors=errors,
    message="Please fix the validation errors",
)
```

### Bad Request (400)

```python
return ExceptionBuilder.bad_request(
    message="Invalid search parameters",
    error_code="INVALID_SEARCH_PARAMS",
    hint="Use 'q' parameter for search query",
)
```

### Conflict (409)

```python
return ExceptionBuilder.conflict(
    message="User with this email already exists",
    error_code="EMAIL_EXISTS",
    field="email",
)
```

### Unauthorized (401)

```python
return ExceptionBuilder.unauthorized(
    message="Invalid or expired token",
    error_code="INVALID_TOKEN",
)
```

### Forbidden (403)

```python
return ExceptionBuilder.forbidden(
    message="You don't have permission to access this resource",
    error_code="INSUFFICIENT_PERMISSIONS",
)
```

### Route Not Found (404)

```python
@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return ExceptionBuilder.route_not_found(
        path=request.url.path,
        method=request.method,
    )
```

### Internal Server Error (500)

```python
try:
    result = risky_operation()
except Exception:
    logger.exception("Operation failed")
    return ExceptionBuilder.internal_error(
        message="Failed to process request",
        error_code="OPERATION_FAILED",
    )
```

## Real-World Examples

### Complete CRUD Router

```python
from fastapi import APIRouter, Depends, Query
from app.core.builders import ResponseBuilder, PaginationBuilder, ExceptionBuilder
from app.core.dependencies import PaginationDep
from typing import Optional

router = APIRouter(prefix="/api/v1/users", tags=["users"])

@router.get("")
async def list_users(
    pagination: PaginationDep,
    search: Optional[str] = Query(None),
    service: UserService = Depends(get_user_service),
):
    """List users with pagination and optional search"""
    if search:
        users, total = service.search(search, pagination.skip, pagination.limit)
    else:
        users, total = service.get_all(pagination.skip, pagination.limit)

    return PaginationBuilder.from_params(
        items=[UserResponse(**u).model_dump() for u in users],
        total=total,
        pagination_params=pagination,
        message=f"Found {total} users",
    )

@router.get("/{user_id}")
async def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
):
    """Get a single user by ID"""
    user = service.get_by_id(user_id)

    if not user:
        return ExceptionBuilder.not_found(
            resource="User",
            resource_id=user_id,
        )

    return ResponseBuilder.success(
        data=UserResponse(**user).model_dump(),
        message="User retrieved successfully",
    )

@router.post("")
async def create_user(
    user_data: UserCreate,
    service: UserService = Depends(get_user_service),
):
    """Create a new user"""
    # Check if email already exists
    if service.email_exists(user_data.email):
        return ExceptionBuilder.conflict(
            message="User with this email already exists",
            error_code="EMAIL_EXISTS",
        )

    user = service.create(user_data)

    return ResponseBuilder.created(
        data=UserResponse(**user).model_dump(),
        message="User created successfully",
    )

@router.patch("/{user_id}")
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    service: UserService = Depends(get_user_service),
):
    """Partially update a user"""
    user = service.update(user_id, user_data)

    if not user:
        return ExceptionBuilder.not_found(
            resource="User",
            resource_id=user_id,
        )

    return ResponseBuilder.success(
        data=UserResponse(**user).model_dump(),
        message="User updated successfully",
    )

@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
):
    """Delete a user"""
    success = service.delete(user_id)

    if not success:
        return ExceptionBuilder.not_found(
            resource="User",
            resource_id=user_id,
        )

    return ResponseBuilder.no_content()
```

### Custom Response with Metadata

```python
@router.get("/dashboard")
async def get_dashboard(user_id: int):
    stats = calculate_dashboard_stats(user_id)

    return ResponseBuilder.success(
        data=stats,
        message="Dashboard data retrieved",
        metadata={
            "generated_at": datetime.now().isoformat(),
            "refresh_interval": 300,  # seconds
            "cache_key": f"dashboard_{user_id}",
        },
    )
```

## Best Practices

1. **Always use builders** - Never manually construct JSONResponse objects
2. **Be consistent** - Use the same error codes across your application
3. **Include metadata** - Add helpful metadata to responses when appropriate
4. **Log exceptions** - Always log errors before returning error responses
5. **Use pagination** - Always use PaginationBuilder for list responses
6. **Clear messages** - Write clear, user-friendly error messages

## Common Error Codes

```python
# Predefined error codes in ExceptionBuilder
ExceptionBuilder.NOT_FOUND          # "NOT_FOUND"
ExceptionBuilder.VALIDATION_ERROR   # "VALIDATION_ERROR"
ExceptionBuilder.BAD_REQUEST       # "BAD_REQUEST"
ExceptionBuilder.UNAUTHORIZED       # "UNAUTHORIZED"
ExceptionBuilder.FORBIDDEN          # "FORBIDDEN"
ExceptionBuilder.CONFLICT          # "CONFLICT"
ExceptionBuilder.INTERNAL_ERROR     # "INTERNAL_ERROR"
ExceptionBuilder.ROUTE_NOT_FOUND    # "ROUTE_NOT_FOUND"
```

You can also use custom error codes:

```python
return ExceptionBuilder.bad_request(
    message="Custom error",
    error_code="MY_CUSTOM_ERROR_CODE",
)
```
