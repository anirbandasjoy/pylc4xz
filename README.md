# Product API - FastAPI

A well-structured, modular FastAPI application demonstrating best practices for building RESTful APIs with product CRUD operations, JWT authentication, and user management.

## 📚 Documentation Guides

- **[⚡ QUICK_START.md](QUICK_START.md)** - Fastest way to start running the project
- **[🚀 RUN_FULL_PROJECT.md](RUN_FULL_PROJECT.md)** - Complete guide to run the full project
- **[🔐 AUTHENTICATION_SETUP.md](AUTHENTICATION_SETUP.md)** - Authentication system setup and usage

## 🚀 Quick Start

### Easiest Way - Interactive Menu

```bash
./run-project.sh
```

### Manual Setup - Two Terminals

**Terminal 1 (PostgreSQL):**
```bash
docker-compose up
```

**Terminal 2 (FastAPI):**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload
```

### Access Points

- **API**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs
- **pgAdmin**: http://localhost:5050

---

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
│   │   ├── dependencies.py     # Dependency injection functions
│   │   ├── database.py         # Database connection and session
│   │   ├── security.py         # JWT and password hashing utilities
│   │   └── auth_dependencies.py # Authentication dependencies
│   ├── middleware/              # Custom middleware
│   │   ├── __init__.py
│   │   ├── request_logging.py  # Request/response logging middleware
│   │   └── error_handler.py    # Global error handling middleware
│   ├── models/                  # Database models
│   │   ├── __init__.py
│   │   └── user.py             # User model and schemas
│   ├── routers/                 # API route handlers
│   │   ├── __init__.py
│   │   ├── products.py         # Product endpoints
│   │   ├── auth.py             # Authentication endpoints
│   │   └── users.py            # User management endpoints
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

### 1. JWT Authentication & Authorization

OAuth 2.0 compliant JWT token-based authentication with role-based access control (RBAC):

- **User Registration**: Create new user accounts with email/username
- **User Login**: OAuth2 password flow with JWT tokens
- **Token Refresh**: Refresh access tokens using refresh tokens
- **Password Hashing**: Bcrypt-based secure password hashing
- **Role-Based Access**: Admin, Moderator, and User roles
- **Protected Routes**: JWT-based route protection

### 2. User Management

Complete CRUD operations for user management:

- **Get All Users**: List all users with pagination (Admin/Moderator)
- **Get User by ID**: Retrieve specific user details
- **Update User**: Modify user information and roles
- **Delete User**: Terminate user accounts
- **Activate/Deactivate**: Enable or disable user accounts
- **Verify User**: Email verification management
- **User Statistics**: Get user counts and statistics

### 3. Layered Architecture

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

### Authentication

- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login with OAuth2 (get JWT token)
- `POST /api/v1/auth/refresh` - Refresh access token
- `GET /api/v1/auth/me` - Get current user info
- `PUT /api/v1/auth/change-password` - Change user password

### User Management

- `GET /api/v1/users/` - Get all users (Admin/Moderator only)
- `GET /api/v1/users/me` - Get my profile
- `GET /api/v1/users/{user_id}` - Get user by ID (Admin/Moderator only)
- `PUT /api/v1/users/me` - Update my profile
- `PUT /api/v1/users/{user_id}` - Update user by ID (Admin only)
- `DELETE /api/v1/users/{user_id}` - Delete user (Admin only)
- `PATCH /api/v1/users/{user_id}/activate` - Activate user (Admin only)
- `PATCH /api/v1/users/{user_id}/deactivate` - Deactivate user (Admin only)
- `PATCH /api/v1/users/{user_id}/verify` - Verify user email (Admin only)
- `GET /api/v1/users/stats/count` - Get user statistics (Admin only)

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

### Quick Start with Docker (Recommended)

1. Clone the repository
2. Start PostgreSQL with Docker Compose:

```bash
docker-compose up -d
```

This starts:
- PostgreSQL on port `5432`
- pgAdmin on port `5050` (optional web-based database manager)

3. Install Python dependencies:

```bash
pip install -r requirements.txt
```

4. Configure environment variables:

```bash
cp .env.example .env
```

The `.env.example` is pre-configured for Docker. Optionally generate a secure SECRET_KEY:

```bash
openssl rand -hex 32
```

5. Run the application:

```bash
uvicorn main:app --reload
```

### Without Docker

If you have PostgreSQL installed locally:

1. Create a database:

```sql
CREATE DATABASE fastapi_db;
CREATE USER fastapi_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE fastapi_db TO fastapi_user;
```

2. Update `.env` with your database credentials

3. Install dependencies and run:

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## Running the Application

```bash
uvicorn main:app --reload
```

The API will be available at:

- API: http://localhost:8000
- Interactive docs (Swagger): http://localhost:8000/docs
- Alternative docs (ReDoc): http://localhost:8000/redoc
- pgAdmin (if using Docker): http://localhost:5050

## Docker Commands

```bash
# Start containers
docker-compose up -d

# Stop containers
docker-compose down

# View logs
docker-compose logs -f postgres

# Restart containers
docker-compose restart

# Remove all data (volumes)
docker-compose down -v
```

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

### Authentication Examples

#### Register a New User

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "johndoe",
    "password": "securepassword123",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

#### Login (Get JWT Token)

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=johndoe&password=securepassword123"
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

#### Access Protected Route

```bash
curl -X GET "http://localhost:8000/api/v1/users/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### Refresh Token

```bash
curl -X POST "http://localhost:8000/api/v1/auth/refresh" \
  -H "Content-Type: application/json" \
  -d '{
    "refresh_token": "YOUR_REFRESH_TOKEN"
  }'
```

### Product Examples

#### Create a Product

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

- Email verification system
- Password reset functionality
- Rate limiting
- Caching (Redis)
- Unit and integration tests
- Docker containerization
- CI/CD pipeline
- API versioning (v2)
- WebSocket support
