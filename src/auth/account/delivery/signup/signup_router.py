from fastapi import APIRouter, Depends, Path, status
from fastapi.openapi.models import Example
from starlette.responses import JSONResponse

from src.auth.account.application.signup.account_with_user_signup import AccountWithUserSignup
from src.auth.account.delivery.deps import postgres_account_repository
from src.auth.account.delivery.signup.signup_request import SignupRequest
from src.auth.account.infra.api.signup.signup_controller import SignupController
from src.auth.account.infra.argon_password_manager import ArgonPasswordManager
from src.auth.account.infra.persistence.postgres_account_repository import PostgresAccountRepository
from src.backoffice.user.application.signup.user_signup import UserSignup
from src.backoffice.user.delivery.deps import postgres_user_repository
from src.backoffice.user.infra.persistence.postgres_user_repository import PostgresUserRepository
from src.shared.delivery.fastapi_response import FastAPIResponse
from src.shared.infra.api.error_response import UnprocessableEntityError
from src.shared.infra.api.success_response import AcceptedResponse
from src.shared.infra.datetime_clock import DatetimeClock

signup_router = APIRouter()


def get_controller(
    account_repository: PostgresAccountRepository = Depends(postgres_account_repository),
    user_repository: PostgresUserRepository = Depends(postgres_user_repository),
) -> SignupController:
    return SignupController(
        use_case=AccountWithUserSignup(
            repository=account_repository,
            user_signup=UserSignup(
                repository=user_repository,
            ),
            password_manager=ArgonPasswordManager(),
            clock=DatetimeClock(),
        )
    )


@signup_router.post(
    "/{account_id}",
    responses={
        status.HTTP_202_ACCEPTED: {"model": AcceptedResponse},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": UnprocessableEntityError},
    },
)
async def signup_account_and_user(
    request: SignupRequest,
    account_id: str = Path(
        openapi_examples={"valid_id": Example(value="123e4567-e89b-12d3-a456-426614174000")},
    ),
    controller: SignupController = Depends(get_controller),
) -> JSONResponse:
    result = await controller.signup(
        account_id=account_id,
        name=request.name,
        username=request.username,
        email=request.email,
        password=request.password,
    )
    return FastAPIResponse.as_json(result)
