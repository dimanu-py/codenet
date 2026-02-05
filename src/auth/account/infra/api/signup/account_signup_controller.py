from src.auth.account.application.signup.account_signup import AccountSignup
from src.shared.infra.http.success_response import SuccessResponse


class AccountSignupController:
    def __init__(self, use_case: AccountSignup) -> None:
        self._signup = use_case

    async def signup(self, account_id: str, name: str, username: str, email: str, password: str) -> SuccessResponse:
        raise NotImplementedError
