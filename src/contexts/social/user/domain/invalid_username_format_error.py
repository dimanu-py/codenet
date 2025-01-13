class InvalidUsernameFormatError(Exception):
    def __init__(self) -> None:
        message = "The username can only contain letters, numbers and underscores."
        super().__init__(message)
