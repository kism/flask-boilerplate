"""Settings Processing."""

import contextlib
import logging
import os
import pwd
import sys
from types import SimpleNamespace

import tomlkit

# This means that the logger will have the right name, loging should be done with this object
logger = logging.getLogger(__name__)

DEFAULT_SETTINGS = {
    "app": {
        "my_message": "Hello, World!",
    },
    "logging": {
        "level": "INFO",
        "path": "",
    },
    "flask": {  # This section is for Flask default config entries https://flask.palletsprojects.com/en/3.0.x/config/
        "DEBUG": False,
    },
}


def load_settings_from_disk(instance_path: str) -> None:
    """Initiate settings object, get settings from file."""
    settings_path = __get_settings_dir(instance_path)  # Get the path of the settings file

    settings = __load_settings(settings_path)  # Load settings from file

    __write_settings(settings, settings_path)  # Re-write the settings file

    __check_settings(settings)  # This will exit the program if there is a config issue

    settings = __dict_to_namespace(settings)

    logger.info("Config looks all good!")

    return settings


def __write_settings(settings: dict, settings_path: str) -> None:
    """Write settings file."""
    try:
        with open(settings_path, "w", encoding="utf8") as toml_file:
            settings_write_temp = settings.copy()
            tomlkit.dump(settings_write_temp, toml_file)
    except PermissionError as exc:
        user_account = pwd.getpwuid(os.getuid())[0]
        err = f"Fix permissions: chown {user_account} {settings_path}"
        raise PermissionError(err) from exc


def __check_settings(settings: dict) -> True:
    """Validate Settings."""
    failure = False

    if "app" not in settings:
        failure = True  # Somehow no app section of settings

    if failure:
        logger.error("Settings validation failed")
        logger.critical("Exiting")
        sys.exit(1)


def __get_settings_dir(instance_path: str) -> str:
    """Figure out the settings path to load settings from."""
    settings_path = None
    paths = []
    paths.append(instance_path + os.sep + "settings.toml")
    paths.append(os.path.expanduser("~/.config/mycoolapp/settings.toml"))
    paths.append("/etc/mycoolapp/settings.toml")

    for path in paths:
        if os.path.exists(path):
            logger.info("Found settings at path: %s", path)
            if not settings_path:
                logger.info("Using this path as it's the first one that was found")
                settings_path = path
        else:
            logger.info("No settings file found at: %s", path)

    if not settings_path:
        settings_path = paths[0]
        logger.critical("No configuration file found, creating at default location: %s", settings_path)
        with contextlib.suppress(Exception):
            os.makedirs(instance_path)  # Create instance path if it doesn't exist
        __write_settings()

    return settings_path


def __load_settings(settings_path: str) -> dict:
    """Load settings from file into a dict."""
    settings = {}

    with open(settings_path, encoding="utf8") as toml_file:
        settings_temp = tomlkit.load(toml_file)

    # Set the variables of this object
    for settings_key in DEFAULT_SETTINGS:
        try:
            settings[settings_key] = settings_temp[settings_key]
        except (KeyError, TypeError):
            logger.info("%s not defined, leaving as default", settings_key)

    return settings


def __dict_to_namespace(d: any) -> any:
    """I prefer to access the settings via a namespace, no brackets and keys."""
    if isinstance(d, dict):
        # Convert nested dictionaries to SimpleNamespace
        return SimpleNamespace(**{k: __dict_to_namespace(v) for k, v in d.items()})

    return d
