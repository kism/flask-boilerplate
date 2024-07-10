"""Setup the logger functionality for mycoolapp."""

import logging
from logging.handlers import RotatingFileHandler
from types import SimpleNamespace

from flask import Flask

LOGLEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
LOG_FORMAT = "%(asctime)s:%(levelname)s:%(name)s:%(message)s"


# In flask the root logger doesnt have any handlers, its all in app.logger
# root_logger : root,
# app.logger  : root, mycoolapp,
# logger      : root, mycoolapp, mycoolapp.module_name,
# The issue is that waitress, werkzeug (any any other modules that log) will log separately.
# The aim is, remove the default handler from the flask App and create one on the root logger to apply config to all.

root_logger = logging.getLogger()  # Get the root logger
logger = logging.getLogger(__name__)  # This is where we log to in this module, following the standard of every module.


# Pass in the app to make it obvious what we are configuring (the logger object within the app object).
def setup_logger(app: Flask, in_logging_conf: SimpleNamespace | None = None) -> None:
    """APP LOGGING, set config per mca_sett."""
    # Remove the Flask default handlers
    app.logger.handlers.clear()

    logging_conf = in_logging_conf

    # Figure out the config we will use...
    if not logging_conf:
        logging_conf = {"level": logging.INFO, "path": ""}

    # If the root_logger doesnt have a handler (It doesn't by default)
    if len(root_logger.handlers) == 0:
        _add_console_handler()

    _set_log_level(logging_conf["level"])

    # If we are logging to a file, this will only get called once since the default config don't have a log path
    if logging_conf["path"] != "":
        _add_file_handler(logging_conf["path"])

    # Configure modules that are external and have their own loggers
    logging.getLogger("waitress").setLevel(logging.INFO)  # Prod webserver, info has useful info.
    logging.getLogger("werkzeug").setLevel(logging.DEBUG)  # Only will be used in dev, debug logs incomming requests.
    logging.getLogger("urllib3").setLevel(logging.WARNING)  # Bit noisy when set to info, used by requests module.

    if in_logging_conf:
        logger.info("Logger config configured!")
    else:
        logger.info("Logger initial setup complete.")


def _add_console_handler() -> None:
    """Setup the Console handler."""
    formatter = logging.Formatter(LOG_FORMAT)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    root_logger.addHandler(console_handler)


def _set_log_level(log_level: int | str) -> None:
    """Sets the log level."""
    if isinstance(log_level, str):
        log_level = log_level.upper()
        if log_level not in LOGLEVELS:
            logger.warning(
                "❗ Invalid logging level: %s, defaulting to INFO",
                root_logger.getEffectiveLevel(),
            )
        else:
            root_logger.setLevel(log_level)
            logger.debug("Set log level: %s", log_level)
    else:
        root_logger.setLevel(log_level)


def _add_file_handler(log_path: str) -> None:
    """Sets up the file handler."""
    try:
        filehandler = RotatingFileHandler(log_path, maxBytes=1000000, backupCount=5)
        formatter = logging.Formatter(LOG_FORMAT)
        filehandler.setFormatter(formatter)
        root_logger.addHandler(filehandler)
        logger.info("Logging to file: %s", log_path)
    except IsADirectoryError as exc:
        err = "You are trying to log to a directory, try a file"
        raise IsADirectoryError(err) from exc

    except PermissionError as exc:
        err = "The user running this does not have access to the file: " + log_path
        raise PermissionError(err) from exc
