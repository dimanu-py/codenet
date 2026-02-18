import pytest

from src.auth.account.application.signup.account_signup import AccountSignup
from src.auth.account.domain.account import Account
from src.auth.account.domain.account_email_already_exists import AccountEmailAlreadyExists
from tests.auth.account.domain.mothers.account_mother import AccountMother
from tests.auth.account.infra.fake_password_manager import FakePasswordManager
from tests.auth.account.infra.persistence.mock_account_repository import MockAccountRepository
from tests.backoffice.user.domain.mothers.user_mother import UserMother
from tests.shared.expects.matchers import async_expect, raise_error
from tests.shared.infra.mock_clock import MockClock


@pytest.mark.unit
@pytest.mark.asyncio
class TestAccountSignup:
    def setup_method(self) -> None:
        self._account_repository = MockAccountRepository()
        self._clock = MockClock()
        self._password_manager = FakePasswordManager()
        self._signup = AccountSignup(repository=self._account_repository, password_manager=self._password_manager,
                                     clock=self._clock)

    async def test_should_signup_a_new_account(self) -> None:
        account = AccountMother.any()
        account_primitives = account.to_primitives()
        user_primitives = UserMother.create(id=account_primitives["id"]).to_primitives()

        self._clock.should_generate(account_primitives["created_at"])
        self._should_search_and_not_find_account()

        await self._signup.execute(account_id=account_primitives["id"], username=user_primitives["username"],
                                   email=account_primitives["email"], plain_password=account_primitives["password"])

        self._should_have_saved_account(account)

    async def test_should_raise_error_when_account_email_is_already_signed_up(self) -> None:
        existing_account = AccountMother.any()
        existing_account_primitives = existing_account.to_primitives()
        user_primitives = UserMother.create(id=existing_account_primitives["id"]).to_primitives()
        self._should_search_and_find(existing_account)

        signup_information = {
            "account_id": existing_account_primitives["id"],
            "username": user_primitives["username"],
            "email": existing_account_primitives["email"],
            "plain_password": existing_account_primitives["password"],
        }
        await async_expect(lambda: self._signup.execute(**signup_information)).to(
            raise_error(AccountEmailAlreadyExists)
        )

    def _should_have_saved_account(self, account: Account) -> None:
        self._account_repository.should_have_saved(account)

    def _should_search_and_find(self, account: Account) -> None:
        self._account_repository.should_search(account)

    def _should_search_and_not_find_account(self) -> None:
        self._account_repository.should_not_search_account()
