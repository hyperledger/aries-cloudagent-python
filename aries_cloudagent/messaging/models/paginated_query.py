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
        load_default="id",
        validate=OneOf(["id"]),  # only one possible column supported in askar
        metadata={
            "description": (
                'The column to order results by. Only "id" is currently supported.'
            )
        },
        error_messages={"validator_failed": '`order_by` only supports column "id"'},
    )
    descending = fields.Bool(
        required=False,
        load_default=False,
        metadata={"description": "Order results in descending order if true"},
    )


def get_paginated_query_params(request: BaseRequest) -> Tuple[int, int, str, bool]:
    """Read the limit, offset, order_by, and descending query parameters from a request.

    Args:
        request: aiohttp request object.

    Returns:
        A tuple containing:
        - limit (int): The number of results to return, defaulting to DEFAULT_PAGE_SIZE.
        - offset (int): The offset for pagination, defaulting to 0.
        - order_by (str): The field by which to order results, defaulting to "id".
        - descending (bool): Order results in descending order; defaults to False.
    """

    limit = int(request.query.get("limit", DEFAULT_PAGE_SIZE))
    offset = int(request.query.get("offset", 0))
    order_by = request.query.get("order_by", "id")
    descending = bool(request.query.get("descending", False))
    return limit, offset, order_by, descending
