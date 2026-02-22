from src.shared.domain.exceptions.domain_error import DomainError


class AccountAuthenticator:
    async def execute(self, identification: str, password: str) -> str:
        pass


class InvalidCredentials(DomainError):
    def __init__(self) -> None:
        super().__init__(
            message="Invalid credentials",
            error_type="invalid_credentials",
        )
