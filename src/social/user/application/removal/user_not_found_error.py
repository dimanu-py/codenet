from src.shared.domain.exceptions.application_error import ApplicationError


class UserNotFoundError(ApplicationError):
    def __init__(self, user_id: str) -> None:
        super().__init__(
            message=f"User with id {user_id} not found",
            error_type="user_not_found",
        )
