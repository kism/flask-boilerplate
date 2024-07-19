"""Blueprints for..."""

import logging

from flask import Blueprint, jsonify

# Modules should all setup logging like this so the log messages include the modules name.
# If you were to list all loggers with something like...
# `loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]`
# Before creating this object, you would not see a logger with this modules name (mycoolapp.this_module_name)
logger = logging.getLogger(__name__)  # Create a logger: mycoolapp.this_module_name, inherit config from root logger

bp = Blueprint("mycoolapp", __name__)


# KISM-BOILERPLATE: This is the demo api endpoint, enough to show a basic javascript interaction.
@bp.route("/hello/", methods=["GET"])
def get_hello() -> int:
    """Hello GET Method."""
    from flask import current_app

    mca_app_conf = current_app.config["app"]  # Get the config

    message = {"msg": mca_app_conf["my_message"]}
    status = 200

    logger.debug("GET request to /hello/, returning: %s", current_app.config["app"])

    return jsonify(message), status  # Return json, not a webpage.
