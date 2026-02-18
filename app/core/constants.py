from enum import Enum
from typing import Final


class HttpStatus(str, Enum):
    OK = "200"
    CREATED = "201"
    NO_CONTENT = "204"
    BAD_REQUEST = "400"
    NOT_FOUND = "404"
    UNPROCESSABLE_ENTITY = "422"
    INTERNAL_SERVER_ERROR = "500"


class ResponseMessage(str, Enum):
    SUCCESS = "Success"
    CREATED = "Resource created successfully"
    UPDATED = "Resource updated successfully"
    DELETED = "Resource deleted successfully"
    NOT_FOUND = "Resource not found"
    BAD_REQUEST = "Bad request"
    INTERNAL_ERROR = "Internal server error"


class APIErrors(str, Enum):
    PRODUCT_NOT_FOUND = "PRODUCT_001"
    PRODUCT_INVALID_DATA = "PRODUCT_002"
    PRODUCT_ALREADY_EXISTS = "PRODUCT_003"
    PRODUCT_OUT_OF_STOCK = "PRODUCT_004"


# Pagination constants
DEFAULT_SKIP: Final[int] = 0
DEFAULT_LIMIT: Final[int] = 100
MAX_LIMIT: Final[int] = 100


# API Versioning
API_V1_PREFIX: Final[str] = "/api/v1"
API_V2_PREFIX: Final[str] = "/api/v2"
