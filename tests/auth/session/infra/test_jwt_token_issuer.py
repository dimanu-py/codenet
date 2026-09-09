import jwt
import pytest
from expects import equal, expect, have_keys

from src.auth.session.infra.jwt_token_issuer import JwtTokenIssuer
from src.shared.delivery.settings import Settings


@pytest.mark.integration
@pytest.mark.asyncio
class TestJwtTokenIssuer:
    _SECRET_KEY = "test-secret-key-that-is-long-enough-for-hs256"
    _ALGORITHM = "HS256"
    _EXPIRES_IN = 3600

    def setup_method(self) -> None:
        self._settings = Settings(
            JWT_SECRET_KEY=self._SECRET_KEY, JWT_ALGORITHM=self._ALGORITHM, JWT_EXPIRES_IN=self._EXPIRES_IN
        )
        self._token_issuer = JwtTokenIssuer(settings=self._settings)

    async def test_should_generate_token_with_required_fields(self) -> None:
        account_id = "test-user"

        token = await self._token_issuer.generate_token(account_id)

        expect(token).to(have_keys("access_token", "token_type", "expires_in"))
        expect(token["token_type"]).to(equal("bearer"))
        expect(token["expires_in"]).to(equal(self._EXPIRES_IN))

    async def test_should_include_account_id_in_token_claim_sub(self) -> None:
        account_id = "9c9e2b1a-3a2b-4f3e-9c8b-1a2b3c4d5e6f"

        token = await self._token_issuer.generate_token(account_id)
        decoded = jwt.decode(token["access_token"], self._SECRET_KEY, algorithms=[self._ALGORITHM])

        expect(decoded.get("sub")).to(equal(account_id))
