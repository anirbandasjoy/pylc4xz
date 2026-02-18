from app.routers.products import router as products_router
from app.routers.auth import router as auth_router
from app.routers.users import router as users_router

__all__ = ["products_router", "auth_router", "users_router"]
