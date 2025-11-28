import logging
import sys
from logging import LogRecord, Logger


class NoErrorFilter(logging.Filter):
    """Filter that suppresses ERROR records, letting INFO/DEBUG through."""

    def filter(self, record: LogRecord) -> bool:
        """Return True when the log record is not an ERROR level entry."""
        return record.levelno != logging.ERROR


def configure_logger() -> Logger:
    """Configure and return the shared pandasaurus logger."""
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    # logger.propagate = False

    # Create a console handler and set the level to INFO
    info = logging.StreamHandler()
    info.setLevel(logging.INFO)
    # Create a console handler and set the level to ERROR
    error = logging.StreamHandler()
    error.setLevel(logging.ERROR)

    # Create a formatter and set the format for log messages
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    info.setFormatter(formatter)
    error.setFormatter(formatter)
    error.addFilter(NoErrorFilter())
    # Add the console handler to the logger
    logger.addHandler(info)
    logger.addHandler(error)

    if "pytest" not in sys.modules:
        logger.propagate = False

    return logger
