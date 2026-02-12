from src.shared.domain.exceptions.domain_error import NotFoundError


class UserNotFound(NotFoundError):
    def __init__(self) -> None:
        super().__init__(
            message="User with that id not found",
            error_type="user_resource_not_found",
        )
