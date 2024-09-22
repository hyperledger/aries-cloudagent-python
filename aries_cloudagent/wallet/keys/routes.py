"""Key admin routes."""

import logging

from aiohttp import web
from aiohttp_apispec import docs, request_schema, response_schema
from marshmallow import fields

from ...admin.decorators.auth import tenant_authentication
from ...admin.request_context import AdminRequestContext
from ...messaging.models.openapi import OpenAPISchema
from .manager import MultikeyManager, MultikeyManagerError
from ...wallet.error import WalletDuplicateError, WalletNotFoundError
from ..base import BaseWallet

LOGGER = logging.getLogger(__name__)


class CreateKeyRequestSchema(OpenAPISchema):
    """Request schema for creating a new key."""

    alg = fields.Str(
        required=False,
        metadata={
            "description": "Which key algorithm to use.",
            "example": "ed25519",
        },
    )

    seed = fields.Str(
        required=False,
        metadata={
            "description": "Optional seed to generate the key pair. \
                Must enable insecure wallet mode.",
            "example": "00000000000000000000000000000000",
        },
    )

    kid = fields.Str(
        required=False,
        metadata={
            "description": "Optional kid to bind to the keypair, \
                such as a verificationMethod.",
            "example": "did:web:example.com#key-01",
        },
    )


class CreateKeyResponseSchema(OpenAPISchema):
    """Response schema from creating a new key."""

    multikey = fields.Str(
        metadata={
            "description": "The Public Key Multibase format (multikey)",
            "example": "z6MkgKA7yrw5kYSiDuQFcye4bMaJpcfHFry3Bx45pdWh3s8i",
        },
    )

    kid = fields.Str(
        metadata={
            "description": "The associated kid",
            "example": "did:web:example.com#key-01",
        },
    )


class UpdateKeyRequestSchema(OpenAPISchema):
    """Request schema for updating an existing key pair."""

    multikey = fields.Str(
        required=True,
        metadata={
            "description": "Multikey of the key pair to update",
            "example": "z6MkgKA7yrw5kYSiDuQFcye4bMaJpcfHFry3Bx45pdWh3s8i",
        },
    )

    kid = fields.Str(
        required=True,
        metadata={
            "description": "New kid to bind to the key pair, \
                such as a verificationMethod.",
            "example": "did:web:example.com#key-02",
        },
    )


class UpdateKeyResponseSchema(OpenAPISchema):
    """Response schema from updating an existing key pair."""

    multikey = fields.Str(
        metadata={
            "description": "The Public Key Multibase format (multikey)",
            "example": "z6MkgKA7yrw5kYSiDuQFcye4bMaJpcfHFry3Bx45pdWh3s8i",
        },
    )

    kid = fields.Str(
        metadata={
            "description": "The associated kid",
            "example": "did:web:example.com#key-02",
        },
    )


class FetchKeyResponseSchema(OpenAPISchema):
    """Response schema from updating an existing key pair."""

    multikey = fields.Str(
        metadata={
            "description": "The Public Key Multibase format (multikey)",
            "example": "z6MkgKA7yrw5kYSiDuQFcye4bMaJpcfHFry3Bx45pdWh3s8i",
        },
    )

    kid = fields.Str(
        metadata={
            "description": "The associated kid",
            "example": "did:web:example.com#key-01",
        },
    )


@docs(tags=["wallet"], summary="Fetch key info.")
@response_schema(FetchKeyResponseSchema, 200, description="")
@tenant_authentication
async def fetch_key(request: web.BaseRequest):
    """Request handler for fetching a key.

    Args:
        request: aiohttp request object

    """
    context: AdminRequestContext = request["context"]
    multikey = request.match_info["multikey"]
    
    try:
        return web.json_response(
            await MultikeyManager(context).from_multikey(multikey=multikey),
            status=200,
        )

    except (MultikeyManagerError, WalletDuplicateError, WalletNotFoundError) as err:
        return web.json_response({"message": str(err)}, status=400)


@docs(tags=["wallet"], summary="Create a key pair")
@request_schema(CreateKeyRequestSchema())
@response_schema(CreateKeyResponseSchema, 200, description="")
@tenant_authentication
async def create_key(request: web.BaseRequest):
    """Request handler for creating a new key pair in the wallet.

    Args:
        request: aiohttp request object

    Returns:
        The Public Key Multibase format (multikey)

    """
    context: AdminRequestContext = request["context"]
    body = await request.json()

    seed = body.get("seed") or None
    kid = body.get("kid") or None
    alg = body.get("alg") or "ed25519"
    try:
        return web.json_response(
            await MultikeyManager(context).create(seed=seed, kid=kid, alg=alg),
            status=201,
        )
    except (MultikeyManagerError, WalletDuplicateError, WalletNotFoundError) as err:
        return web.json_response({"message": str(err)}, status=400)

    async with context.session() as session:
        wallet: BaseWallet | None = session.inject_or(BaseWallet)
        
        if kid:
            if await wallet.get_key_by_kid(kid=kid):
                raise web.HTTPBadRequest(
                    reason=f"kid {kid} already used in wallet."
                )
                    
        key_type = ALG_MAPPINGS[alg]["key_type"]
        key_info = await wallet.create_key(key_type=key_type, seed=seed, kid=kid)
        
        return web.json_response(
            {
                "kid": key_info.kid,
                "multikey": verkey_to_multikey(key_info.verkey),
            },
            status=200,
        )

    # try:
    #     key_info = await MultikeyManager(context).create(
    #         seed=seed,
    #         kid=kid,
    #     )
    #     return web.json_response(key_info, status=201)


@docs(tags=["wallet"], summary="Update a key pair's kid")
@request_schema(UpdateKeyRequestSchema())
@response_schema(UpdateKeyResponseSchema, 200, description="")
@tenant_authentication
async def update_key(request: web.BaseRequest):
    """Request handler for creating a new key pair in the wallet.

    Args:
        request: aiohttp request object

    Returns:
        The Public Key Multibase format (multikey)

    """
    context: AdminRequestContext = request["context"]
    body = await request.json()

    multikey = body.get("multikey")
    kid = body.get("kid")

    try:
        return web.json_response(
            await MultikeyManager(context).update(
                multikey=multikey,
                kid=kid,
            ), 
            status=200
        )
    except (MultikeyManagerError, WalletDuplicateError, WalletNotFoundError) as err:
        return web.json_response({"message": str(err)}, status=400)


async def register(app: web.Application):
    """Register routes."""

    app.add_routes(
        [
            web.get("/wallet/keys/{multikey}", fetch_key, allow_head=False),
            web.post("/wallet/keys", create_key),
            web.put("/wallet/keys", update_key),
        ]
    )