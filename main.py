from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
from app.routers import products_router
from app.core.config import settings
from app.core.builders import ExceptionBuilder
from app.middleware import RequestLoggingMiddleware, ErrorHandlerMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    # Startup
    print("\n" + "=" * 60)
    print(f"🚀 {settings.APP_NAME} v{settings.APP_VERSION}")
    print("=" * 60)
    print("✅ Server is running!")
    print("\n📚 API Documentation:")
    print("   → Swagger UI:  http://localhost:8000/docs")
    print("   → ReDoc:       http://localhost:8000/redoc")
    print("\n🌐 Available Endpoints:")
    print("   → Root:        http://localhost:8000/")
    print("   → Health:      http://localhost:8000/health")
    print("   → Products:    http://localhost:8000/api/v1/products")
    print("\n" + "=" * 60 + "\n")

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

app.include_router(products_router)


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

