class InvalidNameFormatError(Exception):
    def __init__(self) -> None:
        message = "Your name cannot contain special characters or numbers"
        super().__init__(message)
