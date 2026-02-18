from app.core.config import settings, Settings
from app.core.constants import (
    HttpStatus,
    ResponseMessage,
    APIErrors,
    DEFAULT_SKIP,
    DEFAULT_LIMIT,
    MAX_LIMIT,
    API_V1_PREFIX,
)
from app.core.exceptions import (
    BaseAPIException,
    NotFoundException,
    BadRequestException,
    UnprocessableEntityException,
    ConflictException,
    ProductNotFoundException,
    ProductInvalidDataException,
    ProductAlreadyExistsException,
)
from app.core.responses import (
    ApiResponse,
    PaginatedResponse,
    PaginationParams,
    success_response,
    created_response,
    no_content_response,
    paginated_response,
)
from app.core.dependencies import (
    get_pagination_params,
    get_product_id,
    get_search_query,
    PaginationDep,
    SearchQueryDep,
    ProductIdDep,
)
from app.core.builders import (
    ResponseBuilder,
    PaginationBuilder,
    ExceptionBuilder,
)

__all__ = [
    # Config
    "settings",
    "Settings",
    # Constants
    "HttpStatus",
    "ResponseMessage",
    "APIErrors",
    "DEFAULT_SKIP",
    "DEFAULT_LIMIT",
    "MAX_LIMIT",
    "API_V1_PREFIX",
    # Exceptions
    "BaseAPIException",
    "NotFoundException",
    "BadRequestException",
    "UnprocessableEntityException",
    "ConflictException",
    "ProductNotFoundException",
    "ProductInvalidDataException",
    "ProductAlreadyExistsException",
    # Responses
    "ApiResponse",
    "PaginatedResponse",
    "PaginationParams",
    "success_response",
    "created_response",
    "no_content_response",
    "paginated_response",
    # Dependencies
    "get_pagination_params",
    "get_product_id",
    "get_search_query",
    "PaginationDep",
    "SearchQueryDep",
    "ProductIdDep",
    # Builders
    "ResponseBuilder",
    "PaginationBuilder",
    "ExceptionBuilder",
]
