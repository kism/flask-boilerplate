"""Config Processing."""

import contextlib
import logging
import os
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

    def __init__(self, config: dict | None = None, instance_path: str | None = None) -> None:
        """Initiate object with default config.

        Don't validate config yet
        Defaults shouldn't necessarily be enough to get the app to get to the point of starting the webapp.
        """
        self._config_path = None

        self._config = DEFAULT_CONFIG

        self.instance_path = instance_path

        self._get_config_file_path()

        if not config:
            config = self._load_file()

        self._config = self._merge_with_defaults(DEFAULT_CONFIG, config)

        self._validate_config()

        self._write_config()

        logger.info("Configuration loaded successfully!")

    """ These next special methods make this object behave like a dict, a few methods are missing
    __setitem__, __len__,__delitem__
    https://gist.github.com/turicas/1510860
    """

    def __getitem__(self, key: str) -> any:
        """Get item from config like a dictionary."""
        return self._config[key]

    def __contains__(self, key: str) -> str:
        """Check if key is 'in' the configuration."""
        return key in self._config

    def __repr__(self) -> str:
        """Return string representation of the config."""
        return repr(self._config)

    def _write_config(self) -> None:
        """Write configuration to a file."""
        try:
            with open(self._config_path, "w", encoding="utf8") as toml_file:
                tomlkit.dump(self._config, toml_file)
        except PermissionError as exc:
            user_account = pwd.getpwuid(os.getuid())[0]
            err = f"Fix permissions: chown {user_account} {self._config_path}"
            raise PermissionError(err) from exc

    def _validate_config(self) -> dict:
        """Validate Config. Exit the program if they don't validate."""
        failure = False

        self._warn_unexpected_keys(DEFAULT_CONFIG, self._config, "<root>")

        # KISM-BOILERPLATE: Put your settings validation here, set failure to True if it's a critical failure

        # Check & fail if key exists in app settings, this is just for testing/code coverage for the boilerplate.
        # This is a silly example and should be removed!
        if "configuration_failure" in self._config["app"]:
            logger.critical("Config contains 'configuration_failure' key!")
            failure = True

        if failure:
            logger.critical("Config validation failed, Exiting.")
            sys.exit(1)


    def _warn_unexpected_keys(self, target_dict: dict, base_dict: dict, parent_key: str) -> dict:
        """If the loaded config has a key that isn't in the schema (default config), we log a warning.

        This is recursive, be careful.
        """
        if parent_key != "flask":
            for key, value in base_dict.items():
                if isinstance(value, dict) and key in target_dict:
                    self._warn_unexpected_keys(target_dict[key], value, key)
                elif key not in target_dict:
                    if parent_key != "<root>":
                        parent_key = f"[{parent_key}]"

                    msg = f"Config entry key {parent_key}[{key}] not in schema"
                    logger.warning(msg)

        return target_dict

    def _merge_with_defaults(self, base_dict: dict, target_dict: dict) -> dict:
        """This is recursive, be careful."""
        for key, value in base_dict.items():
            if isinstance(value, dict) and key in target_dict:
                self._merge_with_defaults(value, target_dict[key])
            elif key not in target_dict:
                target_dict[key] = target_dict.get(key, value)

        return target_dict

    def _get_config_file_path(self) -> str:
        """Figure out the config path to load config from."""
        paths = [
            os.path.join(self.instance_path, "config.toml"),
            os.path.expanduser("~/.config/mycoolapp/config.toml"),
            "/etc/mycoolapp/config.toml",
        ]

        for path in paths:
            if os.path.isfile(path):
                logger.info("Found config at path: %s", path)
                if not self._config_path:
                    logger.info("Using this path as it's the first one that was found")
                    self._config_path = path
            else:
                logger.info("No config file found at: %s", path)

        if not self._config_path:
            self._config_path = paths[0]
            logger.warning("No configuration file found, creating at default location: %s", self._config_path)
            with contextlib.suppress(FileExistsError):
                os.makedirs(self.instance_path)  # Create instance path if it doesn't exist
            self._write_config()

    def _load_file(self) -> dict:
        """Load configuration from a file."""
        with open(self._config_path, encoding="utf8") as toml_file:
            return tomlkit.load(toml_file)
