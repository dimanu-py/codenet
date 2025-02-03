class InvalidUsernameFormatError(Exception):
    def __init__(self) -> None:
        message = "Username cannot contain special characters"
        super().__init__(message)
