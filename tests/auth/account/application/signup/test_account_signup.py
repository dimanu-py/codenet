import pytest

from src.auth.account.application.signup.account_signup import AccountSignup
from src.auth.account.domain.account import Account
from src.auth.account.domain.account_email_already_exists import AccountEmailAlreadyExists
from src.auth.account.domain.account_username_already_exists import AccountUsernameAlreadyExists
from tests.auth.account.domain.mothers.account_mother import AccountMother
from tests.auth.account.infra.fake_password_manager import FakePasswordManager
from tests.auth.account.infra.persistence.mock_account_repository import MockAccountRepository
from tests.shared.expects.matchers import async_expect, raise_error
from tests.shared.infra.mock_clock import MockClock


@pytest.mark.unit
@pytest.mark.asyncio
class TestAccountSignup:
    def setup_method(self) -> None:
        self._repository = MockAccountRepository()
        self._clock = MockClock()
        self._password_manager = FakePasswordManager()
        self._signup = AccountSignup(repository=self._repository, password_manager=self._password_manager,
                                     clock=self._clock)

    def teardown_method(self) -> None:
        self._repository.reset_mocks()

    async def test_should_signup_a_new_account(self) -> None:
        account = AccountMother.any()
        account_primitives = account.to_primitives()

        self._clock.should_generate(account_primitives["created_at"])
        self._should_not_find_account_matching_criteria()

        await self._signup.execute(account_id=account_primitives["id"], username=account_primitives["username"],
                                   email=account_primitives["email"], plain_password=account_primitives["password"])

        self._should_have_saved_account(account)

    async def test_should_not_allow_to_signup_account_with_already_registered_email(self) -> None:
        existing_account = AccountMother.any()
        existing_account_primitives = existing_account.to_primitives()
        new_account_primitives = AccountMother.with_email(existing_account_primitives["email"]).to_primitives()

        self._should_match_criteria_with([existing_account])

        signup_information = {
            "account_id": new_account_primitives["id"],
            "username": new_account_primitives["username"],
            "email": existing_account_primitives["email"],
            "plain_password": new_account_primitives["password"],
        }
        await async_expect(lambda: self._signup.execute(**signup_information)).to(
            raise_error(AccountEmailAlreadyExists)
        )

        self._should_have_not_saved_account()

    async def test_should_not_allow_to_signup_account_with_already_registered_username(self) -> None:
        existing_account = AccountMother.any()
        existing_account_primitives = existing_account.to_primitives()
        new_account_primitives = AccountMother.with_username(existing_account_primitives['username']).to_primitives()

        self._should_match_criteria_with([], [existing_account])

        signup_information = {
            "account_id": new_account_primitives["id"],
            "username": existing_account_primitives["username"],
            "email": new_account_primitives["email"],
            "plain_password": new_account_primitives["password"],
        }
        await async_expect(lambda: self._signup.execute(**signup_information)).to(
            raise_error(AccountUsernameAlreadyExists)
        )

        self._should_have_not_saved_account()

    def _should_have_saved_account(self, account: Account) -> None:
        self._repository.should_have_saved(account)

    def _should_have_not_saved_account(self) -> None:
        self._repository.should_not_have_saved_account()

    def _should_not_find_account_matching_criteria(self) -> None:
        self._repository.should_not_match_criteria()

    def _should_match_criteria_with(self, *accounts: list[Account]) -> None:
        self._repository.should_match_criteria_with_successive_calls(*accounts)

