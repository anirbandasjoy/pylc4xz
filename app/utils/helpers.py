from typing import Tuple


def normalize_string(text: str) -> str:
    """Normalize string by stripping and converting to lowercase"""
    return text.strip().lower() if text else ""


def calculate_pagination(
    total: int, skip: int, limit: int
) -> Tuple[int, bool, bool]:
    """Calculate pagination metadata

    Args:
        total: Total number of items
        skip: Number of items to skip
        limit: Number of items per page

    Returns:
        Tuple of (current_page, has_next, has_prev)
    """
    current_page = (skip // limit) + 1 if limit else 1
    total_pages = (total + limit - 1) // limit if limit else 0

    has_next = current_page < total_pages
    has_prev = current_page > 1

    return current_page, has_next, has_prev


def format_price(price: float, currency: str = "USD") -> str:
    """Format price with currency symbol"""
    return f"{price:.2f} {currency}"


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to maximum length"""
    if not text or len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def build_query_params(base_url: str, params: dict) -> str:
    """Build URL with query parameters"""
    if not params:
        return base_url

    query_string = "&".join(f"{k}={v}" for k, v in params.items() if v is not None)
    return f"{base_url}?{query_string}" if query_string else base_url


def extract_error_message(error: Exception) -> str:
    """Extract error message from exception"""
    if hasattr(error, "detail"):
        return str(error.detail)
    return str(error)
