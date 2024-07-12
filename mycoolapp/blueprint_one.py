"""Blueprints for ..."""

import logging

from flask import Blueprint, jsonify

from . import get_mycoolapp_config

mca_conf = get_mycoolapp_config()  # Get the config

# This means that the logger will have the right name, logging should be done with this object
# If you were to list all loggers with something like...
# `loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]`
# Before creating this object, you would not see a logger with this modules name (mycoolapp.this_module_name)
logger = logging.getLogger(__name__)  # Create a logger: mycoolapp.this_module_name, inherit config from root logger

bp = Blueprint("mycoolapp", __name__)


# KISM-BOILERPLATE, this is the demo api endpoint, enough to show a basic javascript interaction.
@bp.route("/hello/", methods=["GET"])
def get_hello() -> int:
    """Hello GET Method."""
    message = {"msg": mca_conf["app"]["my_message"]}
    status = 200

    logger.debug("GET request to /hello/, returning: %s", mca_conf["app"]["my_message"])

    return jsonify(message), status
