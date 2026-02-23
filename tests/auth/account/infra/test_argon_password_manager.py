import pytest
from expects import equal, expect, be_true

from src.auth.account.infra.argon_password_manager import ArgonPasswordManager


@pytest.mark.integration
@pytest.mark.asyncio
class TestArgonPasswordManager:
    def setup_method(self) -> None:
        self._password_manager = ArgonPasswordManager()

    async def test_should_hash_plain_password(self) -> None:
        plain_password = "securePassword123!"

        hashed_password = await self._password_manager.hash(plain_password)

        expect(hashed_password).to_not(equal(plain_password))

    async def test_should_verify_password_is_correct(self) -> None:
        plain_password = "securePassword123!"
        hashed_password = await self._password_manager.hash(plain_password)

        is_correct = await self._password_manager.verify_credentials(plain_password, hashed_password)

        expect(is_correct).to(be_true)

    async def test_should_not_verify_password_if_is_not_hashed(self) -> None:
        plain_password = "securePassword123!"
        not_hashed_password = "notHashedPassword"

        is_correct = await self._password_manager.verify_credentials(plain_password, not_hashed_password)

        expect(is_correct).to_not(be_true)

    async def test_should_verify_password_do_not_match(self) -> None:
        plain_password = "securePassword123!"
        different_hashed_password = await self._password_manager.hash("differentPassword456!")

        is_correct = await self._password_manager.verify_credentials(plain_password, different_hashed_password)

        expect(is_correct).to_not(be_true)
