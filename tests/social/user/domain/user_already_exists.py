from src.shared.domain.exceptions.application_error import ApplicationError


class UsernameAlreadyExists(ApplicationError):
    def __init__(self) -> None:
        super().__init__(
            message="Username already exists.",
            error_type="username_already_exists",
        )
