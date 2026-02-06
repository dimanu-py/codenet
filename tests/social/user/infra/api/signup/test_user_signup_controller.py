from unittest.mock import AsyncMock

from src.shared.domain.exceptions.base_error import BaseError
from src.social.user.application.signup.user_signup import UserSignup
from src.social.user.delivery.signup import SignupRequest
from src.social.user.domain.user_email import InvalidEmailFormat
from src.social.user.domain.user_name import InvalidNameFormat
from src.social.user.domain.user_username import InvalidUsernameFormat
from src.social.user.infra.api.signup.user_signup_controller import UserSignupController
from tests.social.user.domain.mothers.user_email_primitives_mother import UserEmailPrimitivesMother
from tests.social.user.domain.mothers.user_id_primitives_mother import UserIdPrimitivesMother
from tests.social.user.domain.mothers.user_name_primitives_mother import UserNamePrimitivesMother
from tests.social.user.domain.mothers.user_username_primitives_mother import UserUsernamePrimitivesMother
from tests.social.user.domain.user_already_exists import UsernameAlreadyExists
from tests.social.user.infra.api.user_module_routers_test_config import UserModuleRoutersTestConfig


class TestUserSignupController(UserModuleRoutersTestConfig):
    def setup_method(self) -> None:
        self._use_case = AsyncMock(spec=UserSignup)
        self._controller = UserSignupController(use_case=self._use_case)

    async def test_should_return_202_when_signup_data_is_valid(self) -> None:
        request_body = SignupRequest(
            name=UserNamePrimitivesMother.any(),
            username=UserUsernamePrimitivesMother.any(),
            email=UserEmailPrimitivesMother.any(),
        )
        user_id = UserIdPrimitivesMother.any()
        self._should_signup_user()

        self._response = await self._controller.signup(id=user_id, **request_body.model_dump())

        self._assert_contract_is_met_on_success(202, {"accepted": True})

    async def test_should_return_422_when_user_name_has_invalid_character(self) -> None:
        request_body = SignupRequest(
            name="Invalid@Name",
            username=UserUsernamePrimitivesMother.any(),
            email=UserEmailPrimitivesMother.any(),
        )
        user_id = UserIdPrimitivesMother.any()
        self._should_fail_with_error(InvalidNameFormat)

        self._response = await self._controller.signup(id=user_id, **request_body.model_dump())

        self._assert_contract_is_met_on_error(422, "Name cannot contain special characters or numbers.")

    async def test_should_return_422_when_user_username_has_invalid_character(self) -> None:
        request_body = SignupRequest(
            name=UserNamePrimitivesMother.any(),
            username="Invalid*Username",
            email=UserEmailPrimitivesMother.any(),
        )
        user_id = UserIdPrimitivesMother.any()
        self._should_fail_with_error(InvalidUsernameFormat)

        self._response = await self._controller.signup(id=user_id, **request_body.model_dump())

        self._assert_contract_is_met_on_error(422, "Username cannot contain special characters")

    async def test_should_return_422_when_email_does_not_have_valid_format(self) -> None:
        request_body = SignupRequest(
            name=UserNamePrimitivesMother.any(),
            username=UserUsernamePrimitivesMother.any(),
            email="invalid-email-format",
        )
        user_id = UserIdPrimitivesMother.any()
        self._should_fail_with_error(InvalidEmailFormat)

        self._response = await self._controller.signup(id=user_id, **request_body.model_dump())

        self._assert_contract_is_met_on_error(
            422, "Email cannot contain special characters and must contain '@' and '.'"
        )

    async def test_should_return_409_when_username_is_already_registered(self) -> None:
        request_body = SignupRequest(
            name=UserNamePrimitivesMother.any(),
            username=UserUsernamePrimitivesMother.any(),
            email=UserEmailPrimitivesMother.any(),
        )
        user_id = UserIdPrimitivesMother.any()
        self._should_fail_with_error(UsernameAlreadyExists)

        self._response = await self._controller.signup(id=user_id, **request_body.model_dump())

        self._assert_contract_is_met_on_error(409, "Username is already registered.")

    def _should_signup_user(self) -> None:
        self._use_case.execute.return_value = None

    def _should_fail_with_error(self, error: BaseError) -> None:
        self._use_case.execute.side_effect = error
