import logging
from typing import TypedDict

from asgi_correlation_id import CorrelationIdFilter

from src.shared.infra.logger.file_rotating_handler import TimeRotatingFileHandler


class SuccessRecordDetails(TypedDict):
    method: str
    source: str
    process_time: float
    status_code: int


class ErrorRecordDetails(TypedDict):
    method: str
    error_message: str
    source: str
    status_code: int


class FastApiFileLogger:
    def __init__(self, name: str, handlers: list[logging.Handler]) -> None:
        self._logger = logging.getLogger(name)
        self._logger.setLevel(logging.DEBUG)
        self._logger.addFilter(CorrelationIdFilter())

        if not self._logger.hasHandlers():
            self._logger.handlers.extend(handlers)

    def success(self, message: str, details: SuccessRecordDetails) -> None:
        self._logger.info(
            msg=f"success - {message}",
            extra={"details": details},
        )

    def error(self, message: str, details: ErrorRecordDetails) -> None:
        self._logger.error(
            msg=f"error - {message}",
            extra={"details": details},
        )


def create_api_logger(name: str) -> FastApiFileLogger:
    return FastApiFileLogger(
        name=name,
        handlers=[
            TimeRotatingFileHandler.create(
                file_name="production",
                level_to_record=logging.ERROR,
            ),
            TimeRotatingFileHandler.create(
                file_name="dev",
                level_to_record=logging.DEBUG,
            ),
        ],
    )
