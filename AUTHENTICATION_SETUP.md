# Authentication System Setup Guide

## Overview

This FastAPI application now includes a complete JWT-based authentication system with the following features:

- **User Registration & Login** with OAuth 2.0 compliance
- **JWT Token Authentication** with access and refresh tokens
- **Password Hashing** using Bcrypt
- **Role-Based Access Control** (Admin, Moderator, User)
- **Complete User Management** (CRUD operations)
- **PostgreSQL Database** with SQLModel

## Installation Steps

### Option 1: Using Docker (Recommended)

#### 1. Start PostgreSQL with Docker Compose

```bash
# Start PostgreSQL and pgAdmin containers
docker-compose up -d

# Check if containers are running
docker-compose ps

# View logs
docker-compose logs -f postgres
```

This will start:
- **PostgreSQL** on port `5432`
  - User: `fastapi_user`
  - Password: `fastapi_password`
  - Database: `fastapi_db`
- **pgAdmin** on port `5050` (optional web-based database manager)
  - Email: `admin@example.com`
  - Password: `admin`
  - URL: http://localhost:5050

#### 2. Stop Containers

```bash
# Stop all containers
docker-compose down

# Stop and remove volumes (deletes all data!)
docker-compose down -v
```

### Option 2: Manual PostgreSQL Setup

If you prefer to use a locally installed PostgreSQL:

```sql
CREATE DATABASE fastapi_db;
CREATE USER fastapi_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE fastapi_db TO fastapi_user;
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

Required packages:
- `sqlmodel` - Database ORM
- `python-jose[cryptography]` - JWT token handling
- `passlib[bcrypt]` - Password hashing
- `asyncpg` - Async PostgreSQL driver
- `psycopg2-binary` - PostgreSQL adapter

### 4. Configure Environment Variables

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

**For Docker users** - The `.env.example` is already configured with Docker credentials:
```env
DATABASE_URL=postgresql://fastapi_user:fastapi_password@localhost:5432/fastapi_db
```

**For manual PostgreSQL users** - Update the DATABASE_URL:
```env
DATABASE_URL=postgresql://fastapi_user:your_actual_password@localhost:5432/fastapi_db
```

**Generate a secure SECRET_KEY for JWT:**
```bash
openssl rand -hex 32
```

Update the SECRET_KEY in your `.env` file with the generated value.

### 5. Run the Application

### 3. Configure Environment Variables

Copy `.env.example` to `.env` and update:

```bash
cp .env.example .env
```

Update these values in `.env`:

```env
# Database
DATABASE_URL=postgresql://fastapi_user:your_password@localhost:5432/fastapi_db

# JWT (IMPORTANT: Generate a secure key!)
SECRET_KEY=your-secret-key-change-this-in-production
```

Generate a secure SECRET_KEY:

```bash
openssl rand -hex 32
```

### 4. Run the Application

```bash
uvicorn main:app --reload
```

The application will automatically create the required tables on startup.

## API Documentation

Visit http://localhost:8000/docs for interactive API documentation.

## Authentication Flow

### 1. Register a User

```bash
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "SecurePass123!",
  "first_name": "John",
  "last_name": "Doe"
}
```

### 2. Login

```bash
POST /api/v1/auth/login
Content-Type: application/x-www-form-urlencoded

username=johndoe&password=SecurePass123!
```

Response:
```json
{
  "access_token": "eyJhbG...",
  "refresh_token": "eyJhbG...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### 3. Access Protected Routes

```bash
GET /api/v1/users/me
Authorization: Bearer YOUR_ACCESS_TOKEN
```

### 4. Refresh Token

```bash
POST /api/v1/auth/refresh
Content-Type: application/json

{
  "refresh_token": "YOUR_REFRESH_TOKEN"
}
```

## User Roles

- **USER**: Regular user (default)
- **MODERATOR**: Can view and manage users
- **ADMIN**: Full access including user management

## Protected Endpoints

### Public Endpoints
- `POST /api/v1/auth/register` - Register
- `POST /api/v1/auth/login` - Login
- `GET /` - Root
- `GET /health` - Health check

### Authenticated Endpoints (Any User)
- `GET /api/v1/auth/me` - Get current user
- `PUT /api/v1/auth/change-password` - Change password
- `GET /api/v1/users/me` - Get my profile
- `PUT /api/v1/users/me` - Update my profile

### Admin/Moderator Endpoints
- `GET /api/v1/users/` - List all users
- `GET /api/v1/users/{user_id}` - Get user by ID

### Admin Only Endpoints
- `PUT /api/v1/users/{user_id}` - Update any user
- `DELETE /api/v1/users/{user_id}` - Delete user
- `PATCH /api/v1/users/{user_id}/activate` - Activate user
- `PATCH /api/v1/users/{user_id}/deactivate` - Deactivate user
- `PATCH /api/v1/users/{user_id}/verify` - Verify user
- `GET /api/v1/users/stats/count` - User statistics

## Security Features

1. **Password Hashing**: Bcrypt with salt
2. **JWT Tokens**: HS256 algorithm
3. **Token Expiration**: Access tokens (30 min), Refresh tokens (7 days)
4. **Role-Based Access**: Three-tier permission system
5. **Account Status**: Active/inactive user accounts
6. **Email Verification**: Verify/unverify users

## Database Schema

### Users Table

| Column        | Type         | Description                     |
|---------------|--------------|---------------------------------|
| id            | int          | Primary key                     |
| email         | varchar(255) | Unique email                    |
| username      | varchar(100) | Unique username                 |
| hashed_password | varchar(255)| Bcrypt password hash            |
| first_name    | varchar(100) | Optional first name             |
| last_name     | varchar(100) | Optional last name              |
| role          | enum         | USER, MODERATOR, ADMIN          |
| is_active     | boolean      | Account active status           |
| is_verified   | boolean      | Email verification status       |
| created_at    | datetime     | Account creation timestamp      |
| updated_at    | datetime     | Last update timestamp           |
| last_login    | datetime     | Last login timestamp            |

## Creating an Admin User

After registering a user, you can make them an admin directly in the database:

```sql
UPDATE users SET role = 'admin' WHERE email = 'admin@example.com';
```

Or create an admin user programmatically (you can add this to a startup script).

## Troubleshooting

### Docker Issues

#### Container not starting

```bash
# Check container status
docker-compose ps

# View logs
docker-compose logs postgres

# Restart containers
docker-compose restart
```

#### Port already in use

If port 5432 is already in use:

```bash
# Check what's using the port
sudo lsof -i :5432

# Or change the port mapping in docker-compose.yml
# Change "5432:5432" to "5433:5432" (external:internal)
```

#### Connect to PostgreSQL inside container

```bash
# Access PostgreSQL directly
docker exec -it fastapi_postgres psql -U fastapi_user -d fastapi_db

# Or run commands
docker exec -it fastapi_postgres psql -U fastapi_user -d fastapi_db -c "SELECT * FROM users;"
```

### Database Connection Error

**For Docker users:**

```bash
# Check if container is running
docker-compose ps

# Test connection
docker exec -it fastapi_postgres psql -U fastapi_user -d fastapi_db -c "SELECT 1;"
```

**For manual PostgreSQL users:**

```bash
# Check PostgreSQL status
sudo service postgresql status

# Start PostgreSQL if not running
sudo service postgresql start

# Test connection
psql -U fastapi_user -d fastapi_db -h localhost
```

### Invalid Token Error

- Check that the SECRET_KEY is the same for login and verification
- Ensure the token hasn't expired (default: 30 minutes)
- Verify the token format: `Authorization: Bearer <token>`

### Import Errors

Run:
```bash
pip install -r requirements.txt
```

### Reset Everything (Docker)

⚠️ **WARNING: This will delete all data!**

```bash
# Stop and remove all containers and volumes
docker-compose down -v

# Rebuild and start
docker-compose up -d

# Reinitialize the database (tables will be created on app start)
```

## Quick Start Commands

```bash
# 1. Start PostgreSQL (Docker)
docker-compose up -d

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Copy environment file
cp .env.example .env

# 4. Generate SECRET_KEY (optional, .env.example has a default)
openssl rand -hex 32

# 5. Run the FastAPI application
uvicorn main:app --reload
```

Now your API is running at:
- **API**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs
- **pgAdmin** (optional): http://localhost:5050

## Next Steps

1. **Email Verification**: Implement email sending for verification
2. **Password Reset**: Add forgot password functionality
3. **Rate Limiting**: Add rate limiting to prevent brute force attacks
4. **Two-Factor Authentication**: Add 2FA for enhanced security
5. **Session Management**: Add token blacklisting for logout
