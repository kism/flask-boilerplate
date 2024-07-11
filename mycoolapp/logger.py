"""Setup the logger functionality for mycoolapp."""

import logging
from logging.handlers import RotatingFileHandler

from flask import Flask

LOGLEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]  # Valid str logging levels.
LOG_FORMAT = "%(asctime)s:%(levelname)s:%(name)s:%(message)s"  # This is the logging message format that I like.


# In flask the root logger doesnt have any handlers, its all in app.logger
# root_logger : root,
# app.logger  : root, mycoolapp,
# logger      : root, mycoolapp, mycoolapp.module_name,
# The issue is that waitress, werkzeug (any any other modules that log) will log separately.
# The aim is, remove the default handler from the flask App and create one on the root logger to apply config to all.

logger = logging.getLogger(__name__)  # This is where we log to in this module, following the standard of every module.


# Pass in the app to make it obvious what we are configuring (the logger object within the app object).
def setup_logger(app: Flask, logging_conf: dict, in_logger: logging.Logger | None = None) -> None:
    """APP LOGGING, set config per mca_conf."""
    if not in_logger:  # Only the case when testing with pytest.
        in_logger = logging.getLogger()  # Get the root logger

    app.logger.handlers.clear()  # Remove the Flask default handlers

    # If the logger doesnt have a console handler (root logger doesn't by default)
    if not _has_console_handler(in_logger):
        _add_console_handler(in_logger)

    _set_log_level(in_logger, logging_conf["level"])

    # If we are logging to a file
    if not _has_file_handler(in_logger) and logging_conf["path"] != "":
        _add_file_handler(in_logger, logging_conf["path"])

    # Configure modules that are external and have their own loggers
    logging.getLogger("waitress").setLevel(logging.INFO)  # Prod webserver, info has useful info.
    logging.getLogger("werkzeug").setLevel(logging.DEBUG)  # Only will be used in dev, debug logs incomming requests.
    logging.getLogger("urllib3").setLevel(logging.WARNING)  # Bit noisy when set to info, used by requests module.

    logger.info("Logger config set!")


def _has_file_handler(in_logger: logging.Logger) -> bool:
    """Check if logger has file handler."""
    return any(isinstance(handler, logging.FileHandler) for handler in in_logger.handlers)


def _has_console_handler(in_logger: logging.Logger) -> bool:
    """Check if logger has console handler."""
    return any(isinstance(handler, logging.StreamHandler) for handler in in_logger.handlers)


def _add_console_handler(in_logger: logging.Logger) -> None:
    """Setup the Console handler."""
    formatter = logging.Formatter(LOG_FORMAT)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    in_logger.addHandler(console_handler)


def _set_log_level(in_logger: logging.Logger, log_level: int | str) -> None:
    """Sets the log level."""
    if isinstance(log_level, str):
        log_level = log_level.upper()
        if log_level not in LOGLEVELS:
            in_logger.setLevel("INFO")
            logger.warning(
                "❗ Invalid logging level: %s, defaulting to INFO",
                in_logger.getEffectiveLevel(),
            )
        else:
            in_logger.setLevel(log_level)
            logger.debug("Set log level: %s", log_level)
    else:
        in_logger.setLevel(log_level)


def _add_file_handler(in_logger: logging.Logger, log_path: str) -> None:
    """Sets up the file handler."""
    try:
        filehandler = RotatingFileHandler(log_path, maxBytes=1000000, backupCount=5)
    except IsADirectoryError as exc:
        err = "You are trying to log to a directory, try a file"
        raise IsADirectoryError(err) from exc
    except PermissionError as exc:
        err = "The user running this does not have access to the file: " + log_path
        raise PermissionError(err) from exc

    formatter = logging.Formatter(LOG_FORMAT)
    filehandler.setFormatter(formatter)
    in_logger.addHandler(filehandler)
    logger.info("Logging to file: %s", log_path)
