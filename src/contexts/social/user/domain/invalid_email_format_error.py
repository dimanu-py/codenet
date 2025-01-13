class InvalidEmailFormatError(Exception):
    def __init__(self) -> None:
        message = "Email cannot contain special characters and must have an @ symbol."
        super().__init__(message)
