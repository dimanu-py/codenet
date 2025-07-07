from src.shared.domain.exceptions.domain_error import DomainError


class UserNotFoundError(DomainError):
    def __init__(self, user_id: str) -> None:
        self._message = f"User with id {user_id} not found"
        self._type = "user_not_found"
        super().__init__(self._message, self._type)
