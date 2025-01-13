class InvalidUrlFormatError(Exception):
    def __init__(self) -> None:
        message = "Invalid URL format."
        super().__init__(message)
