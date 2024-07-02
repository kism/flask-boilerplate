"""Settings Processing."""

import logging
import os
import pwd
import sys

import yaml

# This means that the logger will have the right name, loging should be done with this object
logger = logging.getLogger(__name__)

DEFAULT_SETTINGS = {
    "log_level": "INFO",
    "log_path": "",
    "my_message": "Hello user!",
}


class MyCoolAppSettings:
    """Object Definition for the settings of the app."""

    def __init__(self) -> None:
        """Initiate settings object, get settings from file."""
        # Load the settings from one of the paths
        self.settings_path = None

        paths = []
        paths.append(os.getcwd() + os.sep + "settings.yml")
        paths.append(os.path.expanduser("~/.config/mycoolapp/settings.yml"))
        paths.append("/etc/mycoolapp/settings.yml")

        for path in paths:
            if os.path.exists(path):
                logger.info("Found settings at path: %s", path)
                if not self.settings_path:
                    logger.info("Using this path as it's the first one that was found")
                    self.settings_path = path
            else:
                logger.info("No settings file found at: %s", path)

        if not self.settings_path:
            self.settings_path = paths[0]
            logger.critical("No configuration file found, creating at default location: %s", self.settings_path)
            self.__write_settings()

        # Load settings file from path
        with open(self.settings_path, encoding="utf8") as yaml_file:
            settings_temp = yaml.safe_load(yaml_file)

        # Set the variables of this object
        for key, default_value in DEFAULT_SETTINGS.items():
            try:
                setattr(self, key, settings_temp[key])
            except (KeyError, TypeError):
                logger.info("%s not defined, using default", key)
                setattr(self, key, default_value)

        self.__write_settings()

        self.__check_settings()

        logger.info("Config looks all good!")

    def __write_settings(self) -> None:
        """Write settings file."""
        try:
            with open(self.settings_path, "w", encoding="utf8") as yaml_file:
                settings_write_temp = vars(self).copy()
                del settings_write_temp["settings_path"]
                yaml.safe_dump(settings_write_temp, yaml_file)
        except PermissionError as exc:
            user_account = pwd.getpwuid(os.getuid())[0]
            err = f"Fix permissions: chown {user_account} {self.settings_path}"
            raise PermissionError(err) from exc

    def __check_settings(self) -> True:
        """Validate Settings."""
        failure = False

        if failure:
            logger.error("Settings validation failed")
            logger.critical("Exiting")
            sys.exit(1)
