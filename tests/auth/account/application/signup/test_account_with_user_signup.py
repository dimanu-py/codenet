import pytest

from src.auth.account.application.signup.account_with_user_signup import AccountWithUserSignup
from tests.auth.account.domain.mothers.account_mother import AccountMother
from tests.auth.account.infra.persistence.mock_account_repository import MockAccountRepository
from tests.social.user.domain.mothers.user_mother import UserMother


@pytest.mark.unit
@pytest.mark.asyncio
class TestAccountWithUserSignup:
    def setup_method(self) -> None:
        self._account_repository = MockAccountRepository()
        self._signup = AccountWithUserSignup(repository=self._account_repository)

    async def test_should_signup_account_and_user(self) -> None:
        account = AccountMother.any()
        user = UserMother.create(id=account["id"]).to_primitives()

        await self._signup.execute(
            account_id=account["id"],
            name=user["name"],
            username=user["username"],
            email=account["email"],
            password=account["plain_password"],
        )

        self._should_have_saved_account(account)
        self._should_have_saved_user(user)

    def _should_have_saved_account(self, account: dict) -> None:
        self._account_repository.should_have_saved(account)

    def _should_have_saved_user(self, user: dict) -> None:
