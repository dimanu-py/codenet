import logging

from src.shared.infra.logger.file_rotating_handler import TimeRotatingFileHandler


class FastApiFileLogger:
    def __init__(self, name: str, handlers: list[logging.Handler]) -> None:
        self._logger = logging.getLogger(name)
        self._logger.setLevel(logging.DEBUG)

        if not self._logger.hasHandlers():
            self._logger.handlers.extend(handlers)

    def debug(self, message: str, details: dict) -> None:
        self._logger.debug(
            msg=message,
            extra={"details": details},
        )

    def info(self, message: str, details: dict) -> None:
        self._logger.info(
            msg=message,
            extra={"details": details},
        )

    def warning(self, message: str, details: dict) -> None:
        raise NotImplementedError

    def error(self, message: str, details: dict) -> None:
        self._logger.error(
            msg=message,
            extra={"details": details},
        )

    def critical(self, message: str, details: dict) -> None:
        self._logger.critical(
            msg=message,
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
