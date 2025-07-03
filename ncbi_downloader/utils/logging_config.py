import logging
from logging.handlers import RotatingFileHandler


def configure_logging(log_file: str | None = None, level: int = logging.INFO) -> None:
    """Configure basic logging for the application.

    Parameters
    ----------
    log_file : str | None, optional
        Optional path to a log file. If provided, logs will also be written to
        this file with rotation.
    level : int, optional
        Logging level, by default ``logging.INFO``.
    """
    handlers = [logging.StreamHandler()]

    if log_file:
        file_handler = RotatingFileHandler(log_file, maxBytes=1_000_000, backupCount=3)
        handlers.append(file_handler)

    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=handlers,
    )

