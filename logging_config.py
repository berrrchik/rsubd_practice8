import json
import logging
import os
from datetime import datetime, timezone


class JSONFormatter(logging.Formatter):
    """JSON-форматтер для логов приложения."""

    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            "logger": record.name,
            "author": "ZaklyakovDE",
        }

        for field in [
            "request_id",
            "method",
            "path",
            "status_code",
            "duration_ms",
            "remote_addr",
        ]:
            if hasattr(record, field):
                log_data[field] = getattr(record, field)

        return json.dumps(log_data, ensure_ascii=False)


def configure_logging() -> logging.Logger:
    logger = logging.getLogger("cement_factory_app")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    log_path = os.environ.get("LOG_FILE", "/var/log/app/application.log")
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    formatter = JSONFormatter()

    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    logger.propagate = False
    return logger
