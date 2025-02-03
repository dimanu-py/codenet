class InvalidIdFormatError(Exception):
    def __init__(self) -> None:
        message = "User id must be a valid UUID"
        super().__init__(message)
