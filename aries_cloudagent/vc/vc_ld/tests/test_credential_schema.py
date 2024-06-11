"""Test VcLdpManager."""

from unittest import IsolatedAsyncioTestCase
from aries_cloudagent.core.in_memory.profile import InMemoryProfile
from aries_cloudagent.resolver.default.key import KeyDIDResolver
from aries_cloudagent.resolver.did_resolver import DIDResolver
from aries_cloudagent.vc.ld_proofs.document_loader import DocumentLoader
from aries_cloudagent.vc.ld_proofs.schema_manager import VcSchemaValidatorError
from aries_cloudagent.wallet.default_verification_key_strategy import BaseVerificationKeyStrategy, DefaultVerificationKeyStrategy
import pytest
from ....wallet.did_method import  DIDMethods
from ..manager import VcLdpManager
from ..models.credential import VerifiableCredential
from ..models.options import LDProofVCOptions
from ...tests.data import (
    TEST_LD_DOCUMENT_CORRECT_SCHEMA,
    TEST_LD_DOCUMENT_INCORRECT_SCHEMA,
)

TEST_DID_SOV = "did:sov:LjgpST2rjsoxYegQDRm7EL"
TEST_DID_KEY = "did:key:z6Mkgg342Ycpuk263R9d8Aq6MUaxPn1DDeHyGo38EefXmgDL"
TEST_UUID = "urn:uuid:1b6824b1-db3f-43e8-8f17-baf618743635"



class TestCredentialSchema(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.did_resolver = DIDResolver([KeyDIDResolver()])
        self.profile = InMemoryProfile.test_profile(
        {},
        {
            DIDMethods: DIDMethods(),
            BaseVerificationKeyStrategy: DefaultVerificationKeyStrategy(),
            DIDResolver: self.did_resolver,
        },
    )
        self.ldp_manager = VcLdpManager(self.profile)
        self.profile.context.injector.bind_instance(DocumentLoader, DocumentLoader(self.profile))
        self.options = LDProofVCOptions.deserialize({
            "proofType": "Ed25519Signature2018",
            "created": "2019-12-11T03:50:55",
        })
        

    async def test_derive_ld_proofs(self):
        vc = VerifiableCredential.deserialize(TEST_LD_DOCUMENT_CORRECT_SCHEMA)
        detail = await self.ldp_manager.prepare_credential(vc, self.options, None, True)
        assert detail

    async def test_prepare_detail(
        self
    ):
        vc = VerifiableCredential.deserialize(TEST_LD_DOCUMENT_CORRECT_SCHEMA)
        detail = await self.ldp_manager.prepare_credential(vc, self.options, None, True)
        assert detail

    
    async def test_prepare_detail_fail(
        self
    ):
        vc = VerifiableCredential.deserialize(TEST_LD_DOCUMENT_INCORRECT_SCHEMA)
        with pytest.raises(VcSchemaValidatorError) as validator_error:
            await self.ldp_manager.prepare_credential(vc, self.options, None, True)
    
        assert '''"reason": "\'2.1\' is not of type \'number\'", "credential_path": "$.credentialSubject.creditsEarned"''' in validator_error.value.args[0]