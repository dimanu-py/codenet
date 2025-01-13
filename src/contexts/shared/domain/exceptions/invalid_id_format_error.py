class InvalidIdFormatError(Exception):
    def __init__(self) -> None:
        message = "Id must follow UUID format."
        super().__init__(message)
