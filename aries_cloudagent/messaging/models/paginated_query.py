"""Class for paginated query parameters."""

from typing import Tuple

from aiohttp.web import BaseRequest
from marshmallow import fields
from marshmallow.validate import OneOf

from ...messaging.models.openapi import OpenAPISchema
from ...storage.base import DEFAULT_PAGE_SIZE, MAXIMUM_PAGE_SIZE


class PaginatedQuerySchema(OpenAPISchema):
    """Parameters for paginated queries."""

    limit = fields.Int(
        required=False,
        load_default=DEFAULT_PAGE_SIZE,
        validate=lambda x: x > 0 and x <= MAXIMUM_PAGE_SIZE,
        metadata={"description": "Number of results to return", "example": 50},
        error_messages={
            "validator_failed": (
                "Value must be greater than 0 and "
                f"less than or equal to {MAXIMUM_PAGE_SIZE}"
            )
        },
    )
    offset = fields.Int(
        required=False,
        load_default=0,
        validate=lambda x: x >= 0,
        metadata={"description": "Offset for pagination", "example": 0},
        error_messages={"validator_failed": "Value must be 0 or greater"},
    )
    order_by = fields.Str(
        required=False,
        load_default=None,
        dump_only=True,  # Hide from schema by making it dump-only
        load_only=True,  # Ensure it can still be loaded/validated
        validate=OneOf(["id"]),  # Example of possible fields
        metadata={"description": "Order results in descending order if true"},
        error_messages={"validator_failed": "Ordering only support for column `id`"},
    )
    descending = fields.Bool(
        required=False,
        load_default=False,
        metadata={"description": "Order results in descending order if true"},
    )


def get_limit_offset(request: BaseRequest) -> Tuple[int, int]:
    """Read the limit and offset query parameters from a request as ints, with defaults.

    Args:
        request: aiohttp request object

    Returns:
        A tuple of the limit and offset values
    """

    limit = int(request.query.get("limit", DEFAULT_PAGE_SIZE))
    offset = int(request.query.get("offset", 0))
    return limit, offset
