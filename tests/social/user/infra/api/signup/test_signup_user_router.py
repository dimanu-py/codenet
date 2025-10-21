from doublex import ANY_ARG, when

from src.shared.domain.exceptions.domain_error import DomainError
from src.social.user.application.signup.user_signup import UserSignup
from src.social.user.domain.user_email import InvalidEmailFormatError
from src.social.user.domain.user_name import InvalidNameFormatError
from src.social.user.domain.user_username import InvalidUsernameFormatError
from src.social.user.infra.api.signup.signup_user_router import signup_user
from src.social.user.infra.api.signup.user_sign_up_request import UserSignupRequest
from tests.shared.expects.async_stub import AsyncStub
from tests.social.user.domain.mothers.user_email_primitives_mother import UserEmailPrimitivesMother
from tests.social.user.domain.mothers.user_id_primitives_mother import UserIdPrimitivesMother
from tests.social.user.domain.mothers.user_name_primitives_mother import UserNamePrimitivesMother
from tests.social.user.domain.mothers.user_username_primitives_mother import UserUsernamePrimitivesMother
from tests.social.user.infra.api.user_module_routers_test_config import UserModuleRoutersTestConfig


class TestSignupUserRouter(UserModuleRoutersTestConfig):
    def setup_method(self) -> None:
        self._user_signup = AsyncStub(UserSignup)

    async def test_should_return_201_when_signup_data_is_valid(self) -> None:
        request_body = UserSignupRequest(
            name=UserNamePrimitivesMother.any(),
            username=UserUsernamePrimitivesMother.any(),
            email=UserEmailPrimitivesMother.any(),
        )
        user_id = UserIdPrimitivesMother.any()
        self._should_signup_user()

        self._response = await signup_user(
            request=request_body,
            user_id=user_id,
            user_signup=self._user_signup,
        )

        self._assert_contract_is_met_with(201, {"resource": f"/app/users/{user_id}"})

    async def test_should_return_422_when_user_name_has_invalid_character(self) -> None:
        request_body = UserSignupRequest(
            name="Invalid@Name",
            username=UserUsernamePrimitivesMother.any(),
            email=UserEmailPrimitivesMother.any(),
        )
        user_id = UserIdPrimitivesMother.any()
        self._should_fail_validating_user_data_with(InvalidNameFormatError)

        self._response = await signup_user(
            request=request_body,
            user_id=user_id,
            user_signup=self._user_signup,
        )

        self._assert_contract_is_met_with(422, {"detail": "Name cannot contain special characters or numbers."})

    async def test_should_return_422_when_user_username_has_invalid_character(self) -> None:
        request_body = UserSignupRequest(
            name=UserNamePrimitivesMother.any(),
            username="Invalid*Username",
            email=UserEmailPrimitivesMother.any(),
        )
        user_id = UserIdPrimitivesMother.any()
        self._should_fail_validating_user_data_with(InvalidUsernameFormatError)

        self._response = await signup_user(
            request=request_body,
            user_id=user_id,
            user_signup=self._user_signup,
        )

        self._assert_contract_is_met_with(422, {"detail": "Username cannot contain special characters"})

    async def test_should_return_422_when_email_does_not_have_valid_format(self) -> None:
        request_body = UserSignupRequest(
            name=UserNamePrimitivesMother.any(),
            username=UserUsernamePrimitivesMother.any(),
            email="invalid-email-format",
        )
        user_id = UserIdPrimitivesMother.any()
        self._should_fail_validating_user_data_with(InvalidEmailFormatError)

        self._response = await signup_user(
            request=request_body,
            user_id=user_id,
            user_signup=self._user_signup,
        )

        self._assert_contract_is_met_with(
            422, {"detail": "Email cannot contain special characters and must contain '@' and '.'"}
        )

    def _should_signup_user(self) -> None:
        when(self._user_signup).execute(ANY_ARG).returns(None)

    def _should_fail_validating_user_data_with(self, error: DomainError) -> None:
        when(self._user_signup).execute(ANY_ARG).raises(error)
