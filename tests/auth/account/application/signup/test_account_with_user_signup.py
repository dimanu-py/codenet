from unittest.mock import AsyncMock

import pytest

from src.auth.account.application.signup.account_with_user_signup import AccountWithUserSignup
from src.auth.account.domain.account import Account
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
        account_primitives = account.to_primitives()
        user_primitives = UserMother.create(id=account_primitives["id"]).to_primitives()

        self._clock.should_generate(account_primitives["created_at"])

        await self._signup.execute(
            account_id=account_primitives["id"],
            name=user_primitives["name"],
            username=user_primitives["username"],
            email=account_primitives["email"],
            plain_password=account_primitives["password"],
        )

        self._should_have_saved_account(account)
        self._should_have_saved_user(user_primitives)

    def _should_have_saved_account(self, account: Account) -> None:
        self._account_repository.should_have_saved(account)

    def _should_have_saved_user(self, user: dict) -> None:
        self._user_signup.execute.assert_awaited_once_with(**user)
