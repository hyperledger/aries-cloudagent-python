import pytest

from ....core.in_memory import InMemoryProfile
from ....core.profile import Profile
from ....messaging.valid import DIDTdw
from ..tdw import TdwDIDResolver

TEST_DID = "did:tdw:Qma6mc1qZw3NqxwX6SB5GPQYzP4pGN2nXD15Jwi4bcDBKu:domain.example"


@pytest.fixture
def resolver():
    """Resolver fixture."""
    yield TdwDIDResolver()


@pytest.fixture
def profile():
    """Profile fixture."""
    profile = InMemoryProfile.test_profile()
    yield profile


@pytest.mark.asyncio
async def test_supported_did_regex(profile, resolver: TdwDIDResolver):
    """Test the supported_did_regex."""
    assert resolver.supported_did_regex == DIDTdw.PATTERN
    assert await resolver.supports(
        profile,
        TEST_DID,
    )


@pytest.mark.asyncio
async def test_resolve(resolver: TdwDIDResolver, profile: Profile):
    """Test resolve method."""
    assert await resolver.resolve(profile, TEST_DID)
