from unittest.mock import AsyncMock

import pytest

from src.auth.account.application.signup.account_with_user_signup import AccountWithUserSignup
from src.social.user.application.signup.user_signup import UserSignup
from tests.auth.account.domain.mothers.account_mother import AccountMother
from tests.auth.account.infra.persistence.mock_account_repository import MockAccountRepository
from tests.shared.infra.mock_clock import MockClock
from tests.social.user.domain.mothers.user_mother import UserMother


@pytest.mark.unit
@pytest.mark.asyncio
class TestAccountWithUserSignup:
    def setup_method(self) -> None:
        self._account_repository = MockAccountRepository()
        self._user_signup = AsyncMock(spec=UserSignup)
        self._clock = MockClock()
        self._signup = AccountWithUserSignup(
            repository=self._account_repository, user_signup=self._user_signup, clock=self._clock
        )

    async def test_should_signup_account_and_user(self) -> None:
        account = AccountMother.any()
        user = UserMother.create(id=account["id"], email=account["email"]).to_primitives()

        self._clock.should_generate(account["created_at"])

        await self._signup.execute(
            account_id=account["id"],
            name=user["name"],
            username=user["username"],
            email=account["email"],
            plain_password=account["password"],
        )

        self._should_have_saved_account(account)
        self._should_have_saved_user(user)

    def _should_have_saved_account(self, account: dict) -> None:
        self._account_repository.should_have_saved(account)

    def _should_have_saved_user(self, user: dict) -> None:
        self._user_signup.execute.assert_awaited_once_with(**user)
