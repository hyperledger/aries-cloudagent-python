"""DID INDY routes."""

from http import HTTPStatus

from aiohttp import web
from aiohttp_apispec import docs, request_schema, response_schema
from marshmallow import fields

from ...admin.decorators.auth import tenant_authentication
from ...admin.request_context import AdminRequestContext
from ...did.indy.indy_manager import DidIndyManager
from ...messaging.models.openapi import OpenAPISchema
from ...wallet.error import WalletError


class CreateRequestSchema(OpenAPISchema):
    """Parameters and validators for create DID endpoint."""

    seed = fields.Str(
        required=False,
        metadata={
            "description": (
                "Optional seed to use for DID, Must be enabled in configuration before"
                " use."
            ),
            "example": "000000000000000000000000Trustee1",
        },
    )


class CreateResponseSchema(OpenAPISchema):
    """Response schema for create DID endpoint."""

    did = fields.Str(description="DID created", example="did:indy:DFZgMggBEXcZFVQ2ZBTwdr")
    verkey = fields.Str(
        description="Verification key",
        example="BnSWTUQmdYCewSGFrRUhT6LmKdcCcSzRGqWXMPnEP168",
    )


@docs(tags=["did"], summary="Create an INDY DID")
@request_schema(CreateRequestSchema())
@response_schema(CreateResponseSchema, HTTPStatus.OK)
@tenant_authentication
async def create_indy_did(request: web.BaseRequest):
    """Create a INDY DID."""
    context: AdminRequestContext = request["context"]
    body = await request.json()
    try:
        return web.json_response(
            (await DidIndyManager(context.profile).register(body.get("seed")))
        )
    except WalletError as e:
        raise web.HTTPBadRequest(reason=str(e))


async def register(app: web.Application):
    """Register routes."""
    app.add_routes([web.post("/did/indy/create", create_indy_did)])


def post_process_routes(app: web.Application):
    """Amend swagger API."""
    # Add top-level tags description
    if "tags" not in app._state["swagger_dict"]:
        app._state["swagger_dict"]["tags"] = []
    app._state["swagger_dict"]["tags"].append(
        {
            "name": "did",
            "description": "Endpoints for managing dids",
            "externalDocs": {
                "description": "Specification",
                "url": "https://www.w3.org/TR/did-core/",
            },
        }
    )