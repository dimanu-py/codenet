from src.shared.domain.exceptions.application_error import ApplicationError


class UserNotFound(ApplicationError):
    def __init__(self) -> None:
        super().__init__(
            message="User with that id not found",
            error_type="user_resource_not_found",
        )
