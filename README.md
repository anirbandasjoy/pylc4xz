# Product API - FastAPI CRUD Application

A well-structured, modular FastAPI application demonstrating best practices for building RESTful APIs with product CRUD operations.

## Architecture

### Project Structure

```
fastApi/
├── app/
│   ├── __init__.py
│   ├── core/                    # Core application components
│   │   ├── __init__.py
│   │   ├── config.py           # Application settings and configuration
│   │   ├── constants.py        # Constants, enums, and configuration values
│   │   ├── exceptions.py       # Custom exception classes
│   │   ├── responses.py        # Response wrappers and handlers
│   │   └── dependencies.py     # Dependency injection functions
│   ├── middleware/              # Custom middleware
│   │   ├── __init__.py
│   │   ├── request_logging.py  # Request/response logging middleware
│   │   └── error_handler.py    # Global error handling middleware
│   ├── models/                  # Database models (for future use)
│   ├── routers/                 # API route handlers
│   │   ├── __init__.py
│   │   └── products.py         # Product endpoints
│   ├── schemas/                 # Pydantic models for validation
│   │   ├── __init__.py
│   │   └── product.py          # Product schemas
│   ├── services/                # Business logic layer
│   │   ├── __init__.py
│   │   ├── base_service.py     # Base service with common CRUD operations
│   │   └── product_service.py  # Product business logic
│   └── utils/                   # Utility functions and decorators
│       ├── __init__.py
│       ├── decorators.py       # Custom decorators
│       └── helpers.py          # Helper functions
├── main.py                      # Application entry point
├── requirements.txt             # Python dependencies
├── .env.example                # Environment variables template
└── README.md                    # This file
```

## Key Features

### 1. Layered Architecture
- **Routers**: Handle HTTP requests/responses
- **Services**: Contain business logic
- **Schemas**: Pydantic models for validation
- **Core**: Shared functionality (exceptions, responses, dependencies)

### 2. Custom Exceptions
- `BaseAPIException`: Base exception for all API errors
- `NotFoundException`: 404 errors
- `BadRequestException`: 400 errors
- `ProductNotFoundException`: Product-specific 404 errors
- And more...

### 3. Response Handlers
- `success_response()`: Standard success response
- `created_response()`: 201 Created response
- `paginated_response()`: Paginated list response
- `no_content_response()`: 204 No Content response

### 4. Base Service Pattern
Reusable base service class with common CRUD operations:
- `get_all()`: Get all entities with filtering
- `get_by_id()`: Get entity by ID
- `create()`: Create new entity
- `update()`: Update entity
- `delete()`: Delete entity
- `search()`: Search entities
- `exists()`: Check existence
- `count()`: Get total count

### 5. Dependency Injection
Type aliases for clean dependency injection:
- `PaginationDep`: Pagination parameters
- `SearchQueryDep`: Search query parameter
- `ProductIdDep`: Product ID parameter

### 6. Middleware
- **RequestLoggingMiddleware**: Logs all requests with timing and request IDs
- **ErrorHandlerMiddleware**: Centralized error handling

### 7. Utilities & Decorators
- `@catch_exceptions`: Catch and handle exceptions
- `@log_execution_time`: Log function execution time
- `@validate_required_fields`: Validate required fields
- `@cache_result`: Cache function results

## API Endpoints

### Products
- `GET /api/v1/products` - Get all products (with pagination & category filter)
- `GET /api/v1/products/search` - Search products
- `GET /api/v1/products/category/{category}` - Get products by category
- `GET /api/v1/products/{id}` - Get single product
- `POST /api/v1/products` - Create new product
- `PUT /api/v1/products/{id}` - Full update
- `PATCH /api/v1/products/{id}` - Partial update
- `PATCH /api/v1/products/{id}/stock` - Update product stock
- `DELETE /api/v1/products/{id}` - Delete product

### Root
- `GET /` - Root endpoint with API info
- `GET /health` - Health check endpoint

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables (optional):
```bash
cp .env.example .env
```

## Running the Application

```bash
uvicorn main:app --reload
```

The API will be available at:
- API: http://localhost:8000
- Interactive docs (Swagger): http://localhost:8000/docs
- Alternative docs (ReDoc): http://localhost:8000/redoc

## Demo Data

The application comes with 8 pre-loaded products:
1. Laptop - $1299.99 (Electronics)
2. Wireless Mouse - $29.99 (Electronics)
3. Mechanical Keyboard - $89.99 (Electronics)
4. HD Monitor 27" - $249.99 (Electronics)
5. USB-C Hub - $49.99 (Accessories)
6. Webcam 1080p - $79.99 (Electronics)
7. Desk Lamp LED - $39.99 (Office)
8. Noise-Cancelling Headphones - $199.99 (Audio)

## Best Practices Implemented

1. **Separation of Concerns**: Clear separation between routes, services, and schemas
2. **DRY Principle**: Base service class with reusable CRUD operations
3. **Dependency Injection**: Clean dependency injection using FastAPI's Depends
4. **Consistent Error Handling**: Custom exceptions with error codes
5. **Consistent Responses**: Standardized response format across all endpoints
6. **Type Hints**: Full type annotations for better IDE support
7. **Validation**: Pydantic models for request/response validation
8. **Logging**: Request logging with timing and unique request IDs
9. **Pagination**: Built-in pagination support
10. **Documentation**: Auto-generated interactive API documentation

## Example Requests

### Create a Product
```bash
curl -X POST "http://localhost:8000/api/v1/products" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Gaming Mouse",
    "description": "High-precision gaming mouse with RGB",
    "price": 59.99,
    "category": "Electronics",
    "stock": 25,
    "is_active": true
  }'
```

### Get All Products (Paginated)
```bash
curl "http://localhost:8000/api/v1/products?skip=0&limit=10"
```

### Search Products
```bash
curl "http://localhost:8000/api/v1/products/search?query=laptop"
```

### Update Product
```bash
curl -X PATCH "http://localhost:8000/api/v1/products/1" \
  -H "Content-Type: application/json" \
  -d '{
    "price": 1199.99,
    "stock": 20
  }'
```

### Delete Product
```bash
curl -X DELETE "http://localhost:8000/api/v1/products/1"
```

## Future Enhancements

- Database integration (SQLAlchemy)
- Authentication & Authorization (JWT)
- Rate limiting
- Caching (Redis)
- Unit and integration tests
- Docker containerization
- CI/CD pipeline
- API versioning (v2)
- WebSocket support
