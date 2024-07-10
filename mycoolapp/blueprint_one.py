"""Blueprints for ..."""

import logging

from flask import Blueprint, jsonify

from . import get_mycoolapp_config

mca_sett = get_mycoolapp_config()  # Get the config

# This means that the logger will have the right name, loging should be done with this object
# If you were to list all loggers with something like...
# `loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]`
# Before creating this object, you would not see a logger with this modules name (mycoolapp.this_module_name)
logger = logging.getLogger(__name__)  # Create a logger named mycoolapp.this_module_name

bp = Blueprint("mycoolapp", __name__)


@bp.route("/hello/", methods=["GET"])
def get_hello() -> int:
    """Hello GET Method."""
    message = {"msg": mca_sett["app"]["my_message"]}
    status = 200

    logger.debug("GET request to /hello/, returning: %s", mca_sett["app"]["my_message"])

    return jsonify(message), status
