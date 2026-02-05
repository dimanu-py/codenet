from src.shared.infra.http.success_response import SuccessResponse


class AccountSignupController:
    async def signup(self) -> SuccessResponse:
        raise NotImplementedError
