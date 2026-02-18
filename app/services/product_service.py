from typing import Optional
from app.services.base_service import BaseService
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.core.exceptions import ProductNotFoundException


class ProductService(BaseService[ProductResponse]):
    """Service for managing products"""

    def __init__(self):
        super().__init__()
        self._initialize_demo_data()

    def _to_entity(self, data: dict) -> ProductResponse:
        """Convert dict to ProductResponse"""
        return ProductResponse(**data)

    def _to_dict(self, entity: ProductResponse) -> dict:
        """Convert ProductResponse to dict"""
        return entity.model_dump()

    def _initialize_demo_data(self) -> None:
        """Initialize demo products"""
        demo_products = [
            {
                "id": 1,
                "name": "Laptop",
                "description": "High-performance laptop for professionals",
                "price": 1299.99,
                "category": "Electronics",
                "stock": 15,
                "is_active": True,
            },
            {
                "id": 2,
                "name": "Wireless Mouse",
                "description": "Ergonomic wireless mouse with precision tracking",
                "price": 29.99,
                "category": "Electronics",
                "stock": 50,
                "is_active": True,
            },
            {
                "id": 3,
                "name": "Mechanical Keyboard",
                "description": "RGB mechanical keyboard with blue switches",
                "price": 89.99,
                "category": "Electronics",
                "stock": 25,
                "is_active": True,
            },
            {
                "id": 4,
                "name": "HD Monitor 27\"",
                "description": "27-inch Full HD monitor with IPS panel",
                "price": 249.99,
                "category": "Electronics",
                "stock": 10,
                "is_active": True,
            },
            {
                "id": 5,
                "name": "USB-C Hub",
                "description": "7-in-1 USB-C hub with power delivery",
                "price": 49.99,
                "category": "Accessories",
                "stock": 30,
                "is_active": True,
            },
            {
                "id": 6,
                "name": "Webcam 1080p",
                "description": "Full HD webcam with auto-focus",
                "price": 79.99,
                "category": "Electronics",
                "stock": 20,
                "is_active": True,
            },
            {
                "id": 7,
                "name": "Desk Lamp LED",
                "description": "Adjustable LED desk lamp with touch control",
                "price": 39.99,
                "category": "Office",
                "stock": 40,
                "is_active": True,
            },
            {
                "id": 8,
                "name": "Noise-Cancelling Headphones",
                "description": "Over-ear headphones with active noise cancellation",
                "price": 199.99,
                "category": "Audio",
                "stock": 12,
                "is_active": True,
            },
        ]

        for product in demo_products:
            self._db[product["id"]] = product
            self._next_id = max(self._next_id, product["id"] + 1)

    def get_by_category(
        self, category: str, skip: int = 0, limit: int = 100
    ) -> tuple[list[dict], int]:
        """Get products by category"""
        return self.get_all(skip=skip, limit=limit, category=category)

    def get_active_products(
        self, skip: int = 0, limit: int = 100
    ) -> tuple[list[dict], int]:
        """Get only active products"""
        return self.get_all(skip=skip, limit=limit, is_active=True)

    def search_products(
        self, query: str, skip: int = 0, limit: int = 100
    ) -> tuple[list[dict], int]:
        """Search products by name, description, or category"""
        return self.search(
            query=query,
            fields=["name", "description", "category"],
            skip=skip,
            limit=limit,
        )

    def get_or_404(self, product_id: int) -> dict:
        """Get product by ID or raise 404 exception"""
        product = self.get_by_id(product_id)
        if not product:
            raise ProductNotFoundException(product_id=product_id)
        return product

    def update_stock(self, product_id: int, quantity: int) -> Optional[dict]:
        """Update product stock"""
        product = self.get_by_id(product_id)
        if not product:
            return None

        product["stock"] = quantity
        return product

    def decrease_stock(self, product_id: int, quantity: int) -> Optional[dict]:
        """Decrease product stock"""
        product = self.get_by_id(product_id)
        if not product:
            return None

        if product["stock"] < quantity:
            return None

        product["stock"] -= quantity
        return product


# Singleton instance
product_service = ProductService()
