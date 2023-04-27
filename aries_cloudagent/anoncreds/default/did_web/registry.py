"""DID Web Registry"""
import re
from typing import Optional, Pattern

from ....config.injection_context import InjectionContext
from ....core.profile import Profile
from ...models.anoncreds_cred_def import (
    GetCredDefResult,
)
from ...models.anoncreds_revocation import (
    GetRevListResult,
    AnonCredsRegistryGetRevocationRegistryDefinition,
    RevRegDef,
    RevList,
    RevListResult,
)
from ...models.anoncreds_schema import GetSchemaResult
from ...base import BaseAnonCredsRegistrar, BaseAnonCredsResolver
from ...models.anoncreds_cred_def import CredDef, CredDefResult, GetCredDefResult
from ...models.anoncreds_revocation import (
    AnonCredsRegistryGetRevocationRegistryDefinition,
    GetRevListResult,
    RevRegDef,
    RevRegDefResult,
    RevList,
    RevListResult,
)
from ...models.anoncreds_schema import AnonCredsSchema, GetSchemaResult, SchemaResult


class DIDWebRegistry(BaseAnonCredsResolver, BaseAnonCredsRegistrar):
    """DIDWebRegistry"""

    def __init__(self):
        self._supported_identifiers_regex = re.compile(
            r"^did:web:[a-z0-9]+(?:\.[a-z0-9]+)*(?::\d+)?(?:\/[^#\s]*)?(?:#.*)?\s*$"
        )

    @property
    def supported_identifiers_regex(self) -> Pattern:
        return self._supported_identifiers_regex
        # TODO: fix regex (too general)

    async def setup(self, context: InjectionContext):
        """Setup."""
        print("Successfully registered DIDWebRegistry")

    async def get_schema(self, profile, schema_id: str) -> GetSchemaResult:
        """Get a schema from the registry."""
        raise NotImplementedError()

    async def register_schema(
        self,
        profile: Profile,
        schema: AnonCredsSchema,
        options: Optional[dict] = None,
    ) -> SchemaResult:
        """Register a schema on the registry."""
        raise NotImplementedError()

    async def get_credential_definition(
        self, profile: Profile, credential_definition_id: str
    ) -> GetCredDefResult:
        """Get a credential definition from the registry."""
        raise NotImplementedError()

    async def register_credential_definition(
        self,
        profile: Profile,
        schema: GetSchemaResult,
        credential_definition: CredDef,
        options: Optional[dict] = None,
    ) -> CredDefResult:
        """Register a credential definition on the registry."""
        raise NotImplementedError()

    async def get_revocation_registry_definition(
        self, profile: Profile, revocation_registry_id: str
    ) -> AnonCredsRegistryGetRevocationRegistryDefinition:
        """Get a revocation registry definition from the registry."""
        raise NotImplementedError()

    async def register_revocation_registry_definition(
        self,
        profile: Profile,
        revocation_registry_definition: RevRegDef,
        options: Optional[dict] = None,
    ) -> RevRegDefResult:
        """Register a revocation registry definition on the registry."""
        raise NotImplementedError()

    async def get_revocation_list(
        self, profile: Profile, revocation_registry_id: str, timestamp: int
    ) -> GetRevListResult:
        """Get a revocation list from the registry."""
        raise NotImplementedError()

    async def register_revocation_list(
        self,
        profile: Profile,
        rev_reg_def: RevRegDef,
        rev_list: RevList,
        options: Optional[dict] = None,
    ) -> RevListResult:
        """Register a revocation list on the registry."""
        raise NotImplementedError()

    async def update_revocation_list(
        self,
        profile: Profile,
        rev_reg_def: RevRegDef,
        prev_list: RevList,
        curr_list: RevList,
        options: Optional[dict] = None,
    ) -> RevListResult:
        """Update a revocation list on the registry."""
        raise NotImplementedError()
