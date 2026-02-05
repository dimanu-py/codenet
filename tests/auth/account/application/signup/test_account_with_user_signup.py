import pytest

from src.auth.account.application.signup.account_with_user_signup import AccountWithUserSignup
from tests.auth.account.domain.mothers.account_mother import AccountMother
from tests.social.user.domain.mothers.user_mother import UserMother


@pytest.mark.unit
@pytest.mark.asyncio
class TestAccountWithUserSignup:
    def setup_method(self) -> None:
        self._signup = AccountWithUserSignup()

    async def test_should_signup_account_and_user(self) -> None:
        account = AccountMother.any()
        user = UserMother.create(id=account["id"]).to_primitives()

        self._should_save_account(account)
        self._should_save_user(user)

        await self._signup.execute(
            account_id=account["id"],
            name=user["name"],
            username=user["username"],
            email=account["email"],
            password=account["password"],
        )

    def _should_save_account(self, account: dict) -> None:
        pass

    def _should_save_user(self, user: dict) -> None:
        pass
