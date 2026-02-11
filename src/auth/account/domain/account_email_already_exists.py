from src.shared.domain.exceptions.application_error import ConflictError


class AccountEmailAlreadyExists(ConflictError):
    def __init__(self) -> None:
        super().__init__(
            message="Email is already signed up",
            error_type="account_resource_conflict_error",
        )
