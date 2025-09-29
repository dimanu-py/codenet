import json
import logging


class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_record = {
            "time": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
        }

        if hasattr(record, "details"):
            log_record["details"] = record.details
        if hasattr(record, "correlation_id"):
            log_record["correlation_id"] = record.correlation_id

        return json.dumps(log_record)
