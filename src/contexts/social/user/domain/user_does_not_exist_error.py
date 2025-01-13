class UserDoesNotExistError(Exception):
    def __init__(self) -> None:
        message = "No user was found with the given fields."
        super().__init__(message)
