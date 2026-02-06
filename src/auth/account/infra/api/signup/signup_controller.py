from src.auth.account.application.signup.account_with_user_signup import AccountWithUserSignup
from src.shared.infra.http.success_response import SuccessResponse, AcceptedResponse


class SignupController:
    def __init__(self, use_case: AccountWithUserSignup) -> None:
        self._signup = use_case

    async def signup(self, account_id: str, name: str, username: str, email: str, password: str) -> SuccessResponse:
        await self._signup.execute(
            account_id=account_id,
            name=name,
            username=username,
            email=email,
            plain_password=password,
        )
        return AcceptedResponse()
