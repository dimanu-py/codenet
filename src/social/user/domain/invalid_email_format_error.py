class InvalidEmailFormatError(Exception):
    def __init__(self) -> None:
        message = "Email cannot contain special characters and must contain '@' and '.'"
        super().__init__(message)
