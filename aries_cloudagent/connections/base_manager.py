"""
Class to provide some common utilities.

For Connection, DIDExchange and OutOfBand Manager.
"""

import logging

from typing import Sequence, Tuple, List

from aries_cloudagent.resolver.base import ResolverError
from aries_cloudagent.resolver.did_resolver import DIDResolver
from ..core.error import BaseError
from ..core.profile import ProfileSession
from ..protocols.connections.v1_0.messages.connection_invitation import (
    ConnectionInvitation,
)
from ..protocols.coordinate_mediation.v1_0.models.mediation_record import (
    MediationRecord,
)
from ..storage.base import BaseStorage
from ..storage.error import StorageNotFoundError
from ..storage.record import StorageRecord
from ..wallet.base import BaseWallet, DIDInfo
from ..wallet.util import did_key_to_naked
from .models.conn_record import ConnRecord
from .models.connection_target import ConnectionTarget
from pydid import (
    DIDDocument,
    DIDDocumentBuilder,
    VerificationSuite,
    options,
    DID,
    DIDCommService,
)
import json


class BaseConnectionManagerError(BaseError):
    """BaseConnectionManager error."""


class BaseConnectionManager:
    """Class to provide utilities regarding connection_targets."""

    RECORD_TYPE_DID_DOC = "did_doc"
    RECORD_TYPE_DID_KEY = "did_key"

    def __init__(self, session: ProfileSession):
        """
        Initialize a BaseConnectionManager.

        Args:
            session: The profile session for this presentation
        """
        self._logger = logging.getLogger(__name__)
        self._session = session

    async def create_did_document(
        self,
        did_info: DIDInfo,
        inbound_connection_id: str = None,
        svc_endpoints: Sequence[str] = None,
        mediation_records: List[MediationRecord] = None,
    ) -> DIDDocument:
        """Create our DID doc for a given DID.

        Args:
            did_info: The DID information (DID and verkey) used in the connection
            inbound_connection_id: The ID of the inbound routing connection to use
            svc_endpoints: Custom endpoints for the DID Document
            mediation_record: The record for mediation that contains routing_keys and
                service endpoint

        Returns:
            The prepared `DIDDocument` instance

        """
        did = did_info.did
        if len(did_info.did.split(":")) < 2:
            did = "did:sov:" + did
        builder = DIDDocumentBuilder(did)
        vmethod = builder.verification_methods.add(
            ident="1",
            suite=VerificationSuite(
                "Ed25519VerificationKey2018", "publicKeyBase58"
            ),  # TODO: remove hardcoding
            material=did_info.verkey,
        )

        router_id = inbound_connection_id
        routing_keys = []
        router_idx = 1
        while router_id:
            # look up routing connection information
            router = await ConnRecord.retrieve_by_id(self._session, router_id)
            if ConnRecord.State.get(router.state) != ConnRecord.State.COMPLETED:
                raise BaseConnectionManagerError(
                    f"Router connection not completed: {router_id}"
                )
            routing_doc, _ = await self.fetch_did_document(router.their_did)
            if not routing_doc.service:
                raise BaseConnectionManagerError(
                    f"No services defined by routing DIDDocument: {router_id}"
                )
            for service in routing_doc.service:
                if not service.endpoint:
                    raise BaseConnectionManagerError(
                        "Routing DIDDocument service has no service endpoint"
                    )
                service_id = self._retrieve_service_key(service)
                if not service_id:
                    raise BaseConnectionManagerError(
                        "Routing DIDDocument service has no recipient key(s)"
                    )

                self.method = builder.verification_methods.add(
                    suite=routing_doc.dereference(service_id[0]).suite,
                    material=routing_doc.dereference(service_id[0]).material,
                    ident=f"routing-{router_idx}",
                )

                rk = self.method
                routing_keys.append(rk)
                svc_endpoints = [service.endpoint]
                break
            router_id = router.inbound_connection_id

        if mediation_records:
            for mediation_record in mediation_records:
                mediator_routing_keys = [
                    builder.verification_methods.add(
                        suite=VerificationSuite(
                            "Ed25519VerificationKey2018", "publicKeyBase58"
                        ),
                        material=key,
                        ident=f"routing-{idx}",
                    )
                    for idx, key in enumerate(mediation_record.routing_keys)
                ]

                routing_keys = [*routing_keys, *mediator_routing_keys]

                svc_endpoints = [mediation_record.endpoint]
        index = 1
        for (endpoint_index, svc_endpoint) in enumerate(svc_endpoints or []):

            builder.services.add_didcomm(
                recipient_keys=[vmethod],
                type_="IndyAgent",  # TODO: remove hardcoding
                routing_keys=routing_keys,
                endpoint=svc_endpoint,
                ident="service-{}".format(index),
            )
            index += 1

        return builder.build()

    async def store_did_document(self, did_doc: DIDDocument):
        """Store a DID document.

        Args:
            did_doc: The `DIDDocument` instance to persist
        """
        assert did_doc.id
        storage: BaseStorage = self._session.inject(BaseStorage)
        try:
            stored_doc, record = await self.fetch_did_document(str(did_doc.id))
        except StorageNotFoundError:
            record = StorageRecord(
                self.RECORD_TYPE_DID_DOC,
                json.dumps(did_doc.serialize()),
                {"did": did_doc.id},
            )
            await storage.add_record(record)
        else:
            await storage.update_record(
                record, did_doc.serialize(), {"did": did_doc.id}
            )
        await self.remove_keys_for_did(did_doc.id)
        for key in did_doc.verification_method:
            if key.controller == did_doc.id:
                await self.add_key_for_did(did_doc.id, key.material)

    async def add_key_for_did(self, did: str, key: str):
        """Store a verkey for lookup against a DID.

        Args:
            did: The DID to associate with this key
            key: The verkey to be added
        """
        record = StorageRecord(self.RECORD_TYPE_DID_KEY, key, {"did": did, "key": key})
        storage = self._session.inject(BaseStorage)
        await storage.add_record(record)

    async def find_did_for_key(self, key: str) -> str:
        """Find the DID previously associated with a key.

        Args:
            key: The verkey to look up
        """
        storage = self._session.inject(BaseStorage)
        record = await storage.find_record(self.RECORD_TYPE_DID_KEY, {"key": key})
        return record.tags["did"]

    async def remove_keys_for_did(self, did: str):
        """Remove all keys associated with a DID.

        Args:
            did: The DID for which to remove keys
        """
        storage = self._session.inject(BaseStorage)
        await storage.delete_all_records(self.RECORD_TYPE_DID_KEY, {"did": did})

    async def resolve_invitation(self, did: str):
        """
        Resolve invitation with the DID Resolver.

        Args:
            did: Document ID to resolve
        """
        # populate recipient keys and endpoint from the ledger
        resolver = self._session.inject(DIDResolver)
        try:
            doc: DIDDocument = await resolver.resolve(self._session.profile, did)
        except ResolverError as error:
            raise BaseConnectionManagerError(
                "Failed to resolve public DID in invitation"
            ) from error

        if not doc.service:
            raise ResolverError("Cannot resolve DID without document services")
        endpoint = doc.service[0].endpoint
        recipient_keys = [
            doc.dereference(url) for url in self._retrieve_service_key(doc.service[0])
        ]
        routing_keys = [
            doc.dereference(url)
            for url in self._retrieve_service_key(doc.service[0], routing=True)
        ]

        return endpoint, recipient_keys, routing_keys

    async def fetch_connection_targets(
        self, connection: ConnRecord
    ) -> Sequence[ConnectionTarget]:
        """Get a list of connection target from a `ConnRecord`.

        Args:
            connection: The connection record (with associated `DIDDocument`)
                used to generate the connection target
        """

        if not connection.my_did:
            self._logger.debug("No local DID associated with connection")
            return None

        wallet = self._session.inject(BaseWallet)
        my_info = await wallet.get_local_did(connection.my_did)

        if (
            ConnRecord.State.get(connection.state)
            in (ConnRecord.State.INVITATION, ConnRecord.State.REQUEST)
            and ConnRecord.Role.get(connection.their_role) is ConnRecord.Role.RESPONDER
        ):
            invitation = await connection.retrieve_invitation(self._session)
            if isinstance(invitation, ConnectionInvitation):  # conn protocol invitation
                if invitation.did:
                    did = invitation.did
                    (
                        endpoint,
                        recipient_keys,
                        routing_keys,
                    ) = await self.resolve_invitation(did)

                else:
                    endpoint = invitation.endpoint
                    recipient_keys = invitation.recipient_keys
                    routing_keys = invitation.routing_keys
            else:  # out-of-band invitation
                if invitation.service_dids:
                    did = invitation.service_dids[0]
                    (
                        endpoint,
                        recipient_keys,
                        routing_keys,
                    ) = await self.resolve_invitation(did)

                else:
                    endpoint = invitation.service_blocks[0].service_endpoint
                    recipient_keys = [
                        did_key_to_naked(k)
                        for k in invitation.service_blocks[0].recipient_keys
                    ]
                    routing_keys = [
                        did_key_to_naked(k)
                        for k in invitation.service_blocks[0].routing_keys
                    ]

            return [
                ConnectionTarget(
                    did=connection.their_did,
                    endpoint=endpoint,
                    label=invitation.label,
                    recipient_keys=recipient_keys,
                    routing_keys=routing_keys,
                    sender_key=my_info.verkey,
                )
            ]
        else:
            if not connection.their_did:
                self._logger.debug("No target DID associated with connection")
                return None

            did_doc, _ = await self.fetch_did_document(connection.their_did)
            return self.diddoc_connection_targets(
                did_doc, my_info.verkey, connection.their_label
            )

    def diddoc_connection_targets(
        self, doc: DIDDocument, sender_verkey: str, their_label: str = None
    ) -> Sequence[ConnectionTarget]:
        """Get a list of connection targets from a DID Document.

        Args:
            doc: The DID Document to create the target from
            sender_verkey: The verkey we are using
            their_label: The connection label they are using
        """

        if not doc:
            raise BaseConnectionManagerError(
                "No DIDDocument provided for connection target"
            )
        if not doc.service:
            raise BaseConnectionManagerError("No services defined by DIDDocument")

        return [
            ConnectionTarget(
                did=doc.id,
                endpoint=service.endpoint,
                label=their_label,
                recipient_keys=[
                    doc.dereference(key).material
                    for key in (self._retrieve_service_key(service) or ())
                ],
                routing_keys=[
                    key.material
                    for key in (self._retrieve_service_key(service, routing=True) or ())
                ],
                sender_key=sender_verkey,
            )
            for service in doc.service
            if self._retrieve_service_key(service)
        ]

    async def fetch_did_document(self, did: str) -> Tuple[DIDDocument, StorageRecord]:
        """Retrieve a DID Document for a given DID.

        Args:
            did: The DID to search for
        """
        storage = self._session.inject(BaseStorage)
        tag = {"did": did}
        if "did:" not in did:
            tag = {"did": f"did:sov:{did}"}
        record = await storage.find_record(self.RECORD_TYPE_DID_DOC, tag)
        did_doc = DIDDocument.from_json(
            record.value, options={options.vm_allow_missing_controller}
        )
        return did_doc, record

    def _did_without_method(self, did: str) -> str:
        """Retrieve the DID without method from a Sting."""

        return DID(did).method_specific_id

    def _retrieve_service_key(self, service, routing=False):
        """Retrieve service keys from Service or DIDCommService.

        Args:
            service: pydid Service or DIDCommService instance.
            routing: Boolean that indicate if it is a routing key.
        """

        if routing:
            if isinstance(service, DIDCommService):
                result = service.routing_keys
            else:
                result = service.extra["routingKeys"]

        else:
            if isinstance(service, DIDCommService):
                result = service.recipient_keys
            else:
                result = service.extra["recipientKeys"]

        return result
