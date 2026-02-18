import functools
import time
import logging
from typing import Callable, Any

logger = logging.getLogger(__name__)


def catch_exceptions(exception_type: type[Exception] = Exception, reraise: bool = False):
    """Decorator to catch and handle exceptions"""

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return await func(*args, **kwargs)
            except exception_type as e:
                logger.error(f"Exception in {func.__name__}: {str(e)}")
                if reraise:
                    raise
                return None

        @functools.wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except exception_type as e:
                logger.error(f"Exception in {func.__name__}: {str(e)}")
                if reraise:
                    raise
                return None

        # Return appropriate wrapper based on whether function is async
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator


def log_execution_time(func: Callable) -> Callable:
    """Decorator to log function execution time"""

    @functools.wraps(func)
    async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.time()
        try:
            result = await func(*args, **kwargs)
            return result
        finally:
            execution_time = time.time() - start_time
            logger.info(
                f"{func.__name__} executed in {execution_time:.4f} seconds"
            )

    @functools.wraps(func)
    def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            execution_time = time.time() - start_time
            logger.info(
                f"{func.__name__} executed in {execution_time:.4f} seconds"
            )

    # Return appropriate wrapper based on whether function is async
    import asyncio
    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper


def validate_required_fields(fields: list[str]):
    """Decorator to validate required fields in request data"""

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            # Check if request data is in kwargs
            request_data = kwargs.get("request_data") or (
                args[0] if args else None
            )

            if request_data:
                if isinstance(request_data, dict):
                    missing_fields = [
                        field for field in fields if field not in request_data
                    ]
                    if missing_fields:
                        raise ValueError(
                            f"Missing required fields: {', '.join(missing_fields)}"
                        )

            return await func(*args, **kwargs)

        @functools.wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            # Check if request data is in kwargs
            request_data = kwargs.get("request_data") or (
                args[0] if args else None
            )

            if request_data:
                if isinstance(request_data, dict):
                    missing_fields = [
                        field for field in fields if field not in request_data
                    ]
                    if missing_fields:
                        raise ValueError(
                            f"Missing required fields: {', '.join(missing_fields)}"
                        )

            return func(*args, **kwargs)

        # Return appropriate wrapper
        import asyncio
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator


def cache_result(ttl_seconds: int = 300):
    """Simple decorator to cache function results"""

    def decorator(func: Callable) -> Callable:
        cache = {}

        @functools.wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            # Create cache key from args and kwargs
            cache_key = f"{func.__name__}_{str(args)}_{str(kwargs)}"

            # Check if result is in cache and not expired
            if cache_key in cache:
                result, timestamp = cache[cache_key]
                if time.time() - timestamp < ttl_seconds:
                    logger.debug(f"Cache hit for {func.__name__}")
                    return result

            # Execute function and cache result
            result = await func(*args, **kwargs)
            cache[cache_key] = (result, time.time())
            return result

        @functools.wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            # Create cache key from args and kwargs
            cache_key = f"{func.__name__}_{str(args)}_{str(kwargs)}"

            # Check if result is in cache and not expired
            if cache_key in cache:
                result, timestamp = cache[cache_key]
                if time.time() - timestamp < ttl_seconds:
                    logger.debug(f"Cache hit for {func.__name__}")
                    return result

            # Execute function and cache result
            result = func(*args, **kwargs)
            cache[cache_key] = (result, time.time())
            return result

        # Return appropriate wrapper
        import asyncio
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator
