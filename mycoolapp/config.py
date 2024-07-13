"""Config Processing."""

import contextlib
import logging
import os
import pprint
import pwd
import sys

import tomlkit

# This means that the logger will have the right name, logging should be done with this object
logger = logging.getLogger(__name__)

# Default config dictionary, also works as a schema
DEFAULT_CONFIG = {
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


class MyCoolAppConfig:
    """Config Object."""

    def __init__(self) -> None:
        """Initiate object with default config.

        Don't validate config yet
        Defaults shouldn't necessarily be enough to get the app to get to the point of starting the webapp.
        """
        self._config = DEFAULT_CONFIG

    """ These next special methods make this object behave like a dict, a few methods are missing
    __setitem__, __len__,__delitem__
    https://gist.github.com/turicas/1510860
    """

    def __getitem__(self, key: str) -> any:
        """Make this behave like a dictionary."""
        return self._config[key]

    def __contains__(self, key: str) -> str:
        """Make this behave like a dictionary."""
        return key in self._config

    def __repr__(self) -> str:
        """Make this behave like a dictionary."""
        return repr(self._config)

    def load_config_from_disk(self, instance_path: str) -> None:
        """Initiate config object, get config from file."""
        config_path = self._get_config_file_path(instance_path)

        config = self._load_file(config_path)

        config = self._ensure_all_default_config(DEFAULT_CONFIG, config)

        self._write_config(config, config_path)

        self._check_config(config)

        self._config = config

        logger.info("Config looks all good!")

    def load_config_from_dictionary(self, config: dict) -> None:
        """Initiate config dictionary, useful for testing."""
        config = self._ensure_all_default_config(DEFAULT_CONFIG, config)

        self._check_config(config)

        self._config = config

        logger.info("Config looks all good!")

    def log_config(self) -> None:
        """Log the config in full and nice and structured."""
        log_text = ">>>\nConfig dict attributes and their values:\n"
        log_text += f"{pprint.pformat(self._config)}"
        logger.debug(log_text)

    def _write_config(self, config: dict, config_path: str) -> None:
        """Write config file, used to write initial config to disk."""
        try:
            with open(config_path, "w", encoding="utf8") as toml_file:
                tomlkit.dump(config, toml_file)
        except PermissionError as exc:
            user_account = pwd.getpwuid(os.getuid())[0]
            err = f"Fix permissions: chown {user_account} {config_path}"
            raise PermissionError(err) from exc

    def _check_config(self, config: dict) -> None:
        """Validate Config. Exit the program if they don't validate."""
        failure = False

        self._warn_config_entry_not_in_schema(DEFAULT_CONFIG, config, "<root>")

        # KISM-BOILERPLATE: Put your settings validation here, set failure to True if it's a critical failure

        # Check & fail if key exists in app settings, this is just for testing/code coverage for the boilerplate.
        # This is a silly example and should be removed!
        if "configuration_failure" in config["app"]:
            logger.critical("Your config has the 'configuration_failure' key!")
            failure = True

        if failure:
            logger.critical("Config validation failed, Exiting")
            sys.exit(1)

    def _warn_config_entry_not_in_schema(self, target_dict: dict, base_dict: dict, parent_key: str) -> dict:
        """If the loaded config has a key that isn't in the schema (default config), we log a warning.

        This is recursive, be careful.
        """
        if parent_key != "flask":
            for key, value in base_dict.items():
                if isinstance(value, dict) and key in target_dict:
                    self._warn_config_entry_not_in_schema(target_dict[key], value, key)
                elif key not in target_dict:
                    if parent_key != "<root>":
                        parent_key = f"[{parent_key}]"

                    msg = f"Config entry key {parent_key}[{key}] not in schema"
                    logger.warning(msg)

        return target_dict

    def _ensure_all_default_config(self, base_dict: dict, target_dict: dict) -> dict:
        """This is recursive, be careful."""
        for key, value in base_dict.items():
            if isinstance(value, dict) and key in target_dict:
                self._ensure_all_default_config(value, target_dict[key])
            elif key not in target_dict:
                target_dict[key] = target_dict.get(key, value)

        return target_dict

    def _get_config_file_path(self, instance_path: str) -> str:
        """Figure out the config path to load config from."""
        config_path = None
        paths = []
        paths.append(instance_path + os.sep + "config.toml")
        paths.append(os.path.expanduser("~/.config/mycoolapp/config.toml"))
        paths.append("/etc/mycoolapp/config.toml")

        for path in paths:
            if os.path.isfile(path):
                logger.info("Found config at path: %s", path)
                if not config_path:
                    logger.info("Using this path as it's the first one that was found")
                    config_path = path
            else:
                logger.info("No config file found at: %s", path)

        if not config_path:
            config_path = paths[0]
            logger.warning("No configuration file found, creating at default location: %s", config_path)
            with contextlib.suppress(FileExistsError):
                os.makedirs(instance_path)  # Create instance path if it doesn't exist
            self._write_config(DEFAULT_CONFIG, config_path)

        return config_path

    def _load_file(self, config_path: str) -> dict:
        """Load config from file into a dict."""
        with open(config_path, encoding="utf8") as toml_file:
            return tomlkit.load(toml_file)
