"""Logger functionality for mycoolapp."""

import logging
from logging.handlers import RotatingFileHandler

from flask import Flask

LOGLEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
LOG_FORMAT = "%(asctime)s:%(levelname)s:%(name)s:%(message)s"

logger = logging.getLogger(__name__)  # Keep this somewhat consistent with the other modules


# Pass in the app to make it obvious what we are configuring.
# If we were to configure the logger object we get from logging.getLogger(__name__)
# and change that (modules) logging object's settings it would only be the mycoolapp.logger part.
# Were if we configure the app's root logger it trickles down to each module.
def setup_logger(app: Flask, mca_sett: dict | None = None) -> True:
    """APP LOGGING, set config per mca_sett."""
    # Configure modules that are external and have their own loggers
    logging.getLogger("waitress").setLevel(logging.INFO)
    logging.getLogger("werkzeug").setLevel(logging.DEBUG)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    # Figure out the settings we will use...
    mca_sett_dict = {"log_level": logging.INFO, "log_path": ""}
    if mca_sett:
        mca_sett_dict["log_level"] = mca_sett.log_level
        mca_sett_dict["log_path"] = mca_sett.log_path

    __set_formatter(app)
    __set_log_level(app, mca_sett_dict["log_level"])

    # If we are logging to a file
    if mca_sett_dict["log_path"] != "":
        __set_file_handler(app, mca_sett_dict["log_path"])

    if mca_sett:
        logger.info("Logger settings configured!")
    else:
        logger.info("Logger initial setup complete.")


def __set_formatter(app: Flask) -> True:
    """Setup the Formatting for the logger."""
    formatter = logging.Formatter(LOG_FORMAT)
    handler = app.logger.handlers[0]
    handler.setFormatter(formatter)


def __set_log_level(app: Flask, log_level: int | str) -> True:
    """Sets the log level."""
    if isinstance(log_level, str):
        log_level = log_level.upper()
        if log_level not in LOGLEVELS:
            logger.warning(
                "❗ Invalid logging level: %s, defaulting to INFO",
                app.logger.getEffectiveLevel(),
            )
        else:
            app.logger.setLevel(log_level)
            logger.debug("Set log level: %s", log_level)
    else:
        app.logger.setLevel(log_level)


def __set_file_handler(app: Flask, log_path: str) -> True:
    """Sets up the file handler."""
    try:
        filehandler = RotatingFileHandler(log_path, maxBytes=1000000, backupCount=5)
        formatter = logging.Formatter(LOG_FORMAT)
        filehandler.setFormatter(formatter)
        app.logger.addHandler(filehandler)
        logger.info("Logging to file: %s", log_path)
    except IsADirectoryError as exc:
        err = "You are trying to log to a directory, try a file"
        raise IsADirectoryError(err) from exc

    except PermissionError as exc:
        err = "The user running this does not have access to the file: " + log_path
        raise IsADirectoryError(err) from exc
