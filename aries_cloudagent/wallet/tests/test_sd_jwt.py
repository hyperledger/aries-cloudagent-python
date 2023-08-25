import pytest

from ...wallet.did_method import KEY
from ...wallet.key_type import ED25519

from ..sd_jwt import SDJWTVerifyResult, sd_jwt_sign, sd_jwt_verify

from .test_jwt import profile, in_memory_wallet


@pytest.fixture
def create_address_payload():
    return {
        "address": {
            "street_address": "123 Main St",
            "locality": "Anytown",
            "region": "Anystate",
            "country": "US",
        },
        "iss": "https://example.com/issuer",
        "iat": 1683000000,
        "exp": 1883000000,
    }


class TestSDJWT:
    """Tests for JWT sign and verify using dids."""

    seed = "testseed000000000000000000000001"
    headers = {}

    @pytest.mark.asyncio
    async def test_sign_with_did_key_and_verify(self, profile, in_memory_wallet):
        did_info = await in_memory_wallet.create_local_did(KEY, ED25519, self.seed)
        verification_method = None
        payload = {
            "sub": "user_42",
            "given_name": "John",
            "family_name": "Doe",
            "email": "johndoe@example.com",
            "phone_number": "+1-202-555-0101",
            "phone_number_verified": True,
            "address": {
                "street_address": {
                    "house_number": "123",
                    "street": "Main St",
                },
                "locality": "Anytown",
                "region": "Anystate",
                "country": "US",
            },
            "birthdate": "1940-01-01",
            "updated_at": 1570000000,
            "nationalities": ["US", "DE", "SA"],
            "iss": "https://example.com/issuer",
            "iat": 1683000000,
            "exp": 1883000000,
        }
        non_sd_list = [
            "given_name",
            "family_name",
            "nationalities",
        ]
        signed = await sd_jwt_sign(
            profile,
            self.headers,
            payload,
            non_sd_list,
            did_info.did,
            verification_method,
        )
        assert signed

        assert await sd_jwt_verify(profile, signed)

    @pytest.mark.asyncio
    async def test_flat_structure(
        self, profile, in_memory_wallet, create_address_payload
    ):
        did_info = await in_memory_wallet.create_local_did(KEY, ED25519, self.seed)
        verification_method = None
        non_sd_list = [
            "address.street_address",
            "address.street_address.house_number",
            "address.street_address.street",
            "address.locality",
            "address.region",
            "address.country",
        ]
        signed = await sd_jwt_sign(
            profile,
            self.headers,
            create_address_payload,
            non_sd_list,
            did_info.did,
            verification_method,
        )
        assert signed

        verified = await sd_jwt_verify(profile, signed)
        assert isinstance(verified, SDJWTVerifyResult)
        assert verified.valid
        assert verified.payload["_sd"]
        assert verified.payload["_sd_alg"]
        assert verified.disclosures[0][1] == "address"
        assert verified.disclosures[0][2] == {
            "street_address": "123 Main St",
            "locality": "Anytown",
            "region": "Anystate",
            "country": "US",
        }

    @pytest.mark.asyncio
    async def test_nested_structure(
        self, profile, in_memory_wallet, create_address_payload
    ):
        did_info = await in_memory_wallet.create_local_did(KEY, ED25519, self.seed)
        verification_method = None
        non_sd_list = ["address"]

        signed = await sd_jwt_sign(
            profile,
            self.headers,
            create_address_payload,
            non_sd_list,
            did_info.did,
            verification_method,
        )
        assert signed

        verified = await sd_jwt_verify(profile, signed)
        assert isinstance(verified, SDJWTVerifyResult)
        assert verified.valid
        assert len(verified.payload["address"]["_sd"]) >= 4
        assert verified.payload["_sd_alg"]
        sd_claims = ["street_address", "region", "locality", "country"]
        assert sorted(sd_claims) == sorted([claim[1] for claim in verified.disclosures])

    @pytest.mark.asyncio
    async def test_recursive_nested_structure(
        self, profile, in_memory_wallet, create_address_payload
    ):
        did_info = await in_memory_wallet.create_local_did(KEY, ED25519, self.seed)
        verification_method = None
        non_sd_list = []

        signed = await sd_jwt_sign(
            profile,
            self.headers,
            create_address_payload,
            non_sd_list,
            did_info.did,
            verification_method,
        )
        assert signed

        verified = await sd_jwt_verify(profile, signed)
        assert isinstance(verified, SDJWTVerifyResult)
        assert verified.valid
        assert "address" not in verified.payload
        assert verified.payload["_sd"]
        assert verified.payload["_sd_alg"]
        sd_claims = ["street_address", "region", "locality", "country"]
        for disclosure in verified.disclosures:
            if disclosure[1] == "address":
                assert isinstance(disclosure[2], dict)
                assert len(disclosure[2]["_sd"]) >= 4
            else:
                assert disclosure[1] in sd_claims

    @pytest.mark.asyncio
    async def test_list_splice(self, profile, in_memory_wallet):
        did_info = await in_memory_wallet.create_local_did(KEY, ED25519, self.seed)
        payload = {"nationalities": ["US", "DE", "SA"]}
        verification_method = None
        non_sd_list = ["nationalities", "nationalities[1:3]"]

        signed = await sd_jwt_sign(
            profile,
            self.headers,
            payload,
            non_sd_list,
            did_info.did,
            verification_method,
        )
        assert signed

        verified = await sd_jwt_verify(profile, signed)
        assert isinstance(verified, SDJWTVerifyResult)
        assert verified.valid
        for nationality in verified.payload["nationalities"]:
            if isinstance(nationality, dict):
                assert nationality["..."]
                assert len(nationality) == 1
            else:
                assert nationality in payload["nationalities"]
        assert verified.payload["_sd_alg"]
        assert verified.disclosures[0][1] == "US"