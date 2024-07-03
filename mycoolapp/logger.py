"""Setup the logger functionality for mycoolapp."""

import logging
from logging.handlers import RotatingFileHandler

from flask import Flask

LOGLEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
LOG_FORMAT = "%(asctime)s:%(levelname)s:%(name)s:%(message)s"


# In flask the root logger doesnt have any handlers, its all in app.logger
# root_logger : root,
# app.logger  : root, mycoolapp,
# logger      : root, mycoolapp, mycoolapp.module_name,
# The issue is that waitress, werkzeug (any any other modules that log) will log separately.
# The aim is, remove the default handler from the flask App and create one on the root logger to apply settings to all.

root_logger = logging.getLogger()  # Get the root logger
logger = logging.getLogger(__name__)  # This is where we log to in this module, following the standard of every module.


# Pass in the app to make it obvious what we are configuring (the logger object within the app object).
def setup_logger(app: Flask, mca_sett: dict | None = None) -> True:
    """APP LOGGING, set config per mca_sett."""
    # Remove the Flask default handlers
    app.logger.handlers.clear()

    # Figure out the settings we will use...
    mca_sett_dict = {"log_level": logging.INFO, "log_path": ""}
    if mca_sett:
        mca_sett_dict["log_level"] = mca_sett.log_level
        mca_sett_dict["log_path"] = mca_sett.log_path

    # If the root_logger doesnt have a handler (It doesn't by default)
    if len(root_logger.handlers) == 0:
        __add_console_handler()

    __set_log_level(mca_sett_dict["log_level"])

    # If we are logging to a file, this will only get called once since the default settings don't have a log path
    if mca_sett_dict["log_path"] != "":
        __add_file_handler(mca_sett_dict["log_path"])

    # Configure modules that are external and have their own loggers
    logging.getLogger("waitress").setLevel(logging.INFO)  # Prod webserver, info has useful info.
    logging.getLogger("werkzeug").setLevel(logging.DEBUG)  # Only will be used in dev, debug logs incomming requests.
    logging.getLogger("urllib3").setLevel(logging.WARNING)  # Bit noisy when set to info, used by requests module.

    if mca_sett:
        logger.info("Logger settings configured!")
    else:
        logger.info("Logger initial setup complete.")


def __add_console_handler() -> True:
    """Setup the Console handler."""
    formatter = logging.Formatter(LOG_FORMAT)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    root_logger.addHandler(console_handler)


def __set_log_level(log_level: int | str) -> True:
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


def __add_file_handler(log_path: str) -> True:
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
        raise IsADirectoryError(err) from exc
