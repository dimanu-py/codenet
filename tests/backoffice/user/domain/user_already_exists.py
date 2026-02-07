from src.shared.domain.exceptions.application_error import ConflictError


class UsernameAlreadyExists(ConflictError):
    def __init__(self) -> None:
        super().__init__(
            message="Username is already registered.",
            error_type="username_already_exists",
        )
