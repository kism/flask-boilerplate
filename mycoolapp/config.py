"""Settings Processing."""

import contextlib
import logging
import os
import pprint
import pwd
import sys

import tomlkit

# This means that the logger will have the right name, loging should be done with this object
logger = logging.getLogger(__name__)

DEFAULT_SETTINGS = {
    "app": {
        "my_message": "Hello, World!",
        "configuration_failure": False,
    },
    "logging": {
        "level": "INFO",
        "path": "",
    },
    "flask": {  # This section is for Flask default config entries https://flask.palletsprojects.com/en/3.0.x/config/
        "DEBUG": False,
    },
}


class MyCoolAppConfig:
    """Settings Object."""

    def __init__(self) -> None:
        """Initiate object with default settings.

        Don't validate settings yet
        Defaults shouldnt necessaraly be enough to get the app to get to the point of starting the webapp.
        """
        self._settings = DEFAULT_SETTINGS

    def __getitem__(self, key: str) -> any:
        """Make this behave like a dictionary."""
        return self._settings[key]

    def __contains__(self, key: str) -> str:
        """Make this behave like a dictionary."""
        return key in self._settings

    def __repr__(self) -> str:
        """Make this behave like a dictionary."""
        return repr(self._settings)

    def load_settings_from_disk(self, instance_path: str) -> None:
        """Initiate settings object, get settings from file."""
        settings_path = self.__get_settings_file_path(instance_path)

        settings = self.__load_file(settings_path)

        settings = self.__ensure_all_default_settings(DEFAULT_SETTINGS, settings)

        self.__write_settings(settings, settings_path)

        self.__check_settings(settings)

        self._settings = settings

        logger.info("Config looks all good!")

    def load_settings_from_dictionary(self, settings: dict) -> None:
        """Initiate settings dictionary, useful for testing."""
        settings = self.__ensure_all_default_settings(DEFAULT_SETTINGS, settings)

        self.__check_settings(settings)

        self._settings = settings

        logger.info("Config looks all good!")

    def log_settings(self) -> None:
        """Log the settings in full and nice and structured."""
        log_text = ">>>\nSettings object attributes and their values:\n"
        log_text += f"{pprint.pformat(self._settings)}"
        logger.debug(log_text)

    def __write_settings(self, settings: dict, settings_path: str) -> None:
        """Write settings file, used to write initial config to disk."""
        try:
            with open(settings_path, "w", encoding="utf8") as toml_file:
                settings_write_temp = settings.copy()
                tomlkit.dump(settings_write_temp, toml_file)
        except PermissionError as exc:
            user_account = pwd.getpwuid(os.getuid())[0]
            err = f"Fix permissions: chown {user_account} {settings_path}"
            raise PermissionError(err) from exc

    def __check_settings(self, settings: dict) -> True:
        """Validate Settings. Exit the program if they don't validate."""
        failure = False

        if settings["app"]["configuration_failure"]:
            failure = True  # This is a silly example

        if failure:
            logger.error("Settings validation failed")
            logger.critical("Exiting")
            sys.exit(1)

    def __ensure_all_default_settings(self, base_dict: dict, target_dict: dict) -> dict:
        for key, value in base_dict.items():
            if isinstance(value, dict) and key in target_dict:
                self.__ensure_all_default_settings(value, target_dict[key])
            elif key not in target_dict:
                target_dict[key] = target_dict.get(key, value)

        return target_dict

    def __get_settings_file_path(self, instance_path: str) -> str:
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
            logger.warning("No configuration file found, creating at default location: %s", settings_path)
            with contextlib.suppress(Exception):
                os.makedirs(instance_path)  # Create instance path if it doesn't exist
            self.__write_settings(DEFAULT_SETTINGS, settings_path)

        return settings_path

    def __load_file(self, settings_path: str) -> dict:
        """Load settings from file into a dict."""
        with open(settings_path, encoding="utf8") as toml_file:
            return tomlkit.load(toml_file)
