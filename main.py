from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
from app.routers import products_router, auth_router, users_router
from app.core.config import settings
from app.core.builders import ExceptionBuilder
from app.core.database import init_db
from app.middleware import RequestLoggingMiddleware, ErrorHandlerMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    # Startup
    print("\n" + "=" * 60)
    print(f"🚀 {settings.APP_NAME} v{settings.APP_VERSION}")
    print("=" * 60)
    print("✅ Server is running!")

    # Parse database URL for display
    import re
    db_url = settings.DATABASE_URL
    # Match postgresql://user:password@host:port/database
    match = re.match(r'postgresql://[^:]+:[^@]+@([^:]+):(\d+)/(.+)', db_url)
    if match:
        db_host, db_port, db_name = match.groups()
        print("\n🗄️  Database Connection:")
        print(f"   → Host:     {db_host}")
        print(f"   → Port:     {db_port}")
        print(f"   → Database: {db_name}")
    else:
        print(f"\n🗄️  Database: {db_url}")

    print("\n📚 API Documentation:")
    print("   → Swagger UI:  http://localhost:8000/docs")
    print("   → ReDoc:       http://localhost:8000/redoc")
    print("\n🌐 Available Endpoints:")
    print("   → Root:        http://localhost:8000/")
    print("   → Health:      http://localhost:8000/health")
    print("   → Products:    http://localhost:8000/api/v1/products")
    print("   → Auth:        http://localhost:8000/api/v1/auth")
    print("   → Users:       http://localhost:8000/api/v1/users")
    print("\n" + "=" * 60 + "\n")

    # Initialize database
    print("🔄 Initializing database tables...")
    await init_db()
    print("✅ Database connected and ready!")

    yield

    # Shutdown
    print("\n👋 Server shutting down...\n")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="A well-structured FastAPI application with product CRUD operations",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add custom middleware
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(ErrorHandlerMiddleware)

# Include routers with API v1 prefix
app.include_router(products_router, prefix=settings.API_V1_PREFIX)
app.include_router(auth_router, prefix=settings.API_V1_PREFIX)
app.include_router(users_router, prefix=settings.API_V1_PREFIX)


@app.get("/", tags=["root"])
def root():
    return {
        "message": "Welcome to Product API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
    }


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "healthy"}


@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    """Global 404 exception handler for unmatched routes"""
    return ExceptionBuilder.route_not_found(
        path=request.url.path,
        method=request.method,
    )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )

