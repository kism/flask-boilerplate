"""Demo object."""


# KISM-BOILERPLATE: Demo object, doesn't do much
class MyCoolObject:
    """Demo object."""

    def __init__(self, {{cookiecutter.app_config_var}}: dict) -> None:
        """Init config for the NGINX Allowlist Writer."""
        # Monitor Writing
        self._my_message = {{cookiecutter.app_config_var}}["app"]["my_message"]

    def get_my_message_backwards(self) -> str:
        """Return the string backwards."""
        return self._my_message[::-1]
