class InvalidNameFormatError(Exception):
    def __init__(self) -> None:
        message = "Name cannot contain special characters or numbers."
        super().__init__(message)
