import logging
from datetime import date
from logging.handlers import TimedRotatingFileHandler

from src.shared.infra.log.json_formatter import JSONFormatter


def create_file_handler(file_name: str, level: int) -> TimedRotatingFileHandler:
    file_handler = TimedRotatingFileHandler(
        filename=f"var/logs/{file_name}_{date.today().isoformat()}.log",
        when="midnight",
        interval=1,
        backupCount=7,
        encoding="utf-8",
    )
    file_handler.setFormatter(JSONFormatter())
    file_handler.setLevel(level)

    return file_handler


def create_logger(logger_name: str) -> logging.Logger:
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    production_handler = create_file_handler(file_name="prod", level=logging.ERROR)
    develop_handler = create_file_handler(file_name="dev", level=logging.DEBUG)

    if not logger.handlers:
        logger.addHandler(production_handler)
        logger.addHandler(develop_handler)

    return logger
